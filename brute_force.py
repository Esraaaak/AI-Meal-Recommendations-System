def _norm(text):
    """Ignore capital letters and extra spaces."""
    return str(text).strip().lower()


def expected(meals, requirements):
    budget = requirements.get("max_budget")
    cuisine = requirements.get("cuisine")
    meal_time = requirements.get("meal_time")
    allergies = requirements.get("allergies") or []

    result = []
    for meal in meals:
        ok = True

        # budget is inclusive: price <= max_budget
        if budget is not None and budget != "":
            if meal["price"] > budget:
                ok = False

        if cuisine:
            if _norm(meal["cuisine"]) != _norm(cuisine):
                ok = False

        if meal_time:
            times = [_norm(t) for t in meal["meal_times"]]
            if _norm(meal_time) not in times:
                ok = False

        meal_allergens = [_norm(a) for a in meal["allergens"]]
        for allergy in allergies:
            if _norm(allergy) in meal_allergens:
                ok = False

        if ok:
            result.append(meal["id"])

    return sorted(result)