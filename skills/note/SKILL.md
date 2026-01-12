---
name: note
description: Quick notes workflow - capture ideas, issues, inspirations
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [workflow, memo, notes, productivity]
commands: ["@note"]
---

# Note Skill - Quick Notes

## Purpose

Provide quick capture functionality:
1. Rapidly capture ideas, issues, inspirations during work
2. Auto-organize by date
3. Support tag classification and search
4. Convert to formal tasks when needed

## Prerequisites

- Memos directory exists (auto-created on first run)

## Commands Overview

| Command | Description | Example |
|---------|-------------|---------|
| `@note` | Quick record | `@note "Found Redis issue"` |
| `@note list` | List records | `@note list --today` |
| `@note search` | Search records | `@note search "redis"` |
| `@note to-task` | Convert to task | `@note to-task NOTE-001` |

## Command: @note (Quick Record)

```yaml
Syntax:
  @note "<content>" [options]

Options:
  --tags, -t: Tag list, comma-separated
  --type: idea | todo | bug | question | note (default: auto-detect)

Execution:
  1. Determine storage location:
     {output_dir}/memos/{year}-{month}/{day}.md
  
  2. Generate unique ID:
     NOTE-{timestamp}
  
  3. Auto-detect type from content:
     - "idea:" prefix -> idea
     - "bug:" prefix -> bug
     - "todo:" prefix -> todo
     - "?" or "why/how" -> question
     - default -> note
  
  4. Append to daily memo file
```

## Command: @note list

```yaml
Syntax:
  @note list [options]

Options:
  --today: Today's notes
  --week: This week's notes
  --month: This month's notes
  --type: Filter by type

Output:
  Chronological list with types and tags
```

## Command: @note to-task

```yaml
Syntax:
  @note to-task <NOTE-ID> [task options]

Actions:
  1. Read note content
  2. Create task file with note as description
  3. Mark note as converted
  4. Link task to original note
```

## Note File Format

```markdown
# Notes - 2026-01-15

## 10:30 [idea] NOTE-001
Found Redis issue - connection pool too small

#performance #redis

---

## 14:22 [todo] NOTE-002
Check log rotation config tomorrow

#ops

---

## 16:45 [bug] NOTE-003
User session expires unexpectedly

#auth #bug

---
```

## Output Format

### @note (record)

```
[DevFlow] Note Recorded

[idea] NOTE-003 [16:45]
  Redis connection pool optimization idea

File: .worklogs/memos/2026-01/15.md
```

### @note list --today

```
[DevFlow] Today's Notes (2026-01-15)

10:30 [idea] [NOTE-001] Redis pool optimization
      #performance #redis

14:22 [todo] [NOTE-002] Check log config
      #ops

16:45 [bug] [NOTE-003] Session expiry issue
      #auth #bug

Total: 3 notes
```

## Note Types

| Type | Marker | Trigger Prefixes |
|------|--------|------------------|
| idea | [idea] | idea:, thought: |
| todo | [todo] | todo:, reminder: |
| bug | [bug] | bug:, issue: |
| question | [?] | ?, why, how |
| note | [note] | (default) |

## Auto-Tagging

Notes support automatic tagging based on content keywords:

| Keywords | Auto Tag |
|----------|----------|
| redis, cache, memory | #cache |
| api, endpoint, rest | #api |
| auth, login, session | #auth |
| test, spec, coverage | #test |
| perf, slow, optimize | #performance |
