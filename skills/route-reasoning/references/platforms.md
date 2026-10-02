# Portable installation

This bundle follows the open Agent Skills `SKILL.md` format. Keep the whole `route-reasoning` directory together so its references remain available.

## ChatGPT and Codex

Install the bundle as a personal skill through the product's Skills interface or supported skill-management workflow. Invoke it explicitly as `$route-reasoning`, or let the platform select it from its description.

## Claude Code

- Project scope: `.claude/skills/route-reasoning/`
- Personal scope: `~/.claude/skills/route-reasoning/`
- Explicit invocation: `/route-reasoning`

## Google Antigravity

- Workspace scope: `.agents/skills/route-reasoning/`
- Antigravity 2.0 / IDE global scope: `~/.gemini/config/skills/route-reasoning/`
- Antigravity CLI global scope: `~/.gemini/antigravity-cli/skills/route-reasoning/`
- Explicit invocation: `/route-reasoning`

Antigravity also recognizes the older `.agent/skills/` workspace location, but use `.agents/skills/` for new installations.

## Generic chat systems

If the system does not support Agent Skills, paste `SKILL.md` as a system or project instruction and include `references/lenses.md` when the model needs the detailed lens definitions. Preserve the routing, override, verification, and output-discipline sections.
