"""Ground truth (answer key). Plain loops and if statements, no clever tricks.
expected(meals, requirements) -> sorted list of matching meal ids.

requirements example:
  {"max_budget": 30, "cuisine": "Italian", "meal_time": "Dinner", "allergies": ["Nuts"]}
Missing, None or empty fields are ignored. If nothing is active, every meal matches.
Rules: price <= budget (inclusive); text comparison ignores capitals and extra spaces.
"""

def norm(text):
    return " ".join(str(text).lower().split())

def expected(meals, requirements):
    budget = requirements.get("max_budget")
    cuisine = requirements.get("cuisine")
    meal_time = requirements.get("meal_time")
    allergies = requirements.get("allergies") or []

    want_cuisine = norm(cuisine) if cuisine not in (None, "") and norm(cuisine) != "" else None
    want_time = norm(meal_time) if meal_time not in (None, "") and norm(meal_time) != "" else None
    avoid = [norm(a) for a in allergies if norm(a) != ""]

    result = []
    for meal in meals:
        ok = True
        if budget is not None and meal["price"] > budget:
            ok = False
        if ok and want_cuisine is not None and norm(meal["cuisine"]) != want_cuisine:
            ok = False
        if ok and want_time is not None:
            times = [norm(t) for t in meal["meal_times"]]
            if want_time not in times:
                ok = False
        if ok:
            have = [norm(a) for a in meal["allergens"]]
            for a in avoid:
                if a in have:
                    ok = False
                    break
        if ok:
            result.append(meal["id"])
    return sorted(result)
