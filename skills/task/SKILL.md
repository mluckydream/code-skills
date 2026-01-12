---
name: task
description: Task management workflow - create, update, query, archive tasks
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [workflow, tasks, productivity, project-management]
commands: ["@task"]
---

# Task Skill - Task Management

## Purpose

Provide complete task lifecycle management:
1. Create new tasks with auto-generated ID
2. Update task status and progress
3. Query and search tasks
4. Archive completed tasks

## Prerequisites

- Tasks directory structure exists (auto-created on first run)
- Task files use standard YAML frontmatter format

## Commands Overview

| Command | Description | Example |
|---------|-------------|---------|
| `@task new` | Create task | `@task new "Implement login" --priority P1` |
| `@task done` | Mark complete | `@task done TASK-001` |
| `@task progress` | Update progress | `@task progress TASK-001 60` |
| `@task block` | Mark blocked | `@task block TASK-001 "Waiting for API"` |
| `@task list` | List tasks | `@task list --today` |
| `@task show` | View details | `@task show TASK-001` |
| `@task search` | Search tasks | `@task search "auth"` |
| `@task edit` | Edit task | `@task edit TASK-001 --due 2026-01-20` |

## Task File Format

```yaml
---
id: TASK-001
title: Complete user auth module
type: task
status: in-progress
priority: P1
due: 2026-01-15
expected: 2026-01-17
tags: [feature, auth, frontend]
assignee: developer
project: my-project
estimate: 8h
actual: 6h
created: 2026-01-10
updated: 2026-01-15
---

# TASK-001: Complete user auth module

## Description
Implement OAuth2 login functionality

## Acceptance Criteria
- [ ] Google login works
- [ ] GitHub login works
- [ ] Token refresh mechanism

## Progress Log
- 2026-01-15: Completed Google login
```

## Command: @task new

```yaml
Syntax:
  @task new "<title>" [options]

Options:
  --priority, -p: P0 | P1 | P2 | P3 (default P2)
  --due, -d: Due date (YYYY-MM-DD or today/tomorrow/+3d)
  --expected, -e: Expected date
  --tags, -t: Comma-separated tags
  --assignee, -a: Assignee name
  --project: Project name

Auto Features:
  - Generate unique ID (TASK-XXX)
  - Auto-tag based on keywords
  - Set created/updated dates
  - Create file in {output_dir}/tasks/active/
```

## Command: @task done

```yaml
Syntax:
  @task done <TASK-ID>

Actions:
  1. Update status to "done"
  2. Set updated date to today
  3. Move to {output_dir}/tasks/done/{year}-{month}/
```

## Command: @task list

```yaml
Syntax:
  @task list [options]

Options:
  --status: Filter by status (todo, in-progress, done)
  --today: Show today's tasks
  --overdue: Show overdue tasks
  --upcoming N: Show tasks due in N days
  --project: Filter by project
  --assignee: Filter by assignee
  --priority: Filter by priority

Output:
  Grouped list with task details
```

## Output Format

### @task new

```
[DevFlow] Task Created

TASK-042: Implement user login
  Priority: P1
  Due: 2026-01-20
  Tags: feature, auth

File: .worklogs/tasks/active/TASK-042.md
```

### @task list

```
[DevFlow] Task List (active)

P0 Critical (1):
  [ ] [TASK-001] Fix production bug - Due: today

P1 High (3):
  [~] [TASK-002] API refactoring - 60% - Due: 01-17
  [ ] [TASK-003] Auth module - Due: 01-18

P2 Medium (5):
  ...

Total: 9 active tasks
```

## Metadata Schema

```yaml
id: string           # Required, e.g., TASK-001
title: string        # Required, task title
type: task           # Required, fixed value
status: enum         # Required, todo|in-progress|blocked|review|done
priority: enum       # Required, P0|P1|P2|P3
due: date            # Optional, due date YYYY-MM-DD
expected: date       # Optional, expected completion date
tags: array          # Optional, tag list
assignee: string     # Optional, assignee
project: string      # Optional, project name
estimate: string     # Optional, estimated time e.g., "4h" "2d"
actual: string       # Optional, actual time spent
progress: number     # Optional, 0-100 percentage
blocked_reason: str  # Optional, reason if blocked
created: date        # Auto, creation date
updated: date        # Auto, update date
```
