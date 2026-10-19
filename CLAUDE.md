# Standing settings

- Socratic plugin: configured centrally — all types enabled except Flow. Config lives in `.claude/socratic-config.json` and is copied to `~/.claude/` by a SessionStart hook. Never run the socratic init flow or ask which types to enable; if the plugin prompts for first-run setup, write that config and carry on.
- Subagents: always Haiku; Opus orchestrates.
- Handoff files: after reading a handoff file (e.g. `handoff-*.md`, `memory/HANDOFF.md`) at session start, delete it from the repo and commit the deletion. Always.
- Deck v3 (2026-10-19): user chose ~900 new cards (foundations, C++ zero-to-quant-dev course, desk-practice subdecks, weak-area top-up), difficulty tags on all cards, fix unverified items.
