# Route Reasoning

**A portable Agent Skill that selects a useful reasoning scaffold for complex tasks.**

Route Reasoning classifies the *shape* of a task, applies one primary reasoning lens, and optionally uses a second lens as a reviewer. Users can let the skill route automatically or override the selection.

It is designed for ChatGPT/Codex, Claude Code, Google Antigravity, and other clients that support the open [Agent Skills](https://agentskills.io/) format.

## Why this exists

The same model can behave very differently depending on how a problem is structured. A calculation benefits from decomposition; a benchmark claim needs evidence checks; an architecture decision needs explicit treatment of conflicting constraints.

Route Reasoning turns those differences into a small routing system:

| Lens | Best suited to |
|---|---|
| Socrates | Ambiguity, assumptions, counterexamples |
| Aristotle | Classification, causality, system structure |
| Plato | Abstraction, invariants, reusable models |
| Descartes | Calculations, debugging, sequential implementation |
| Hume | Evidence, experiments, benchmarks, uncertainty |
| Kant | Rules, specifications, interfaces, invariants |
| Hegel | Conflicting requirements and design trade-offs |

These are operational reasoning archetypes, not attempts to reproduce the philosophers in full or imitate their voices.

## How it works

1. Parse the objective, evidence, constraints, and expected output.
2. Respect an explicit user-selected lens, or route automatically.
3. Select one primary lens based on the dominant failure risk.
4. Add at most one reviewer lens when it can catch a meaningful error.
5. Solve with the appropriate tools, sources, tests, and calculations.
6. Return the outcome and concise justification without exposing private chain-of-thought.

Typical pairs include:

- Debugging: **Descartes → Socrates**
- Implementation or calculation: **Descartes → Kant**
- Research evaluation: **Hume → Socrates**
- Architecture trade-off: **Hegel → Aristotle**
- Conceptual framework: **Plato → Aristotle**
- Root-cause analysis: **Aristotle → Hume**

## Install

Replace `Arjunrajan3759` with the account or organization hosting your fork.

### Open Agent Skills installer

```bash
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning
```

Target a supported coding agent explicitly:

```bash
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning --agent codex
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning --agent claude-code
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning --agent antigravity
```

### Manual installation

Copy `skills/route-reasoning/` into the appropriate skill directory:

| Client | Project/workspace location | Personal/global location |
|---|---|---|
| Claude Code | `.claude/skills/route-reasoning/` | `~/.claude/skills/route-reasoning/` |
| Google Antigravity | `.agents/skills/route-reasoning/` | `~/.gemini/config/skills/route-reasoning/` |

For ChatGPT and Codex, install the same folder through the product's supported Skills workflow. The runtime instructions remain in `SKILL.md`; client-specific UI metadata is optional.

## Use

Automatic routing:

```text
Use route-reasoning to evaluate whether this benchmark result is strong enough
to justify changing our production prompt.
```

Explicit override:

```text
Use Descartes as the primary lens and Kant as the reviewer.
Debug this packet parser and verify every boundary condition.
```

Compare lenses:

```text
Compare the Hume and Hegel approaches to this architecture decision.
```

Clean output:

```text
Route this automatically, but do not show the lens names.
```

## Repository layout

```text
skills/route-reasoning/   Installable runtime skill
scripts/validate.py       Dependency-free package validator
tests/routing_cases.json  Routing evaluation fixtures
.github/workflows/        Continuous validation
```

The runtime folder intentionally contains no README or contribution material. Agents load only the operational instructions and task-specific references they need.

## Validate

```bash
python3 scripts/validate.py
```

The validator checks the skill manifest, references, UI metadata, placeholder text, and routing fixtures. The cases are routing expectations for evaluation; model behavior should still be tested across multiple supported agents before a release.

## Research inspiration

This project was inspired by research on philosophy-derived prompting for chemistry reasoning, including *The Ballad of LLM Agents: Philosophical Reasoning for Chemistry* ([DOI: 10.1088/2632-2153/ae792d](https://doi.org/10.1088/2632-2153/ae792d)). Route Reasoning generalizes the idea into a domain-independent router with explicit overrides and reviewer checks.

The project is independent, is not affiliated with the paper's authors or publishers, and does not claim that a reasoning lens improves every model or task.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing routing behavior or adding a lens. New behavior should include evaluation fixtures and should preserve the skill's verification and chain-of-thought safeguards.

## License

[MIT](LICENSE) © 2026 Arjun K Rajan
