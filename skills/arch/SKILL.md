---
name: arch
description: Architecture design - creates solution design and implementation plan
version: 1.0.0
author: mluckydream
dependencies: [spec]
platform: [claude, cursor, claude-code]
tags: [development, design, architecture, planning]
commands: ["@arch"]
---

# Arch Skill - Solution Design

## Purpose

Create solution architecture and detailed implementation plans based on analyzed requirements. Generates multiple solution options, facilitates user selection, and produces a complete solution package.

## Prerequisites

- Requirements analysis completed (score >= 7) via @spec
- Project context is available
- User requirements are clear and validated

## Execution Steps

### Phase 1: Solution Generation

#### 1. Determine Complexity

```yaml
Complexity Levels:
  - Simple: 1-2 files, single module
  - Moderate: 3-5 files, 1-2 modules
  - Complex: 6-10 files, multiple modules
  - Very Complex: >10 files, system-wide changes
```

#### 2. Generate Options

```yaml
Generate 2-3 solution approaches:

For each solution:
  1. High-level approach
  2. Key technologies/patterns
  3. Pros and cons
  4. Estimated effort
  5. Risk level

Solution Types:
  - Minimal: Simplest approach, least changes
  - Balanced: Good trade-off (recommended)
  - Comprehensive: Full-featured, more complex
```

### Phase 2: Planning

#### 3. Create Solution Package

```yaml
Package Structure:
  plan/YYYYMMDDHHMM_<feature>/
    |- why.md       # Rationale and context
    |- how.md       # Architecture and approach
    |- task.md      # Detailed task breakdown

Example: plan/202601151430_oauth2-auth/
```

#### 4. Generate Documents

```yaml
why.md:
  - Problem Statement
  - Requirements Summary
  - Solution Rationale
  - Expected Outcomes

how.md:
  - Architecture Overview
  - Technical Approach
  - File Changes
  - Testing Strategy
  - Risk Mitigation

task.md:
  - Preparation tasks
  - Implementation tasks
  - Testing tasks
  - Documentation tasks
```

## Output Format

### Solution Options

```
[DevFlow] Arch Design

Generated 3 solutions for: OAuth2 Authentication

+-----------------------------------------------+
| Option 1: Minimal                             |
| Effort: ~8h | Risk: Low                       |
| Use existing library with minimal config      |
+-----------------------------------------------+

+-----------------------------------------------+
| Option 2: Balanced [RECOMMENDED]              |
| Effort: ~16h | Risk: Medium                   |
| Custom implementation with library support    |
+-----------------------------------------------+

+-----------------------------------------------+
| Option 3: Comprehensive                       |
| Effort: ~40h | Risk: High                     |
| Full auth system with SSO, MFA, audit         |
+-----------------------------------------------+

---
Next: Select option (1/2/3)
```

### Design Complete

```
[DevFlow] Arch Complete

- Solution: Balanced OAuth2 implementation
- Package: plan/202601151430_oauth2-auth/
- Effort: 16 hours
- Tasks: 24 tasks across 5 categories

---
Created:
  - plan/202601151430_oauth2-auth/why.md
  - plan/202601151430_oauth2-auth/how.md
  - plan/202601151430_oauth2-auth/task.md

Next: Run @craft to implement
```

## Examples

```bash
@arch                           # Design after @spec
@arch "Real-time notifications" # Direct design
```
