# Role 3 — CSP: Strengths and Limitations

## Result
`csp_solver.py` passed **24/24** in `check_solvers.py` (8 tests × 3 sizes), the same answers as `brute_force.py` and `logic_solver.py`.

## Evaluations (1 per constraint checked on one meal)

| Test | 100 meals | 1,000 meals | 10,000 meals |
|---|---|---|---|
| T1 proposal example | 109 | 1,210 | 12,438 |
| T5 very strict | 142 | 1,308 | 13,100 |
| T6 no match (budget 0) | 100 | 1,000 | 10,000 |
| T7 budget 1000 only | 100 | 1,000 | 10,000 |

Why T1 at 100 meals is 109: 97 meals fail the first constraint (cuisine) → 1 check each = 97; the 3 Italian meals pass all 4 constraints → 3 × 4 = 12; total 97 + 12 = 109.

## Constraint order (10,000 meals)

| Test | Default order (cuisine → meal time → allergies → price) | Reversed order (price → allergies → meal time → cuisine) |
|---|---|---|
| T1 | 12,438 | 36,664 |
| T5 | 13,100 | 28,895 |

Same answers in both orders, but about 2–3 times more checks when the weak constraints come first.

## Strengths
1. Clear formal model: one variable (the meal), its domain (all meals) and one constraint function per active requirement.
2. Backtracking stops at the first violated constraint, so most meals are rejected after one check (T1: 97 of 100 meals stop at the cuisine check).
3. Ordering the most selective constraints first reduces the work a lot (T1 at 10,000: 12,438 vs. 36,664 evaluations).
4. New requirements are easy to add: write one more small constraint function and put it in the list.
5. Deterministic and verified against the answer key on all tests and sizes.

## Limitations
1. Every constraint involves one meal only (unary constraints), so the search has no real tree to prune; here CSP behaves very close to a filter.
2. The saving depends on constraint order and on the data; with a bad order the benefit mostly disappears.
3. When few requirements are active or almost every meal passes (T6, T7), it does the same work as Logic: 1 check per meal.
4. It still visits every meal once, so the work grows linearly with the menu size.
5. It returns all matching meals without ranking them, and like Logic it relies on approximate keyword-derived allergen and meal-time labels.
