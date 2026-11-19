"""Role 2: Propositional Logic solver.

Rule (with only the active facts included):

    Recommend <=> PriceOK AND IsCuisine AND IsMealTime AND NOT HasNuts

One model per meal: every fact has a fixed true/false value for that meal,
so there is exactly one row of the truth table to check.

Evaluation count: one evaluation per fact computed (not per lookup).
"""

import time


def _norm(text):
    """Same normalisation as brute_force.norm: lowercase + collapse spaces."""
    return " ".join(str(text).lower().split())


def recommend(meals, requirements):
    start = time.perf_counter()

    matching_ids = []
    evaluations = 0

    # ---- Step 1: decide which facts are active ----
    budget = requirements.get("max_budget")
    cuisine = _norm(requirements.get("cuisine") or "")
    meal_time = _norm(requirements.get("meal_time") or "")

    allergies = []
    for item in requirements.get("allergies") or []:
        a = _norm(item)
        if a and a not in allergies:
            allergies.append(a)

    use_price = budget is not None and budget != ""
    use_cuisine = bool(cuisine)
    use_time = bool(meal_time)

    # The rule, kept as a visible named object rather than an if filter.
    rule = "Recommend <=> PriceOK AND IsCuisine AND IsMealTime AND NOT HasNuts"

    def evaluate_rule(facts):
        """Model checking: all required facts true, no avoided allergen present."""
        recommend_is_true = True
        if use_price:
            recommend_is_true = recommend_is_true and facts["PriceOK"]
        if use_cuisine:
            recommend_is_true = recommend_is_true and facts["IsCuisine"]
        if use_time:
            recommend_is_true = recommend_is_true and facts["IsMealTime"]
        for a in allergies:
            recommend_is_true = recommend_is_true and not facts["Has_" + a]
        return recommend_is_true

    # ---- Step 2: one model (fact assignment) per meal ----
    for meal in meals:
        facts = {}

        if use_price:
            facts["PriceOK"] = meal["price"] <= budget
            evaluations += 1                      # one fact computed

        if use_cuisine:
            facts["IsCuisine"] = _norm(meal["cuisine"]) == cuisine
            evaluations += 1

        if use_time:
            facts["IsMealTime"] = any(
                _norm(t) == meal_time for t in meal["meal_times"]
            )
            evaluations += 1

        present = [_norm(x) for x in meal["allergens"]]
        for a in allergies:
            facts["Has_" + a] = a in present
            evaluations += 1

        if evaluate_rule(facts):                 # rule is true for this model
            matching_ids.append(meal["id"])

    elapsed_ms = (time.perf_counter() - start) * 1000

    return matching_ids, {
        "time_ms": elapsed_ms,
        "evaluations": evaluations,
    }
