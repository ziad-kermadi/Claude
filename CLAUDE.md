# Standing settings

- Socratic plugin: configured centrally — all types enabled except Flow. Config lives in `.claude/socratic-config.json` and is copied to `~/.claude/` by a SessionStart hook. Never run the socratic init flow or ask which types to enable; if the plugin prompts for first-run setup, write that config and carry on.
- Subagents: always Haiku; Opus orchestrates.
