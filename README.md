# AI Meal Recommendation System

Comparing **Propositional Logic** and **Constraint Satisfaction (CSP)** on the same problem:
given a user's requirements (budget, cuisine, meal time, allergies), find every meal on a menu that satisfies all of them.

Course project for AI4101.

## Requirements format

```python
{"max_budget": 30, "cuisine": "Italian", "meal_time": "Dinner", "allergies": ["Nuts"]}
```
A missing or empty field is not checked. If nothing is given, every meal matches.

## Rules for everyone

- Python 3.9+ (no `match` statements, no `X | Y` type hints). Standard library + matplotlib only.
- Load data with `from data import load_meals`.
- Each solver must provide:
  `recommend(meals, requirements) -> (list_of_matching_ids, {"time_ms": ..., "evaluations": ...})`
- One evaluation: Logic = one symbol looked up while checking a clause; CSP = one constraint checked on one meal.
- Budget is inclusive (`price <= max_budget`). Text comparison ignores capitals and extra spaces.
- Use the `meals_*.csv` files in this repo. **Do not run `data.py` again**, so everyone tests on identical data.

## Files

| File | What it is |
|---|---|
| `sample_meals.csv` | 20 hand-written meals for quick testing |
| `meals_100.csv`, `meals_1000.csv`, `meals_10000.csv` | Generated menus for testing and scalability |
| `data.py` | `load_meals(path)` reads a menu; `generate(n)` creates one |
| `brute_force.py` | The answer key: `expected(meals, requirements)` returns the correct meal ids |
| `tests.json` | Test cases (T1 to T4 so far; T5 to T8 to be added by Role 3) |
| `make_expected.py` | Recomputes `expected_results.json` after tests change |
| `expected_results.json` | Correct answers: `results["100"]["T1"]` = correct ids for T1 on the 100-meal menu |
| `make_charts.py` | Draws the comparison charts from `results.csv` |

## Check your solver

Your sorted result must equal the saved answer. For example:

```python
import json
from data import load_meals
meals = load_meals("meals_100.csv")
answers = json.load(open("expected_results.json"))
print(sorted(my_ids) == answers["100"]["T1"])
```
