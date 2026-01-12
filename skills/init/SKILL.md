---
name: init
description: Project initialization - setup DevFlow system and generate standards
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [workflow, init, setup, standards]
commands: ["@init"]
---

# Init Skill - Project Initialization

## Purpose

Initialize a new project with the DevFlow system, scan codebase to generate project standards.

## Commands

| Command | Description |
|---------|-------------|
| `@init` | Initialize workflow directories |
| `@init scan` | Scan codebase to generate standards |
| `@init scan --type <type>` | Generate specific type standards (frontend/backend) |

## Execution Steps

### @init (Initialize Directories)

1. Check if workflow output directory exists
2. Create directory structure (based on config `output_dir`, default `.worklogs/`):
   ```
   {output_dir}/
   |- tasks/
   |   |- active/
   |   |- backlog/
   |   |- done/
   |   |- recurring/
   |- memos/
   |- worklogs/
   ```
3. Add `{output_dir}/` to `.gitignore`
4. Create `.cursorrules` or `.cursor/rules/` entry if not exists

### @init scan (Scan & Generate Standards)

1. Analyze project tech stack:
   - Detect `package.json` -> Frontend framework (React, Vue, etc.)
   - Detect `requirements.txt` / `pyproject.toml` -> Python backend
   - Detect config files (tsconfig, eslint, etc.)

2. Scan code patterns:
   - Component structure and naming conventions
   - API route organization
   - State management patterns
   - Type definition styles

3. Generate standard docs to `docs/standards/`:
   - `code-style.md` - Code style guide
   - `component-architecture.md` - Component architecture
   - `python-backend.md` - Backend conventions (if applicable)

## Output Format

```
[DevFlow Init] Project Initialized

Directory Structure:
  [ok] {output_dir}/tasks/
  [ok] {output_dir}/memos/
  [ok] {output_dir}/worklogs/

Detected Tech Stack:
  - Frontend: Next.js + TypeScript
  - Backend: Python + FastAPI

Generated Standards:
  [ok] docs/standards/code-style.md
  [ok] docs/standards/python-backend.md

---
DevFlow system ready!
```

## Configuration

Output directory can be configured in `config/skills-config.yaml`:

```yaml
workflow:
  output_dir: .worklogs    # Can be any path
  worklogs_dir: worklogs
  tasks_dir: tasks
  memos_dir: memos
```

## Notes

- All runtime data (tasks, memos, worklogs) are stored in `{output_dir}/`
- `{output_dir}/` is automatically added to `.gitignore`
- Skill definitions remain in `devflow/` and can be shared across projects
