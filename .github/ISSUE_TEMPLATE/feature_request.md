---
name: "Feature request"
about: "Propose a new feature or enhancement for pyfiles_db."
labels: ["enhancement"]
assignees: []
---

Please use this template to propose new features or enhancements. Provide clear motivation and acceptance criteria to help maintainers evaluate the request.

## 1) Summary
_A short, descriptive title and a one-paragraph summary of the proposed feature._

**Title:**  
**Summary:**

## 2) Problem / Motivation
_What problem does this feature solve? Who benefits (users, integrators, maintainers)?_

## 3) Goals and non‑goals
**Goals:**  
- (What this feature must accomplish)

**Non-goals:**  
- (What this feature explicitly will not do)

## 4) Proposed solution
_Detail the design, API changes, file/structure changes, and examples of how the API will be used (code snippets preferred)._

**API surface (example):**
```python
# example usage
db.craeate_table(
    "users",
    columns={
        "id": "INT",
        "name": "TEXT",
        "age": "INT",
    },
    id_generator="id",
)
# ...
```

5) Backwards compatibility

Will this change be backwards-compatible? If not — migration strategy.

6) Acceptance criteria

List measurable criteria for when this feature can be considered done (tests, docs, performance targets).

✅ Unit tests covering X

✅ Documentation updated in README / docs/

✅ No regression for existing CRUD ops

7) Performance, security, and testing considerations

Estimate performance impact, required benchmarks, and security implications.

8) Alternatives considered

List alternatives and why they were rejected.

9) Related issues / PRs

Link any existing issues or PRs that relate to this feature.

10) Additional context / mockups

Optional: UI mockups, GIFs, diagrams, or links to external references.