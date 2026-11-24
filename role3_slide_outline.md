# Role 3 — Slide Outline (2 minutes)

## Slide: Constraint Satisfaction Problem (CSP)

**The CSP model (40 s)**
- Variable: X = the meal to recommend
- Domain: all meals in the menu
- Constraints, one per active requirement, checked in this order:
  1. `C_cuisine` — cuisine equals the chosen cuisine
  2. `C_meal_time` — the chosen meal time is in the meal's times
  3. `C_no_Nuts`, … — the allergen is not in the meal's allergens (one per allergy)
  4. `C_price` — price ≤ budget
- Missing or empty requirements create no constraint.

**Backtracking trace (40 s), T1: budget ≤ 30, Italian, Dinner, no Nuts**
- Assign X = meal 1, Potato Salad (Diner): `C_cuisine` violated → backtrack, the other 3 constraints are skipped. 1 evaluation.
- Assign X = meal 51, Meatballs (Italian, 11, Lunch|Dinner, no allergens): all 4 constraints satisfied → solution. 4 evaluations.
- At 100 meals: 97 meals × 1 + 3 meals × 4 = **109 evaluations**; solutions 51, 78, 79.

**Constraint order (20 s)**
- 10,000 meals, T1: 12,438 evaluations in our order vs. 36,664 in reversed order. Same answers.

**Results and transition (20 s)**
- 24/24 tests passed against the answer key.
- Stops at the first failure, but the constraints are independent single-meal checks, so here it is close to a filter.
- "Next, Role 4 compares both solvers on time, evaluations, correctness and scalability."

Speaker notes: be ready to define variable, domain, constraint, assignment, solution and backtracking, to explain why order matters, and to answer a basic question about the Logic solver (facts, rule, one model per meal).
