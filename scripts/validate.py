#!/usr/bin/env python3
"""Dependency-free structural checks for the public Route Reasoning package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "route-reasoning"
MANIFEST = SKILL / "SKILL.md"
CASES = ROOT / "tests" / "routing_cases.json"
LENSES = {"Socrates", "Aristotle", "Plato", "Descartes", "Hume", "Kant", "Hegel"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_manifest() -> None:
    if not MANIFEST.is_file():
        fail(f"missing {MANIFEST.relative_to(ROOT)}")

    text = MANIFEST.read_text(encoding="utf-8")
    if "TODO" in text or "[TODO" in text:
        fail("runtime skill contains placeholder text")
    if len(text.splitlines()) >= 500:
        fail("SKILL.md must remain below 500 lines")

    frontmatter = re.match(r"\A---\n(?P<body>.*?)\n---\n", text, re.DOTALL)
    if not frontmatter:
        fail("SKILL.md must start with YAML frontmatter")

    yaml = frontmatter.group("body")
    if not re.search(r"^name:\s*route-reasoning\s*$", yaml, re.MULTILINE):
        fail("frontmatter name must be route-reasoning")
    description = re.search(r"^description:\s*(.+)$", yaml, re.MULTILINE)
    if not description or len(description.group(1).strip()) < 80:
        fail("frontmatter description is missing or too vague")

    for relative in re.findall(r"`(references/[^`]+\.md)`", text):
        if not (SKILL / relative).is_file():
            fail(f"missing referenced file: {relative}")

    for required in [
        "references/lenses.md",
        "references/coding.md",
        "references/platforms.md",
        "agents/openai.yaml",
    ]:
        if not (SKILL / required).is_file():
            fail(f"missing runtime resource: {required}")


def validate_cases() -> None:
    try:
        cases = json.loads(CASES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid routing cases: {exc}")

    if not isinstance(cases, list) or len(cases) < 7:
        fail("routing cases must contain at least seven cases")

    seen: set[str] = set()
    covered: set[str] = set()
    for case in cases:
        case_id = case.get("id")
        if not case_id or case_id in seen:
            fail(f"missing or duplicate case id: {case_id!r}")
        seen.add(case_id)

        primary = case.get("primary")
        reviewer = case.get("reviewer")
        if primary not in LENSES:
            fail(f"{case_id}: unknown primary lens {primary!r}")
        if reviewer is not None and reviewer not in LENSES:
            fail(f"{case_id}: unknown reviewer lens {reviewer!r}")
        if primary == reviewer:
            fail(f"{case_id}: primary and reviewer must differ")
        if not case.get("prompt", "").strip():
            fail(f"{case_id}: prompt is empty")
        covered.add(primary)

    missing = LENSES - covered
    if missing:
        fail(f"routing cases do not cover primary lenses: {sorted(missing)}")


def main() -> None:
    validate_manifest()
    validate_cases()
    print("Route Reasoning package is valid.")


if __name__ == "__main__":
    main()
