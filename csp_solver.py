"""Role 3: CSP solver.

Formal model
------------
Variable    : the meal
Domain      : all meals on the menu
Constraints : one small function per active requirement

For each meal we assign the variable, check the constraints in order and
count one evaluation per check. The first failed constraint causes a
backtrack to the next meal; only meals that pass every constraint are
solutions, so all solutions are collected.

Evaluation count: one evaluation per constraint checked on one meal.
Constraint order matters because a failing early constraint stops the
remaining checks for that meal.
"""

import time


def _norm(text):
    """Same normalisation as brute_force.norm: lowercase + collapse spaces."""
    return " ".join(str(text).lower().split())


def _build_constraints(requirements):
    """Return (name, check) pairs in the default order."""
    constraints = []

    budget = requirements.get("max_budget")
    cuisine = _norm(requirements.get("cuisine") or "")
    meal_time = _norm(requirements.get("meal_time") or "")

    # Equality checks first: they tend to fail fastest.
    if cuisine:
        constraints.append(
            ("cuisine", lambda meal, want=cuisine: _norm(meal["cuisine"]) == want)
        )

    if meal_time:
        constraints.append(
            ("meal_time",
             lambda meal, want=meal_time: any(_norm(t) == want for t in meal["meal_times"]))
        )

    for item in requirements.get("allergies") or []:
        avoid = _norm(item)
        if avoid and avoid not in [name for name, _ in constraints]:
            constraints.append(
                ("allergen:" + avoid,
                 lambda meal, a=avoid: all(_norm(x) != a for x in meal["allergens"]))
            )

    if budget is not None and budget != "":
        constraints.append(
            ("price", lambda meal, limit=budget: meal["price"] <= limit)
        )

    return constraints


def recommend(meals, requirements, order="default"):
    start = time.perf_counter()

    if order not in ("default", "reversed"):
        raise ValueError("order must be 'default' or 'reversed'")

    constraints = _build_constraints(requirements)
    if order == "reversed":
        constraints = list(reversed(constraints))

    matching_ids = []
    evaluations = 0
    assignments_tried = 0

    # ---- Assign each meal to the variable and search its constraints ----
    for meal in meals:
        assignments_tried += 1
        consistent = True

        for _name, check in constraints:
            evaluations += 1                 # one constraint check
            if not check(meal):
                consistent = False
                break                        # backtrack to the next meal

        if consistent:
            matching_ids.append(meal["id"])

    elapsed_ms = (time.perf_counter() - start) * 1000

    return matching_ids, {
        "time_ms": elapsed_ms,
        "evaluations": evaluations,
        "assignments_tried": assignments_tried,
        "order": order,
    }
