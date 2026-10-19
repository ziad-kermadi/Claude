# Standing settings

- Socratic plugin: configured centrally — all types enabled except Flow. Config lives in `.claude/socratic-config.json` and is copied to `~/.claude/` by a SessionStart hook. Never run the socratic init flow or ask which types to enable; if the plugin prompts for first-run setup, write that config and carry on.
- Subagents: always Haiku; Opus orchestrates.
- Handoff files: after reading a handoff file (e.g. `handoff-*.md`, `memory/HANDOFF.md`) at session start, delete it from the repo and commit the deletion. Always.
- Deck v3 (2026-10-19): user chose ~900 new cards (foundations, C++ zero-to-quant-dev course, desk-practice subdecks, weak-area top-up), difficulty tags on all cards, fix unverified items.
- Explanations (user rule, 2026-10-19): always clear and well layered — in chat: answer first, then the why, then detail; in cards: Answer → Intuition → Precise → Worked example → Trap/Where it breaks → Follow-up. Layering pass applied to new foundations, C++ and desk-practice cards; checker: `anki-deskstrat-rates-credit/tools/check_layering.py`.
- Orchestrator for the remaining v3 work was switched to Sonnet 5.5 by the user (2026-10-19); subagents remain Haiku.
- Token budget (user, 2026-10-19): minimise token usage — terse replies, no re-reads, no redundant checks or narration.
