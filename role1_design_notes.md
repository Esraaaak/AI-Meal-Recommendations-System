# Role 1 — Data and Test Design

## Dataset source
The data comes from the Kaggle **New York restaurant menus** dataset. The two raw files in `archive.zip` are:

- `menu_data.csv`: restaurant name, dish name, price (e.g. `$6.00`)
- `restaurant_data.csv`: restaurant name, cuisine tags, address and URLs

## Cleaning done by Role 1
1. Prices were parsed by removing `$` and commas and converting to integers. Prices above **200** were **dropped, not capped**, and invalid prices were also dropped.
2. Duplicate dishes were removed.
3. Cuisine was taken as the **first tag** in the restaurant's cuisine field; rare cuisines were grouped as **Other**. This gives the 13 allowed cuisine values used in the tests.
4. Allergens and meal times were **derived from dish-name keywords** (for example, a name containing "shrimp" gives `Seafood`; "breakfast" gives `Breakfast`). They are therefore **approximate** — they are not verified ingredient lists.
5. The final meal format is `id, name, price, cuisine, allergens, meal_times`. List fields are separated by `|` in the CSV and are Python lists in `data.py`.
6. `meals.csv` contains 82,237 cleaned meals. `meals_100.csv`, `meals_1000.csv` and `meals_10000.csv` are the first 100, 1,000 and 10,000 rows of that file.

## Why these tests
The 8 cases cover the main behaviour of both techniques and the edge cases:

| Test | Why it was chosen |
|---|---|
| T1 | The proposal example: budget + cuisine + meal time + allergy, 3 matches at 100 |
| T2 | Budget + meal time only, 57 matches at 100 |
| T3 | Cuisine + meal time + one allergy, 5 matches at 100 |
| T4 | Three allergies only, 70 matches at 100 |
| T5 | Very strict but not empty: Diner + Breakfast + budget 15 + Nuts + Dairy, **4 matches at 100** |
| T6 | No match: budget 0, 0 matches |
| T7 | Almost everything matches: budget 1000, all 100 meals |
| T8 | Boundary: budget exactly 12 with Italian. The boundary is real only at sizes 1,000 and 10,000; no Italian meal costs exactly 12 in the 100-meal sample |

Together they check normal matches, many matches, few matches, zero matches and an inclusive price boundary. The same tests run on all three dataset sizes to support the scalability comparison.

## Correctness results
`brute_force.py` is the independent ground truth: plain loops and `if` statements that follow the matching rules exactly (price ≤ budget, inclusive; text compared case-insensitively with extra spaces collapsed; empty fields ignored). Both solvers were run on all 8 tests × 3 sizes using `check_solvers.py`.

**Result: logic_solver 24/24 passed; csp_solver 24/24 passed.**

Using the same labels, datasets and tests for both solvers makes the comparison fair. The evaluation counts still follow each technique's own definition, so execution time is the more direct comparison.

## Limitations of the derived labels
Because allergens and meal times are keyword-derived from dish names, they can be missing or wrong: a dish with nuts in the name is caught, but a dish containing nuts that does not say so in its name is not. Meal times are guesses from words like "breakfast" or "lunch", not real restaurant serving times. Cuisine is only the first tag, so multi-tag restaurants lose information. These limits affect both solvers equally and should be mentioned in the discussion.
