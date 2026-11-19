# Role 2 — Slide Outline (2 minutes)

## Slide: Propositional Logic

**Facts (40 s)**
- For each active requirement we create one named true/false fact about the meal:
  - `PriceOK` — price ≤ budget
  - `IsCuisine` — cuisine equals the chosen cuisine
  - `IsMealTime` — the chosen meal time is in the meal's times
  - `HasNuts`, `HasDairy`, … — one per allergy
- Missing or empty requirements create no fact.

**Rule (30 s)**
- `Recommend <=> PriceOK AND IsCuisine AND IsMealTime AND NOT HasNuts`
- Only the active facts appear in the rule. If nothing is active, the rule is true and every meal matches.

**Worked example (30 s)**
- Meal 51: Meatballs, price 11, Italian, no allergens, `Lunch|Dinner`.
- T1 requires budget ≤ 30, Italian, Dinner, no Nuts.
- Facts: `PriceOK = true`, `IsItalian = true`, `IsDinner = true`, `HasNuts = false`.
- Rule evaluates to true → meal 51 is recommended. It is one of the 3 matches in T1 at 100 meals.

**Results and transition (20 s)**
- One model per meal (one truth-table row), no early stopping.
- 24/24 tests passed; T1 used 400 evaluations at 100 meals.
- "Next, Role 3 will show how CSP solves the same task with constraints and backtracking."

Speaker notes: be ready to define proposition, AND/OR/NOT/IFF, truth table and model checking, and to answer a basic question about CSP.
