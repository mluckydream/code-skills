---
name: spec
description: Requirements analysis - ensures completeness and clarity before design
version: 1.0.0
author: mluckydream
dependencies: []
platform: [claude, cursor, claude-code]
tags: [development, analysis, requirements, validation]
commands: ["@spec"]
---

# Spec Skill - Requirements Analysis

## Purpose

Analyze user requirements to ensure completeness and clarity before proceeding with solution design. Validates that all necessary information is present and scores requirement quality on a 10-point scale.

## Prerequisites

- User has provided an initial requirement or request
- Project context is available (codebase or knowledge base)
- File system access is available for reading project files

## Execution Steps

### Phase A: Initial Analysis

#### 1. Acquire Project Context

```yaml
Strategy: Knowledge base first, then codebase scan

If knowledge base exists:
  - Read project.md for overview
  - Read relevant wiki/*.md for module details
  - Extract: Tech stack, architecture, conventions

If knowledge base missing:
  - Scan codebase structure
  - Identify: Languages, frameworks, patterns
  - Extract: Entry points, key modules, dependencies
```

#### 2. Requirement Scoring

```yaml
Scoring Dimensions (10 points total):

1. Goal Clarity (0-3 points):
   - 3: Specific, measurable objective clearly stated
   - 2: General objective with some specifics
   - 1: Vague objective, needs clarification
   - 0: No clear objective

2. Expected Results (0-3 points):
   - 3: Success criteria and deliverables well-defined
   - 2: Some expected outcomes mentioned
   - 1: Vague expectations
   - 0: No expected results stated

3. Scope Boundaries (0-2 points):
   - 2: Clear boundaries, what's in/out of scope
   - 1: Some scope indication
   - 0: Open-ended, no boundaries

4. Constraints (0-2 points):
   - 2: Time, performance, or business constraints stated
   - 1: Some constraints mentioned
   - 0: No constraints specified

Threshold: Score >= 7 to proceed to @arch
```

### Phase B: Detailed Analysis

#### 3. Extract Objectives and Criteria

```yaml
Objectives:
  - Primary: [Main goal]
  - Secondary: [Supporting goals]

Success Criteria:
  - Functional: [What it must do]
  - Non-functional: [Performance, security, etc.]
  - Acceptance: [How to verify success]

Constraints:
  - Technical: [Technology limitations]
  - Business: [Business rules]
  - Time: [Deadlines]
```

## Output Format

### Success (Score >= 7)

```
[DevFlow] Spec Complete

- Score: 8/10
- Goal: Implement OAuth2 authentication for Google and GitHub
- Key Requirements:
  1. Support Google and GitHub OAuth2 providers
  2. Include login, logout, and session management
  3. Integrate with existing user database schema
- Constraints: Must maintain backward compatibility

---
Next: Run @arch to design solution
```

### Needs Clarification (Score < 7)

```
[DevFlow] Spec Needs Clarification

Current score: 5/10

Missing information:
1. Which specific modules need this feature?
2. What are your success metrics?
3. Are there time constraints?

---
Next: Please provide details, or "continue" to proceed anyway
```

## Examples

```bash
@spec "Add user authentication with OAuth2"
@spec "Fix the login page performance issue"
@spec "Refactor the API layer for better maintainability"
```
