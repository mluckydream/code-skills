---
name: wrap
description: End of day workflow - commit code, generate work log, update task status
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [workflow, daily, worklog, git, productivity]
commands: ["@wrap"]
---

# Wrap Skill - End of Day

## Purpose

Execute before leaving work to:
1. Check uncommitted code status
2. Generate commit suggestions following Conventional Commits
3. Compile today's work into work log
4. Update task status, archive completed tasks

## Prerequisites

- Git repository initialized
- Worklogs directory exists (auto-created on first run)
- Tasks directory exists (auto-created on first run)

## Execution Steps

### Step 1: Check Code Status

```yaml
Checks:
  1. Uncommitted changes:
     git status --porcelain
  
  2. Unpushed commits:
     git log origin/main..HEAD --oneline
  
  3. Current branch:
     git branch --show-current

Output Categories:
  clean:
    - No uncommitted changes
    - No unpushed commits
  
  uncommitted:
    - Has unstaged or uncommitted changes
    - List changed files
  
  unpushed:
    - Has local commits not pushed
    - List commit messages
```

### Step 2: Suggest Commit Message

```yaml
Analysis:
  - Parse git diff for changed files
  - Identify change patterns

Conventional Commits Format:
  types:
    - feat: New feature
    - fix: Bug fix
    - docs: Documentation
    - style: Formatting
    - refactor: Code refactoring
    - test: Tests
    - chore: Maintenance

Output:
  - Suggested commit message
  - User can accept, modify, or skip
```

### Step 3: Generate Work Log

```yaml
Location: {output_dir}/worklogs/{year}-W{week}/{MM-DD}.md

Collect:
  - Today's git commits
  - Code stats (+/- lines)
  - Completed tasks
  - In-progress tasks
  - Today's notes

Format:
  # Work Log - YYYY-MM-DD Weekday
  
  ## Stats
  - Commits: N
  - Files: N
  - Lines: +N / -N
  
  ## Commits
  - hash message
  
  ## Completed
  - [TASK-ID] title
  
  ## In Progress
  - [TASK-ID] title (progress%)
  
  ## Notes
  - note content
```

### Step 4: Archive Completed Tasks

```yaml
Action:
  Move completed tasks from:
    {output_dir}/tasks/active/
  To:
    {output_dir}/tasks/done/{year}-{month}/

Condition:
  status == "done" AND updated == today
```

## Output Format

```
[DevFlow] Wrap (2026-01-15)

Code Status:
  - Branch: main
  - [ok] All committed
  - [!] 2 unpushed commits

Today's Stats:
  - Commits: 5
  - Files: 12
  - Lines: +234 / -89

Completed (3):
  [x] [TASK-001] User auth module
  [x] [TASK-015] PR Review

In Progress (1):
  [~] [TASK-002] API refactoring (60%)

---
Work log generated: .worklogs/worklogs/2026-W03/01-15.md
Next: Consider running `git push`
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--no-commit` | Skip commit suggestions | false |
| `--no-archive` | Skip task archiving | false |
| `--push` | Auto push after commit | false |

## Examples

```bash
@wrap                    # Full workflow
@wrap --no-commit        # Skip commit step
@wrap --push             # Include push step
```
