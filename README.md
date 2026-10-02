# Route Reasoning

**A portable Agent Skill that selects a useful reasoning scaffold for complex tasks.**

Route Reasoning classifies the *shape* of a task, applies one primary reasoning lens, and optionally uses a second lens as a reviewer. Users can let the skill route automatically or override the selection.

It is designed for ChatGPT, Claude Chat, Codex, Claude Code, Google Antigravity, and other clients that support the open [Agent Skills](https://agentskills.io/) format.

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

### Compatibility

| Platform | Installation method | Native explicit invocation | Portable textual invocation | Automatic invocation | Notes |
|---|---|---|---|---|---|
| ChatGPT | Download the release ZIP and upload it through the available Skills workflow. | `@route-reasoning` | `/route-reasoning <request>` convention; not a native ChatGPT slash command. | Yes, when Skills are available and enabled. | Availability and upload permissions vary by plan, workspace, and surface. |
| Claude Chat | Upload the release ZIP through **Customize > Skills**, then enable it. | No repository-verified native command. | `/route-reasoning <request>` convention; not a native Claude Chat slash command. | Yes, from the skill description. | Do not expect slash-command autocomplete. |
| Codex | Open Agent Skills installer or the product Skills workflow. | `$route-reasoning` | `/route-reasoning <request>` convention. | Yes. | The bundle includes Codex UI metadata in `agents/openai.yaml`. |
| Claude Code | Open Agent Skills installer or the documented project/personal skill paths. | `/route-reasoning` | `/route-reasoning <request>` | Yes, when the host selects the skill. | The native and portable forms use the same text. |
| Google Antigravity | Open Agent Skills installer or the documented workspace/global skill paths. | `/route-reasoning` | `/route-reasoning <request>` | Yes, when the host selects the skill. | The native and portable forms use the same text. |
| OpenCode | No repository-verified installation method is currently documented. | No repository-verified native command. | Use the portable convention only after confirming that the host has loaded the skill. | Host-dependent. | **Unverified/community testing needed**; no OpenCode-specific behavior is claimed here. |

### ChatGPT

1. Download `route-reasoning-skill.zip` from the [latest GitHub Release](https://github.com/Arjunrajan3759/Route-Reasoning/releases/latest).
2. Upload or install it through ChatGPT's available Skills workflow.
3. If installation through a conversation is supported for your workspace, attach the ZIP and ask ChatGPT to install the skill.
4. Open a new conversation if the newly installed skill is not immediately visible.

ChatGPT's native explicit form is `@route-reasoning`; automatic invocation remains available. `/route-reasoning` is a portable textual convention after installation, not a native ChatGPT slash command. See OpenAI's [Skills documentation](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) for availability, permissions, and upload details.

### Claude Chat

1. Download `route-reasoning-skill.zip` from the latest GitHub Release.
2. Open Claude.
3. Go to **Customize > Skills**.
4. Add or upload the ZIP.
5. Enable the skill.
6. Test a prompt and confirm Claude loads it.

Claude Chat should automatically invoke the skill from its description. `/route-reasoning` is a textual activation convention, not a native Claude Chat slash command, and it is not expected to appear in autocomplete.

### Coding agents

#### Open Agent Skills installer

```bash
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning
```

Target a supported coding agent explicitly:

```bash
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning --agent codex
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning --agent claude-code
npx skills@latest add <github-user>/route-reasoning --skill route-reasoning --agent antigravity
```

#### Manual installation

Copy `skills/route-reasoning/` into the appropriate skill directory:

| Client | Project/workspace location | Personal/global location |
|---|---|---|
| Claude Code | `.claude/skills/route-reasoning/` | `~/.claude/skills/route-reasoning/` |
| Google Antigravity | `.agents/skills/route-reasoning/` | `~/.gemini/config/skills/route-reasoning/` |

For Codex, use `$route-reasoning` as the existing native explicit invocation. For Claude Code and Antigravity, `/route-reasoning` is the documented native explicit invocation; it also matches the portable textual convention. The runtime instructions remain in `SKILL.md`; Codex-specific UI metadata is in `agents/openai.yaml`.

**OpenCode status: unverified/community testing needed.** No OpenCode installation command or native invocation has been verified in this repository. Preserve host-specific instructions where available, and confirm the host's own Skills support before using the portable textual convention there.

## Use

### ChatGPT examples

```text
@route-reasoning Compare a monolithic design with microservices.

@route-reasoning Use Descartes, then review with Kant. Debug this API race condition.
```

### Claude Chat examples

```text
/route-reasoning Should this project use an FPGA or an ASIC?

/route-reasoning --lens hume Evaluate the evidence for this claim.

/route-reasoning --lens descartes --reviewer kant Debug this state machine.
```

### Portable and native examples

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

## Update or uninstall

### Update

Build or download the newer `route-reasoning-skill.zip`, then use the platform's update or upload workflow to replace the installed bundle. For manual coding-agent installs, replace the existing `route-reasoning/` skill directory with the newer bundle and restart or open a new session if the host does not reload skills immediately.

### Uninstall

Use the platform's Skills manager to disable or remove the installed skill. For a manual coding-agent install, remove only that platform's `route-reasoning/` skill directory. Do not remove a broader skills directory.

### Security

Review third-party skills before enabling them. Skills can contain instructions, supporting files, and executable scripts; use only sources you trust and inspect updates before replacing an installed version.

### Troubleshooting

**Skill installed but not triggered:** Confirm it is enabled, start a new conversation or restart the coding agent, and use a task that matches the skill description. Try the platform's native explicit form where one is documented. Workspace permissions or product availability can also prevent skills from loading.

**`/route-reasoning` was treated as plain text:** In ChatGPT and Claude Chat, it is a textual activation convention rather than a native slash command. Use `@route-reasoning` in ChatGPT, or rely on automatic selection in Claude Chat. In coding agents, confirm the skill was installed in the documented location and that the host recognizes its native command.

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
python3 -m unittest discover -s tests -p "test_*.py"
```

The validator checks the skill manifest, references, UI metadata, placeholder text, and routing fixtures. The regression suite checks the command contract, platform documentation, and generated distribution archive. The cases are routing expectations for evaluation; model behavior should still be tested across multiple supported agents before a release.

## Build distribution

Build a deterministic runtime-only ZIP from the canonical skill directory:

```bash
python3 scripts/build_dist.py
```

This creates `dist/route-reasoning-skill.zip` with one `route-reasoning/` top-level directory. The build validates the manifest and local references before packaging, then inspects the finished archive for required runtime files and repository-only content.

## Releases

Use [semantic versioning](https://semver.org/): tag releases as `vMAJOR.MINOR.PATCH`. Increment MAJOR for incompatible changes to the skill contract, MINOR for compatible features, and PATCH for compatible fixes or documentation-only corrections.

Before creating a tag, update the version and release date in `CITATION.cff` when applicable, then run the validation, regression-test, and build commands above. Pushing a `v*` tag runs the same checks in GitHub Actions and, only after they pass, publishes `route-reasoning-skill.zip` and its SHA-256 checksum to the matching GitHub Release. This workflow does not change the current version automatically.

## Research inspiration

This project was inspired by research on philosophy-derived prompting for chemistry reasoning, including *The Ballad of LLM Agents: Philosophical Reasoning for Chemistry* ([DOI: 10.1088/2632-2153/ae792d](https://doi.org/10.1088/2632-2153/ae792d)). Route Reasoning generalizes the idea into a domain-independent router with explicit overrides and reviewer checks.

The project is independent, is not affiliated with the paper's authors or publishers, and does not claim that a reasoning lens improves every model or task.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing routing behavior or adding a lens. New behavior should include evaluation fixtures and should preserve the skill's verification and chain-of-thought safeguards.

## License

[MIT](LICENSE) © 2026 Arjun K Rajan
