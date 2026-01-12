---
name: flow
description: Full development flow - spec -> arch -> dev in one command
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [development, automation, full-flow]
commands: ["@flow"]
---

# Flow Skill - Full Development Flow

## Purpose

Execute the complete development workflow in one command:

```
@flow "feature"
   |
   +-- @spec (Analysis)      Analyze requirements, score completeness
   |
   +-- @arch (Design)        Generate solutions, create plan
   |
   +-- @dev (Implementation) Execute tasks, run tests
```

**Use when**: You have a clear requirement and trust the AI to make decisions.

## What Flow Does

### Step 1: @spec - Requirements Analysis
- Scores your requirement (0-10 points)
- Extracts objectives, constraints, success criteria
- Pauses if score < 7 (asks for clarification)

### Step 2: @arch - Solution Design  
- Generates 2-3 solution options
- Auto-selects the recommended (balanced) approach
- Creates plan package: `plan/YYYYMMDDHHMM_feature/`
  - `why.md` - Rationale
  - `how.md` - Architecture
  - `task.md` - Task breakdown

### Step 3: @dev - Code Implementation
- Executes tasks from `task.md`
- Runs quality checks (lint, type, tests)
- Reports progress and summary

## Prerequisites

- Clear, well-defined requirement
- Project context available
- Clean git working directory recommended

## Behavior

### Automatic Decisions

```yaml
@flow makes these decisions automatically:
  - Requirement score < 7: Pause, ask for clarification
  - Solution selection: Pick recommended option
  - Task execution: Proceed without confirmation
  - Test failures: Report and pause
  - Conflicts: Report and pause
```

### Pause Points

The flow pauses when:
- Requirements unclear (score < 7)
- High risk detected
- Tests fail
- Merge conflicts occur

## Output Format

### Success

```
[DevFlow] Flow Complete

Feature: OAuth2 Authentication

Execution Summary:
  - @spec: Score 9/10 [ok]
  - @arch: Balanced approach selected [ok]
  - @dev: 24/24 tasks completed [ok]

Package: plan/202601151430_oauth2-auth/

Changes:
  - 15 files modified
  - 3 files created
  - +456 / -23 lines
  - 8 tests added

---
Next: Test the feature, then @wrap
```

### Paused

```
[DevFlow] Flow Paused

Feature: OAuth2 Authentication

Paused at: @spec (Requirements)

Reason: Requirement score 5/10

Missing information:
1. Which OAuth providers to support?
2. Session expiration policy?

---
Next: Provide details, then run @flow again
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--plan-only` | Stop after @arch | false |
| `--confirm` | Require confirmation at each step | false |
| `--dry-run` | Show plan without executing | false |

## Examples

```bash
@flow "Add OAuth2 login with Google and GitHub"
@flow "Fix login page performance" --confirm
@flow "Refactor API layer" --plan-only
```

## Comparison with Other Commands

| Command | What it does | Use when |
|---------|-------------|----------|
| `@spec` | Analysis only | Need to clarify requirements first |
| `@arch` | Design only | Want to review plan before coding |
| `@dev` | Execute only | Have existing plan |
| `@flow` | All three | Clear requirement, trust AI |

## Best Practices

1. **Clear requirements** - The clearer your request, the better the result
2. **Review first time** - Use `--confirm` for new types of features
3. **Test after** - Always test the implementation
4. **Use @wrap** - End your session properly to log work
