"""Role 3: Constraint Satisfaction Problem (CSP) solver.

CSP model
---------
    Variable    : X = the meal to recommend
    Domain      : D(X) = every meal in the menu
    Constraints : one small function per ACTIVE requirement
                    C_cuisine   : X.cuisine == chosen cuisine
                    C_meal_time : chosen meal time in X.meal_times
                    C_no_<A>    : allergen A not in X.allergens   (one per allergy)
                    C_price     : X.price <= budget               (inclusive)
                  Missing or empty requirements create no constraint.
                  If no constraint is active, every meal is a solution.

Search (backtracking)
---------------------
    For each meal in the domain:
        1. Assign it to X                       (assignments_tried += 1)
        2. Check the constraints in a fixed order, counting 1 evaluation per check:
               cuisine -> meal time -> allergies -> price
           (equality checks tend to fail fastest, so most bad meals stop early)
        3. At the FIRST failed constraint, backtrack: undo the assignment and
           try the next meal (the remaining constraints are NOT checked).
        4. If every constraint passes, the assignment is a solution: keep the meal
           and continue, so that ALL solutions are returned.

Evaluation count: 1 per constraint checked on one meal.
Returns: (list_of_matching_ids, {"time_ms", "evaluations", "assignments_tried"})
"""

import time

DEFAULT_ORDER = ("cuisine", "meal_time", "allergies", "price")


def _norm(text):
    """Same normalisation as brute_force.norm: lowercase + collapse spaces."""
    return " ".join(str(text).lower().split())


def build_constraints(requirements, order=DEFAULT_ORDER):
    """Turn the active requirements into an ordered list of (name, check_function).

    Each check_function takes one meal and returns True (satisfied) or False (violated).
    """
    budget = requirements.get("max_budget")
    cuisine = _norm(requirements.get("cuisine") or "")
    meal_time = _norm(requirements.get("meal_time") or "")

    allergies = []
    for item in requirements.get("allergies") or []:
        a = _norm(item)
        if a and a not in allergies:
            allergies.append(a)

    # One group of constraints per requirement type.
    groups = {"cuisine": [], "meal_time": [], "allergies": [], "price": []}

    if cuisine:
        groups["cuisine"].append(
            ("C_cuisine", lambda meal: _norm(meal["cuisine"]) == cuisine))

    if meal_time:
        groups["meal_time"].append(
            ("C_meal_time",
             lambda meal: any(_norm(t) == meal_time for t in meal["meal_times"])))

    for a in allergies:
        # a=a fixes the current allergen inside the lambda (otherwise all lambdas
        # would use the last allergen in the loop).
        groups["allergies"].append(
            ("C_no_" + a,
             lambda meal, a=a: a not in [_norm(x) for x in meal["allergens"]]))

    if budget is not None and budget != "":
        groups["price"].append(
            ("C_price", lambda meal: meal["price"] <= budget))

    constraints = []
    for group_name in order:
        constraints.extend(groups[group_name])
    return constraints


def recommend(meals, requirements, order=DEFAULT_ORDER):
    """Backtracking search over the domain (all meals); returns every solution."""
    start = time.perf_counter()

    constraints = build_constraints(requirements, order)   # C
    domain = meals                                         # D(X)

    solutions = []
    evaluations = 0
    assignments_tried = 0

    for meal in domain:
        assignment = meal                 # X = meal
        assignments_tried += 1

        consistent = True
        for _name, check in constraints:
            evaluations += 1              # one constraint checked on one meal
            if not check(assignment):
                consistent = False        # first failure -> backtrack
                break                     # skip the remaining constraints

        if consistent:                    # all constraints satisfied -> solution
            solutions.append(assignment["id"])
        # otherwise: backtrack, X is unassigned and the next meal is tried

    elapsed_ms = (time.perf_counter() - start) * 1000

    return solutions, {
        "time_ms": elapsed_ms,
        "evaluations": evaluations,
        "assignments_tried": assignments_tried,
    }


def trace_meal(meal, requirements, order=DEFAULT_ORDER):
    """Print how one meal is checked: which constraint fails first and where it backtracks.
    Used for the slide example and the demo."""
    print(f"Assign X = meal {meal['id']}: {meal['name']} "
          f"(price {meal['price']}, {meal['cuisine']}, "
          f"times {meal['meal_times']}, allergens {meal['allergens']})")
    for name, check in build_constraints(requirements, order):
        ok = check(meal)
        print(f"  check {name:<14} -> {'satisfied' if ok else 'VIOLATED'}")
        if not ok:
            print("  => backtrack: remaining constraints skipped, try the next meal")
            return False
    print("  => all constraints satisfied: meal is a solution")
    return True


if __name__ == "__main__":
    # Quick run on the 100-meal dataset with the proposal example (T1).
    import data
    meals = data.load_meals("meals_100.csv")
    t1 = {"max_budget": 30, "cuisine": "Italian", "meal_time": "Dinner", "allergies": ["Nuts"]}
    ids, metrics = recommend(meals, t1)
    print("T1 solutions:", ids)
    print("metrics:", metrics)
