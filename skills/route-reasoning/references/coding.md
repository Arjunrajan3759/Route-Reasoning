# Coding and engineering routing

Use the repository's own instructions and verification commands first. The lenses organize the work; they do not replace inspection, tests, builds, measurements, or source documentation.

| Engineering task | Route | Required check |
|---|---|---|
| Reproduce and fix a bug | Descartes → Socrates | Reproduce first; test the suspected assumption; add or run a regression check. |
| Implement a specified feature | Descartes → Kant | Map each acceptance criterion to code and verification evidence. |
| Resolve conflicting requirements | Hegel → Kant | Document the chosen boundary or trade-off; confirm no hard constraint was violated. |
| Refactor architecture | Aristotle → Hegel | Preserve externally observable behavior; compare coupling, ownership, and failure modes. |
| Design an API or abstraction | Plato → Aristotle | Exercise the abstraction with at least two concrete cases and one awkward edge case. |
| Benchmark or optimize | Hume → Kant | Establish a baseline, control variables, report measurement uncertainty, preserve correctness. |
| Investigate flaky behavior | Hume → Descartes | Gather traces, form falsifiable hypotheses, isolate variables, reproduce under controlled conditions. |
| Review code against a spec | Kant → Socrates | Cite the exact requirement and challenge ambiguous interpretations before flagging a defect. |

## Compact execution pattern

1. Inspect relevant code, configuration, tests, and project instructions.
2. State the operational hypothesis or implementation objective.
3. Make the smallest scoped change that satisfies the task.
4. Verify with the strongest available evidence: targeted test, build, static analysis, runtime check, or benchmark.
5. Report the outcome, changed files, verification, and remaining uncertainty.
