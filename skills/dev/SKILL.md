---
name: dev
description: Code implementation - executes solution plan with quality checks
version: 1.0.0
author: mluckydream
dependencies: [spec, arch]
platform: [claude, cursor, claude-code]
tags: [development, implementation, coding]
commands: ["@dev"]
---

# Dev Skill - Code Implementation

## Purpose

Execute the solution plan created by @arch, implementing code changes with quality checks, testing, and documentation updates.

## Prerequisites

- Solution design completed via @arch
- Solution package exists in `plan/` directory
- Project context and codebase access available

## Execution Steps

### Phase 1: Preparation

#### 1. Load Solution Package

```yaml
Read from plan/{package}/:
  - task.md: Get task list
  - how.md: Get implementation details
  - why.md: Understand context

Validate:
  - All files exist
  - Tasks are parseable
  - No blocking issues
```

#### 2. Pre-flight Checks

```yaml
Checks:
  - Git status (clean working directory)
  - Dependencies installed
  - Tests passing (if exist)
  - No conflicting changes
```

### Phase 2: Implementation

#### 3. Execute Tasks

```yaml
For each task in task.md:
  1. Read task description
  2. Implement changes
  3. Mark task complete [x]
  4. Run relevant tests
  5. Continue to next task

Task Status:
  - [ ] Pending
  - [x] Completed
  - [!] Failed
  - [-] Skipped
```

#### 4. Quality Checks

```yaml
After implementation:
  - Lint check
  - Type check
  - Unit tests
  - Integration tests (if applicable)
```

### Phase 3: Finalization

#### 5. Update Documentation

```yaml
Updates:
  - Inline code comments
  - API documentation
  - README updates (if needed)
  - Knowledge base updates
```

#### 6. Generate Summary

```yaml
Summary includes:
  - Tasks completed
  - Files changed
  - Lines added/removed
  - Tests added
  - Next steps
```

## Output Format

### In Progress

```
[DevFlow] Dev In Progress

Task 5/24: Implement OAuth callback handler

Current:
  - Creating src/auth/callback.ts
  - Adding route handler

---
Progress: ========---------- 21%
```

### Complete

```
[DevFlow] Dev Complete

Summary:
  - Tasks: 24/24 completed
  - Files: 12 changed, 3 created
  - Lines: +456 / -23
  - Tests: 8 added, all passing

Changes:
  - src/auth/oauth.ts (new)
  - src/auth/callback.ts (new)
  - src/auth/session.ts (new)
  - src/routes/auth.ts (modified)
  - src/db/schema.ts (modified)
  ...

---
Next: Test the implementation, then @wrap
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dry-run` | Show plan without executing | false |
| `--skip-tests` | Skip test execution | false |
| `--continue` | Resume from last task | false |

## Examples

```bash
@dev                    # Execute latest plan
@dev --dry-run          # Preview changes
@dev --continue         # Resume interrupted work
```
