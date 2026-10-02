#!/usr/bin/env python3
"""Build a reproducible runtime-only Route Reasoning skill archive."""

from __future__ import annotations

import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
SKILL = ROOT / "skills" / "route-reasoning"
DIST = ROOT / "dist"
OUTPUT = DIST / "route-reasoning-skill.zip"
PACKAGE_NAME = "route-reasoning"
RUNTIME_DIRECTORIES = {"agents", "assets", "references", "scripts"}
REPOSITORY_ONLY_PARTS = {
    ".git",
    ".github",
    "build",
    "dist",
    "tests",
    "__pycache__",
}
SECRET_NAME = re.compile(
    r"(?:^|[-_.])(api[-_]?key|credential|password|secret|token|private[-_]?key|id_rsa)(?:$|[-_.])",
    re.IGNORECASE,
)
FRONTMATTER = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_inside_repository(path: Path) -> None:
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve {path}: {exc}")
    if not resolved.is_relative_to(ROOT_RESOLVED):
        fail(f"symlink or path escapes the repository: {path}")


def is_repository_only(relative: Path) -> bool:
    if any(part.lower() in REPOSITORY_ONLY_PARTS for part in relative.parts):
        return True
    name = relative.name.lower()
    return name == "license" or name.startswith("readme")


def is_secret_like(relative: Path) -> bool:
    name = relative.name.lower()
    return name == ".env" or name.startswith(".env.") or bool(SECRET_NAME.search(name)) or name.endswith(
        (".key", ".pem", ".p12", ".pfx")
    )


def parse_frontmatter(skill_text: str) -> dict[str, str]:
    match = FRONTMATTER.match(skill_text)
    if not match:
        fail("SKILL.md must start with YAML frontmatter")

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        field = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if not field:
            fail(f"unsupported or invalid frontmatter line: {line!r}")
        value = field.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        fields[field.group(1)] = value
    return fields


def validate_manifest() -> None:
    manifest = SKILL / "SKILL.md"
    if not manifest.is_file():
        fail("missing canonical skills/route-reasoning/SKILL.md")
    ensure_inside_repository(manifest)

    metadata = parse_frontmatter(manifest.read_text(encoding="utf-8"))
    if metadata.get("name") != PACKAGE_NAME:
        fail("frontmatter name must be route-reasoning")
    description = metadata.get("description", "")
    if not description:
        fail("frontmatter description is missing")
    if len(description) > 200:
        fail("frontmatter description must be 200 characters or fewer")

    text = manifest.read_text(encoding="utf-8")
    candidates = re.findall(r"`([^`]+)`", text)
    candidates.extend(re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", text))
    for candidate in candidates:
        candidate_path = Path(candidate)
        if (
            candidate_path.parts
            and candidate_path.parts[0] in RUNTIME_DIRECTORIES
            and not candidate_path.is_absolute()
        ):
            target = SKILL / candidate_path
            if not target.is_file():
                fail(f"missing local reference mentioned by SKILL.md: {candidate}")
            ensure_inside_repository(target)


def source_files() -> list[Path]:
    if not SKILL.is_dir():
        fail("missing canonical skill directory")
    ensure_inside_repository(SKILL)

    files: list[Path] = []
    manifest = SKILL / "SKILL.md"
    if manifest.is_file():
        files.append(manifest)

    for top_level in sorted(RUNTIME_DIRECTORIES):
        directory = SKILL / top_level
        if not directory.exists():
            continue
        if not directory.is_dir():
            fail(f"runtime path must be a directory: {directory.relative_to(ROOT)}")
        ensure_inside_repository(directory)

        for current, directories, filenames in os.walk(directory, followlinks=False):
            current_path = Path(current)
            directories.sort()
            filenames.sort()
            for name in [*directories, *filenames]:
                path = current_path / name
                relative = path.relative_to(SKILL)
                if path.is_symlink():
                    ensure_inside_repository(path)
                    fail(f"symlinks are not supported in the runtime package: {relative}")
                if is_secret_like(relative):
                    fail(f"secret-like runtime file is not allowed: {relative}")
                if is_repository_only(relative):
                    continue
                ensure_inside_repository(path)
                if path.is_file():
                    files.append(path)

    if is_secret_like(manifest.relative_to(SKILL)):
        fail("canonical SKILL.md has a secret-like filename")
    return sorted(files, key=lambda path: path.relative_to(SKILL).as_posix())


def stage_files(files: list[Path], staging_root: Path) -> None:
    staged_skill = staging_root / PACKAGE_NAME
    for source in files:
        relative = source.relative_to(SKILL)
        destination = staged_skill / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def zip_info(name: str, is_directory: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
    info.create_system = 3
    info.external_attr = ((0o40755 if is_directory else 0o100644) << 16)
    info.compress_type = zipfile.ZIP_STORED
    return info


def write_archive(staging_root: Path, files: list[Path], archive: Path) -> set[str]:
    relative_files = [source.relative_to(SKILL).as_posix() for source in files]
    expected_files = {f"{PACKAGE_NAME}/{relative}" for relative in relative_files}
    directories = {PACKAGE_NAME}
    for relative in relative_files:
        parent = PurePosixPath(relative).parent
        while str(parent) != ".":
            directories.add(f"{PACKAGE_NAME}/{parent.as_posix()}")
            parent = parent.parent

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as package:
        for directory in sorted(directories):
            package.writestr(zip_info(f"{directory}/", is_directory=True), b"")
        for relative in relative_files:
            data = (staging_root / PACKAGE_NAME / relative).read_bytes()
            package.writestr(zip_info(f"{PACKAGE_NAME}/{relative}", is_directory=False), data)
    return expected_files


def inspect_archive(archive: Path, expected_files: set[str]) -> None:
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        if len(names) != len(set(names)):
            fail("archive contains duplicate paths")
        if not names:
            fail("archive is empty")

        for name in names:
            path = PurePosixPath(name)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                fail(f"archive contains an unsafe path: {name}")
            if path.parts[0] != PACKAGE_NAME:
                fail(f"archive contains a file outside {PACKAGE_NAME}/: {name}")
            relative = Path(*path.parts[1:])
            if relative.parts and is_repository_only(relative):
                fail(f"archive includes repository-only content: {name}")
            if relative.parts and is_secret_like(relative):
                fail(f"archive includes a secret-like file: {name}")

        archived_files = {name for name in names if not name.endswith("/")}
        missing = expected_files - archived_files
        unexpected = archived_files - expected_files
        if missing or unexpected:
            fail(f"archive file set mismatch; missing={sorted(missing)}, unexpected={sorted(unexpected)}")
        if f"{PACKAGE_NAME}/SKILL.md" not in archived_files:
            fail("archive is missing route-reasoning/SKILL.md")


def main() -> None:
    validate_manifest()
    files = source_files()
    DIST.mkdir(exist_ok=True)

    temporary_archive: Path | None = None
    try:
        with tempfile.TemporaryDirectory(prefix=".route-reasoning-build-", dir=ROOT) as temporary_directory:
            staging_root = Path(temporary_directory)
            stage_files(files, staging_root)
            descriptor, archive_name = tempfile.mkstemp(prefix=".route-reasoning-", suffix=".zip", dir=DIST)
            os.close(descriptor)
            temporary_archive = Path(archive_name)
            expected_files = write_archive(staging_root, files, temporary_archive)
            inspect_archive(temporary_archive, expected_files)
            temporary_archive.replace(OUTPUT)
            temporary_archive = None
    finally:
        if temporary_archive and temporary_archive.exists():
            temporary_archive.unlink()

    print(f"Built {OUTPUT.relative_to(ROOT)} ({len(files)} files)")
    print("Archive validation passed.")


if __name__ == "__main__":
    main()
