"""Dependency-free compatibility and package regression tests."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "route-reasoning"
MANIFEST = SKILL / "SKILL.md"
PLATFORMS = SKILL / "references" / "platforms.md"
CASES = ROOT / "tests" / "routing_cases.json"
BUILD = ROOT / "scripts" / "build_dist.py"
ARCHIVE = ROOT / "dist" / "route-reasoning-skill.zip"
PACKAGE = "route-reasoning"
LENSES = {"Socrates", "Aristotle", "Plato", "Descartes", "Hume", "Kant", "Hegel"}
FRONTMATTER = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
REPOSITORY_ONLY = {".git", ".github", "build", "dist", "tests", "__pycache__"}


def metadata(text: str) -> dict[str, str]:
    match = FRONTMATTER.match(text)
    if not match:
        raise AssertionError("SKILL.md does not start with YAML frontmatter")
    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        field = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if not field:
            raise AssertionError(f"invalid frontmatter line: {line!r}")
        value = field.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        fields[field.group(1)] = value
    return fields


class RouteReasoningRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = MANIFEST.read_text(encoding="utf-8")
        cls.platform_text = PLATFORMS.read_text(encoding="utf-8")

    def test_canonical_frontmatter_and_core_behavior(self) -> None:
        self.assertTrue(MANIFEST.is_file())
        frontmatter = metadata(self.skill_text)
        self.assertEqual(PACKAGE, frontmatter.get("name"))
        description = frontmatter.get("description", "")
        self.assertTrue(description)
        self.assertLessEqual(len(description), 200)
        self.assertIn("/route-reasoning", description)

        for lens in LENSES:
            self.assertRegex(self.skill_text, rf"\|[^\n|]*\|\s*{lens}\s*\|")
        self.assertIn("`--auto` requests automatic routing", self.skill_text)
        self.assertIn("`--lens` selects the primary lens and overrides automatic routing", self.skill_text)
        self.assertIn("`--reviewer` selects a reviewer without replacing the primary lens", self.skill_text)
        self.assertIn("Do not expose private chain-of-thought", self.skill_text)
        self.assertIn("Keep internal reasoning private", self.skill_text)

    def test_command_contract(self) -> None:
        for form in (
            "/route-reasoning <request>",
            "/route-reasoning --lens <lens> <request>",
            "/route-reasoning --reviewer <lens> <request>",
            "/route-reasoning --lens <lens> --reviewer <lens> <request>",
            "/route-reasoning --auto <request>",
            "/route-reasoning --hide-lenses <request>",
        ):
            self.assertIn(form, self.skill_text)
        self.assertIn("Lens names are case-insensitive", self.skill_text)
        self.assertIn("For an unknown flag, return a short correction", self.skill_text)
        self.assertIn("suppresses lens labels in the answer, not the reasoning procedure", self.skill_text)

    def test_evaluation_case_coverage(self) -> None:
        cases = {case["id"]: case for case in json.loads(CASES.read_text(encoding="utf-8"))}
        expected_primary = {
            "ambiguous-requirement": "Socrates",
            "debug-parser": "Descartes",
            "benchmark-adoption": "Hume",
            "spec-review": "Kant",
            "architecture-tension": "Hegel",
            "reusable-frame-model": "Plato",
            "root-cause-system": "Aristotle",
        }
        for case_id, lens in expected_primary.items():
            self.assertEqual(lens, cases[case_id]["primary"])
        self.assertTrue(cases["manual-override"]["explicit_override"])
        self.assertTrue(cases["explicit-reviewer"]["explicit_reviewer"])
        self.assertEqual("Kant", cases["explicit-reviewer"]["reviewer"])
        self.assertTrue(cases["hide-lens-labels"]["hide_lenses"])
        self.assertFalse(cases["simple-question-no-routing"]["should_route"])
        self.assertIsNone(cases["simple-question-no-routing"]["primary"])

    def test_platform_regressions(self) -> None:
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file(), "Codex metadata is missing")
        self.assertIn("## Codex", self.platform_text)
        self.assertIn("$route-reasoning", self.platform_text)

        self.assertIn(".claude/skills/route-reasoning/", self.platform_text)
        self.assertIn("~/.claude/skills/route-reasoning/", self.platform_text)

        self.assertIn(".agents/skills/route-reasoning/", self.platform_text)
        self.assertIn("~/.gemini/config/skills/route-reasoning/", self.platform_text)
        self.assertIn("~/.gemini/antigravity-cli/skills/route-reasoning/", self.platform_text)

        self.assertIn("## OpenCode", self.platform_text)
        self.assertIn("does not yet document a verified OpenCode installation path", self.platform_text)

    def test_package_contract(self) -> None:
        subprocess.run([sys.executable, str(BUILD)], cwd=ROOT, check=True)
        self.assertTrue(ARCHIVE.is_file())

        expected = {
            f"{PACKAGE}/{path.relative_to(SKILL).as_posix()}"
            for path in SKILL.rglob("*")
            if path.is_file() and path.relative_to(SKILL).parts[0] in {"SKILL.md", "agents", "assets", "references", "scripts"}
        }
        with zipfile.ZipFile(ARCHIVE) as package:
            names = package.namelist()
            files = {name for name in names if not name.endswith("/")}
            self.assertEqual({PACKAGE}, {PurePosixPath(name).parts[0] for name in names})
            self.assertIn(f"{PACKAGE}/SKILL.md", files)
            self.assertTrue(
                {
                    f"{PACKAGE}/references/lenses.md",
                    f"{PACKAGE}/references/coding.md",
                    f"{PACKAGE}/references/platforms.md",
                }.issubset(files)
            )
            self.assertEqual(expected, files)

            for name in files:
                relative = Path(*PurePosixPath(name).parts[1:])
                self.assertFalse(any(part.lower() in REPOSITORY_ONLY for part in relative.parts), name)
                self.assertFalse(relative.name.lower().startswith("readme"), name)
                self.assertNotEqual("license", relative.name.lower(), name)
                self.assertEqual((SKILL / relative).read_bytes(), package.read(name), name)

        for reference in re.findall(r"`(references/[^`]+\.md)`", self.skill_text):
            self.assertIn(f"{PACKAGE}/{reference}", files)


if __name__ == "__main__":
    unittest.main()
