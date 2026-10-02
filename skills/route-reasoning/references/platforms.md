# Portable installation

This bundle follows the open Agent Skills `SKILL.md` format. Keep the whole `route-reasoning` directory together so its references remain available.

## ChatGPT

Install the ZIP through ChatGPT's available Skills workflow. Invoke it natively with `@route-reasoning`, or let ChatGPT select it automatically when Skills are available and enabled. `/route-reasoning` is a portable textual convention, not a native ChatGPT slash command.

## Claude Chat

Upload the ZIP through **Customize > Skills** and enable it. Claude Chat can select the skill automatically from its description. `/route-reasoning` is a textual convention, not a native Claude Chat slash command or autocomplete entry.

## Codex

Install the bundle through the supported Skills workflow or the Open Agent Skills installer. Invoke it explicitly as `$route-reasoning`, or let the platform select it from its description.

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

## OpenCode

**Status: unverified/community testing needed.** This repository does not yet document a verified OpenCode installation path or native invocation. Preserve host-specific instructions where available, and confirm the host's own Skills support before using the portable textual convention.

## Generic chat systems

If the system does not support Agent Skills, paste `SKILL.md` as a system or project instruction and include `references/lenses.md` when the model needs the detailed lens definitions. Preserve the routing, override, verification, and output-discipline sections.
