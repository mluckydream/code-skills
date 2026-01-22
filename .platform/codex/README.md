# DevFlow for Codex CLI

Integration guide for using DevFlow skills with Codex CLI.

## Installation

Add to your Codex configuration:

```yaml
skills:
  - name: devflow
    path: skills/devflow/SKILL.md
    enabled: true
```

## Usage

```bash
codex devflow standup
codex devflow wrap
codex devflow spec "feature description"
```

## Learn More

- [DevFlow README](../../README.md) - Complete documentation
- [DevFlow SKILL.md](../../SKILL.md) - Skill definitions
- [DevFlow CHECKLIST.md](../../CHECKLIST.md) - Pre-delivery checklist
