# Role 1 — Slide Outline (2 minutes)

## Slide: Problem, Objective, Data and Tests

**Problem (30 s)**
- Choosing a meal from a large menu is hard when several requirements apply at once: budget, cuisine, meal time and allergies.
- Checking every dish by hand is slow and can lead to unsafe choices.

**Objective (20 s)**
- Build a system that returns every meal satisfying all user requirements.
- Solve the same task with two techniques — Propositional Logic and CSP — and compare them on identical data and tests.

**Dataset and cleaning (40 s)**
- Real Kaggle New York restaurant menus dataset, cleaned by Role 1.
- Prices cleaned and capped at 200; duplicates dropped; cuisine = first tag; rare cuisines grouped as Other.
- Allergens and meal times derived from dish-name keywords — approximate, not verified ingredients.
- Three sizes: 100, 1,000 and 10,000 meals, all taken from the same cleaned file.

**Tests and correctness (30 s)**
- 8 tests: normal, strict, no-match, almost-all and boundary cases.
- Independent brute-force ground truth.
- Both solvers: 24/24 passed.

**Transition (0 s)**
- "Now I'll hand over to Role 2, who will explain how the Logic solver works."

Speaker notes: be ready to explain why brute force is a valid ground truth, and why the same labels are used for both solvers.
