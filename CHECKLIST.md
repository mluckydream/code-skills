# DevFlow Pre-Delivery Checklist

Use this checklist before delivering code, completing tasks, or ending your workday.

---

## Code Quality

### Testing
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Edge cases covered
- [ ] Error scenarios tested

### Code Standards
- [ ] No linting errors
- [ ] Code follows project conventions
- [ ] No commented-out code (unless documented why)
- [ ] No debug statements (console.log, print, etc.)
- [ ] No hardcoded credentials or secrets
- [ ] Environment variables used for config

### Error Handling
- [ ] Try-catch blocks for async operations
- [ ] Meaningful error messages
- [ ] Graceful degradation implemented
- [ ] User-facing errors are friendly
- [ ] Errors logged appropriately

### Performance
- [ ] No unnecessary re-renders
- [ ] Database queries optimized
- [ ] Large lists virtualized if needed
- [ ] Images optimized
- [ ] Bundle size checked

---

## Documentation

### Code Documentation
- [ ] Complex logic has comments explaining "why"
- [ ] Function/method signatures documented
- [ ] Type definitions provided
- [ ] Public APIs documented

### Project Documentation
- [ ] README updated if needed
- [ ] API documentation current
- [ ] Architecture docs reflect changes

---

## Git Operations

### Commits
- [ ] Meaningful commit messages
- [ ] Commits are atomic
- [ ] No unnecessary files committed
- [ ] No large binary files committed

### Branches
- [ ] Branch naming follows conventions
- [ ] Branch is up to date with main
- [ ] No merge conflicts

---

## Task Management

### Task Status
- [ ] Task status updated
- [ ] Related tasks linked
- [ ] Blockers documented

### Work Logs
- [ ] Work log generated (use wrap command)
- [ ] Progress documented
- [ ] Challenges noted
- [ ] Next steps outlined

---

## Quick Checklist (Minimal)

For quick tasks:

- [ ] Tests passing
- [ ] No linting errors
- [ ] Meaningful commit message
- [ ] Work log generated (wrap)
- [ ] Task status updated

---

## Usage

### Before Committing
```bash
# Review this checklist
cat CHECKLIST.md

# Run tests
npm test

# Generate work log
@wrap
```

---

## Learn More

- [DevFlow README](./README.md) - Main documentation
- [Wrap Skill](./skills/wrap/SKILL.md) - End of day workflow
