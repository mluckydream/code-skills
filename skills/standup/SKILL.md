---
name: standup
description: Daily startup workflow - sync code, scan tasks, generate today's overview
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [workflow, daily, tasks, productivity]
commands: ["@standup"]
---

# Standup Skill - Daily Startup

## Purpose

Execute at the start of each workday to:
1. Switch to main branch and pull latest code
2. Scan all markdown files for YAML frontmatter metadata
3. Summarize tasks due today, in progress, and upcoming
4. Generate `today.md` task overview file

## Prerequisites

- Git repository initialized
- Tasks directory exists (auto-created on first run)
- Worklogs directory exists (auto-created on first run)

## Execution Steps

### Step 1: Git Sync

```yaml
Actions:
  1. Check uncommitted changes
     - Has changes: Prompt to stash or commit, allow skip sync
     - No changes: Continue
  
  2. Execute sync
     git fetch --all
     git checkout main
     git pull origin main
  
  3. Get latest commit info
     git log -1 --pretty=format:"%h %s"

Output:
  - Success: Show latest commit
  - Failed: Show error, continue with remaining steps

Error Handling:
  - Permission denied: Skip sync, continue workflow
  - Network timeout: Skip sync with warning
```

### Step 2: Scan Tasks

```yaml
Scan Directories:
  - {output_dir}/tasks/active/**/*.md
  - {output_dir}/tasks/backlog/**/*.md
  - {output_dir}/tasks/recurring/**/*.md

Parse YAML Frontmatter:
  required:
    - id
    - title
    - status
    - priority
  optional:
    - due
    - expected
    - tags
    - assignee
    - project

Categorization:
  today:
    condition: due == today
    marker: [!]
  
  in-progress:
    condition: status == "in-progress"
    marker: [~]
  
  overdue:
    condition: due < today AND status != "done"
    marker: [!!]
  
  upcoming:
    condition: due in next 7 days
    marker: [ ]
  
  long-term:
    condition: no due date OR due > 7 days
    marker: [ ]
```

### Step 3: Generate today.md

```yaml
Location: {output_dir}/worklogs/{year}-W{week}/today.md

Content:
  - Date and weekday
  - Git sync status
  - Categorized task lists
  - Generation timestamp
```

## Output Format

```
[DevFlow] Standup (2026-01-15 Wednesday)

Git Sync:
  - Branch: main
  - Latest: abc1234 "feat: add OAuth2 login"

Today (3):
  [ ] [TASK-001] Complete user auth module - P0 @developer
  [ ] [TASK-015] Code Review: PR #42 - P1

In Progress (2):
  [~] [TASK-002] Refactor API layer - Expected 01-17

Overdue (1):
  [!!] [TASK-005] Documentation update - 2 days overdue

This Week (4):
  [ ] [TASK-020] i18n support - 01-17

---
today.md generated: .worklogs/worklogs/2026-W03/today.md
Next: Use @task to manage tasks, or start working
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skip-sync` | Skip git sync step | false |
| `--project <name>` | Filter by project | all |
| `--assignee <name>` | Filter by assignee | all |

## Examples

```bash
@standup                        # Full workflow
@standup --skip-sync            # Skip git sync
@standup --project my-project   # Filter by project
```
