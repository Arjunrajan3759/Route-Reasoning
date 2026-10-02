---
name: route-reasoning
description: Selects and applies a fitting structured reasoning lens to complex tasks, with optional user override and a compact verification pass. Use for ambiguous or multi-step questions, calculations, debugging, architecture and design trade-offs, research or evidence synthesis, root-cause analysis, specification and constraint checking, conceptual modeling, or explicit requests to reason using Socratic, Aristotelian, Platonic, Cartesian, Humean, Kantian, or Hegelian methods. Do not trigger for trivial lookups, simple transformations, or purely stylistic writing unless explicitly requested.
---

# Route Reasoning

Route a task to one primary reasoning lens and, only when useful, one reviewer lens. Treat the lenses as operational scaffolds rather than historical impersonations.

## Workflow

1. Parse the user's actual objective, constraints, supplied evidence, and required output.
2. Honor an explicit lens request. Otherwise select a primary lens using the routing table below.
3. Add at most one reviewer lens when the task has a meaningful failure mode that a second lens can catch.
4. Solve the task using the primary lens. Use tools, tests, calculations, sources, or artifacts whenever the task requires them; a reasoning lens never replaces verification.
5. Run the reviewer check, if selected, and correct the answer before responding.
6. Lead with the outcome. Give concise supporting rationale, assumptions, evidence, and checks rather than hidden chain-of-thought.

When explicitly invoked, mention the selected lens or pair in one short line unless the user asks for a clean answer. When triggered implicitly, omit the label unless it materially helps the user evaluate the result.

## Routing table

| Task shape | Primary lens | Operational behavior |
|---|---|---|
| Ambiguous premise, unclear request, risky assumption | Socrates | Clarify terms, test assumptions, seek counterexamples, identify what must be true. |
| Taxonomy, root cause, system structure, causal explanation | Aristotle | Classify entities, identify properties and causes, connect parts to the whole. |
| Abstraction, reusable model, analogy, general design pattern | Plato | Remove incidental detail, expose invariants, symmetries, and transferable structure. |
| Calculation, algorithm, debugging, implementation sequence | Descartes | Decompose, order dependencies, solve from stable premises, verify each boundary. |
| Evidence, experiment, benchmark, uncertainty, recommendation | Hume | Separate observation from inference, weigh evidence, calibrate confidence, seek disconfirmation. |
| Specification, compliance, invariants, interfaces, acceptance criteria | Kant | Make rules and preconditions explicit, check consistency, reject invalid transitions. |
| Conflicting requirements, architectural trade-off, competing explanations | Hegel | State the tension fairly, preserve valid parts of both sides, form and test a synthesis. |

If two lenses seem equally plausible, choose based on the dominant failure risk, not on the topic name. Read `references/lenses.md` when the distinction is unclear or a user requests a specific lens.

## Reviewer selection

Use no reviewer for straightforward tasks. Otherwise choose one:

- **Socrates** to challenge hidden assumptions or an underspecified request.
- **Kant** to check requirements, units, types, invariants, interfaces, or acceptance criteria.
- **Hume** to check whether claims are supported by evidence and uncertainty is calibrated.
- **Hegel** to test whether a proposed solution ignores a serious competing constraint.

Common pairs:

- Calculation or code implementation: **Descartes → Kant**
- Debugging: **Descartes → Socrates**
- Research synthesis or recommendation: **Hume → Socrates**
- Requirements or compliance: **Kant → Socrates**
- Architecture trade-off: **Hegel → Aristotle**
- Conceptual framework: **Plato → Aristotle**
- Root-cause analysis: **Aristotle → Hume**

## Overrides

Accept natural-language overrides such as:

- `Use Socrates.`
- `Route this automatically.`
- `Use Descartes, then review with Kant.`
- `Do not show the lens names.`
- `Compare how Hume and Kant would approach this.`

If the requested lens is poorly matched, follow it but briefly warn about the likely blind spot and use ordinary factual verification. Never silently replace an explicit user choice.

## Output discipline

- Do not role-play a philosopher's voice unless the user explicitly asks for it.
- Do not fabricate quotations, historical doctrine, evidence, or facts to fit a lens.
- Do not claim that a lens guarantees accuracy or general intelligence.
- Keep internal reasoning private. Provide conclusions, key assumptions, concise derivations, evidence, tests, and uncertainty sufficient for evaluation.
- Preserve the platform's safety rules, project instructions, and domain-specific procedures.
- Prefer a direct answer over displaying the entire routing process.

For complex coding tasks, read `references/coding.md`. For installation or sharing across supported agents, read `references/platforms.md`.
