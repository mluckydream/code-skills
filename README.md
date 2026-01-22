# DevFlow

> A modular workflow system for AI coding assistants (Claude Code, Codex CLI, Cursor)

[![Skills](https://img.shields.io/badge/Skills-9-blue)]()
[![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20Codex%20%7C%20Cursor-green)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow)]()

## Why DevFlow?

AI coding assistants are powerful, but they lack **memory** and **structure**:

- **Context Loss** - AI forgets what you did yesterday, last week, or across sessions
- **Inconsistent Workflows** - No standardized process for requirements → design → implementation
- **Scattered Information** - Tasks, notes, and decisions get lost in chat history
- **Manual Tracking** - You manually create work logs, summaries, and documentation

DevFlow solves this by providing:

- **Persistent Memory** - Automatic work logs, task tracking, and project documentation
- **Structured Workflows** - Enforced spec → arch → dev flow prevents skipping steps
- **Centralized Storage** - All tasks, notes, and logs saved to `.devflow/` workspace
- **Automation** - Daily standup, end-of-day wrap, weekly summaries run automatically

**Result:** AI assistants become more reliable and effective with persistent context.

---

## What is DevFlow?

DevFlow is a **skills system** that extends AI coding assistants with structured workflows. It provides **9 skills** organized into two categories:

- **Workflow Skills** - Daily productivity routines
- **Development Skills** - End-to-end feature development

---

## Quick Start

### Daily Workflow

```bash
@standup           # Start your day - sync code & review tasks
@note "idea"       # Quick note during work
@task new "task"   # Create new task
@wrap              # End your day - commit & generate log
```

### Development Flow

```bash
@spec "requirement"   # Requirements analysis
@arch                 # Architecture design
@dev                  # Code implementation
@flow "feature"       # All-in-one: spec -> arch -> dev
```

---

## @flow - Full Development Flow

`@flow` is the **core command** of DevFlow. It executes the complete development pipeline:

```
@flow "Add user login feature"
       |
       +-- 1. @spec (Requirements Analysis)
       |       +-- Score requirement completeness (0-10)
       |       +-- Extract objectives, constraints
       |       +-- Pause if score < 7
       |
       +-- 2. @arch (Solution Design)
       |       +-- Generate 2-3 solution options
       |       +-- Auto-select recommended approach
       |       +-- Create plan package
       |
       +-- 3. @dev (Code Implementation)
               +-- Execute tasks from plan
               +-- Run quality checks
               +-- Output change summary
```

### When to Use Each Command

| Scenario | Command |
|----------|---------|
| Requirements unclear, need analysis first | `@spec` |
| Want to review plan before coding | `@spec` then `@arch` |
| Already have a plan, just implement | `@dev` |
| **Clear requirement, trust AI decisions** | `@flow` |

### @flow Examples

```bash
# Full automation
@flow "Add OAuth2 login with Google and GitHub"

# Step-by-step confirmation
@flow "Fix login page performance" --confirm

# Planning only, no implementation
@flow "Refactor API layer" --plan-only

# Preview without executing
@flow "Add dark mode" --dry-run
```

---

## Command Reference

### Workflow Commands

| Command | Description | Examples |
|---------|-------------|----------|
| `@standup` | Daily startup | `@standup` `@standup --skip-sync` |
| `@wrap` | End of day | `@wrap` `@wrap --push` |
| `@note` | Quick notes | `@note "bug: login fails"` `@note list --today` |
| `@task` | Task management | `@task new "feature"` `@task done TASK-001` |
| `@init` | Initialize project | `@init` `@init scan` |

### Development Commands

| Command | Description | Examples |
|---------|-------------|----------|
| `@spec` | Requirements analysis | `@spec "Add user auth"` |
| `@arch` | Solution design | `@arch` `@arch "notifications"` |
| `@dev` | Code implementation | `@dev` `@dev --continue` |
| `@flow` | Full automation | `@flow "feature"` `@flow "fix" --confirm` |

---

## Skills Overview

### Workflow Skills (5)

| Skill | Command | Description | Memory Tip |
|-------|---------|-------------|------------|
| **Standup** | `@standup` | Daily startup, sync & review | Standup meeting |
| **Wrap** | `@wrap` | End of day, commit & log | Wrap up |
| **Note** | `@note` | Quick notes & ideas | Take note |
| **Task** | `@task` | Task management | Task tracking |
| **Init** | `@init` | Project initialization | Initialize |

### Development Skills (4)

| Skill | Command | Description | Memory Tip |
|-------|---------|-------------|------------|
| **Spec** | `@spec` | Requirements analysis | Specification |
| **Arch** | `@arch` | Solution design | Architecture |
| **Dev** | `@dev` | Code implementation | Development |
| **Flow** | `@flow` | Full automation flow | DevFlow |

---

## Typical Daily Workflow

```
Morning:                     Evening:
+--------------+             +--------------+
|  @standup    |             |   @wrap      |
|  Sync code   |             |  Commit      |
|  See tasks   |             |  Log work    |
+--------------+             +--------------+
      |                            ^
      v                            |
+-------------------------------------+
|         During the day              |
|                                     |
|  @task new "task"   Create task     |
|  @note "idea"       Quick note      |
|  @task done ID      Complete        |
|                                     |
|  @flow "feature"    Build it!       |
+-------------------------------------+
```

---

## Directory Structure

```
devflow/
├── README.md                    # This file
├── skills/                      # 9 Skill definitions
│   ├── standup/SKILL.md         # @standup
│   ├── wrap/SKILL.md            # @wrap
│   ├── note/SKILL.md            # @note
│   ├── task/SKILL.md            # @task
│   ├── init/SKILL.md            # @init
│   ├── spec/SKILL.md            # @spec
│   ├── arch/SKILL.md            # @arch
│   ├── dev/SKILL.md             # @dev
│   └── flow/SKILL.md            # @flow
├── scripts/                     # Python automation
│   ├── standup.py
│   └── wrap.py
└── config/
    └── skills-config.yaml       # Configuration
```

---

## Installation

### For Claude Code (Global)

```bash
cp -r devflow ~/.claude/DevFlow
```

### For Codex CLI (Global)

```bash
cp -r devflow ~/.codex/DevFlow
```

### For Cursor (Project-level)

```bash
# Copy to project
mkdir -p your-project/.skills
cp -r devflow your-project/.skills/

# Create symlink for Cursor
mkdir -p your-project/.cursor/rules
ln -s ../../.skills/devflow/skills your-project/.cursor/rules/skills
```

---

## Personal Workspace

Runtime data is stored separately from skill definitions:

```
project/
├── .skills/devflow/        # Skill definitions (commit)
├── .cursor/rules/skills    # Symlink for Cursor
└── .worklogs/              # Personal data (not committed)
    ├── tasks/              # Task files
    ├── memos/              # Quick notes
    └── worklogs/           # Daily logs
```

### Configure Output Directory

Edit `config/skills-config.yaml`:

```yaml
workflow:
  output_dir: .worklogs    # Can be any path
```

---

## Platform Support

| Platform | Location | Scope |
|----------|----------|-------|
| Claude Code | `~/.claude/DevFlow/` | Global |
| Codex CLI | `~/.codex/DevFlow/` | Global |
| Cursor | `.skills/devflow/` | Project |

---

## Data Isolation

| Directory | Description | Git |
|-----------|-------------|-----|
| `devflow/` | Skill definitions | Commit |
| `.worklogs/` | Personal work data | Ignore |

---

## Learn More

Each skill has detailed documentation in its `SKILL.md` file:

- [Standup](skills/standup/SKILL.md) - Daily startup workflow
- [Wrap](skills/wrap/SKILL.md) - End of day workflow
- [Task](skills/task/SKILL.md) - Task management
- [Note](skills/note/SKILL.md) - Quick notes
- [Spec](skills/spec/SKILL.md) - Requirements analysis
- [Arch](skills/arch/SKILL.md) - Solution design
- [Dev](skills/dev/SKILL.md) - Code implementation
- [Flow](skills/flow/SKILL.md) - Full automation

---

## Contributing

1. Fork the repository
2. Create your feature branch
3. Add or modify skills in `skills/`
4. Submit a pull request
