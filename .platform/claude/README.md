# DevFlow for Claude Code

Integration guide for using DevFlow skills with Claude Code.

## Installation

Add to your `CLAUDE.md`:

```markdown
## DevFlow Skills

Load skills from `skills/devflow/`:
- standup - Daily startup
- wrap - End of day
- note - Quick notes
- task - Task management
- spec/arch/dev/flow - Development

See [DevFlow SKILL.md](skills/devflow/SKILL.md) for complete documentation.
```

## Usage

Claude Code understands natural language:

```
"开始工作" or "standup"  → Daily startup
"下班" or "wrap"         → End of day
"分析需求" or "spec"     → Requirements analysis
```

## Learn More

- [DevFlow README](../../README.md) - Complete documentation
- [DevFlow SKILL.md](../../SKILL.md) - Skill definitions
- [DevFlow CHECKLIST.md](../../CHECKLIST.md) - Pre-delivery checklist
