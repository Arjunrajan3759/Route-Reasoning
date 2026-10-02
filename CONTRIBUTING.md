# Contributing

Route Reasoning should remain small, portable, and verifiable.

## Principles

- Route by task shape and dominant failure risk, not by topic keywords alone.
- Treat lenses as operational scaffolds, not philosopher impersonations.
- Keep one primary lens and at most one reviewer by default.
- Preserve explicit user overrides.
- Require ordinary evidence, tests, tools, and calculations where appropriate.
- Return concise rationale rather than private chain-of-thought.
- Avoid claims that a lens guarantees correctness or general intelligence.

## Proposing a routing change

1. Describe the failure mode the change addresses.
2. Add or update cases in `tests/routing_cases.json`.
3. Keep `SKILL.md` under 500 lines and move detailed material into `references/`.
4. Run `python3 scripts/validate.py`.
5. Test the changed skill on more than one model or agent when possible.

## Adding a lens

Add a lens only when its operational behavior is distinct from the existing seven. Define:

- the task shapes it handles;
- a five-step procedure;
- its primary blind spot;
- when it should be a primary lens or reviewer;
- at least two positive routing cases and one case where it should not be selected.

Do not add a lens solely because a historical thinker is well known.

## Pull requests

Keep pull requests focused. Include the motivation, changed routing behavior, evaluation cases, and manual test results. Avoid unrelated formatting changes to the runtime skill.
