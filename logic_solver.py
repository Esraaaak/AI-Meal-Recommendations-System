
import time


def recommend(meals, requirements):
    # Start measuring the execution time
    start = time.perf_counter()

    # Store matching meal IDs and count symbol evaluations
    matching_ids = []
    evaluations = 0

    # --------------------------------------------------
    # STEP 1: Create symbols from active requirements
    # --------------------------------------------------
    symbols = []
    symbol_info = {}

    budget = requirements.get("max_budget")
    cuisine = str(requirements.get("cuisine") or "").strip().lower()
    meal_time = str(requirements.get("meal_time") or "").strip().lower()
    allergies = requirements.get("allergies") or []

    if budget is not None and budget != "":
        symbols.append("PriceOK")
        symbol_info["PriceOK"] = ("price", budget)

    if cuisine:
        symbol = "Cuisine_" + cuisine
        symbols.append(symbol)
        symbol_info[symbol] = ("cuisine", cuisine)

    if meal_time:
        symbol = "Time_" + meal_time
        symbols.append(symbol)
        symbol_info[symbol] = ("time", meal_time)

    for allergy in allergies:
        allergy = str(allergy).strip().lower()

        if allergy:
            symbol = "Contains_" + allergy
            if symbol not in symbol_info:
                symbols.append(symbol)
                symbol_info[symbol] = ("allergen", allergy)

    # --------------------------------------------------
    # STEP 2: Build the Knowledge Base (CNF clauses)
    # --------------------------------------------------
    # Rule: Recommend iff all active requirements hold.
    # Each literal is (symbol_name, expected_truth_value).
    clauses = []

    # Recommend implies every active requirement
    for symbol in symbols:
        kind, value = symbol_info[symbol]

        if kind == "allergen":
            clauses.append([
                ("Recommend", False),
                (symbol, False)
            ])
        else:
            clauses.append([
                ("Recommend", False),
                (symbol, True)
            ])

    # All active requirements imply Recommend
    reverse_clause = [("Recommend", True)]

    for symbol in symbols:
        kind, value = symbol_info[symbol]

        if kind == "allergen":
            reverse_clause.append((symbol, True))
        else:
            reverse_clause.append((symbol, False))

    clauses.append(reverse_clause)

    # --------------------------------------------------
    # STEP 3: Create facts for each meal
    # --------------------------------------------------
    for meal in meals:
        facts = {}

        for symbol in symbols:
            kind, value = symbol_info[symbol]

            if kind == "price":
                facts[symbol] = meal["price"] <= value

            elif kind == "cuisine":
                facts[symbol] = (
                    str(meal["cuisine"]).strip().lower() == value
                )

            elif kind == "time":
                facts[symbol] = any(
                    str(item).strip().lower() == value
                    for item in meal["meal_times"]
                )

            elif kind == "allergen":
                facts[symbol] = any(
                    str(item).strip().lower() == value
                    for item in meal["allergens"]
                )

        # --------------------------------------------------
        # STEP 4: Entailment by contradiction
        # --------------------------------------------------
        # Assume Recommend is False for this meal.
        # If any KB clause becomes False, the assumption
        # is inconsistent and Recommend is entailed.
        model = dict(facts)
        model["Recommend"] = False

        contradiction = False

        # Evaluate ALL clauses without early stopping
        for clause in clauses:
            clause_satisfied = False

            for symbol, expected_value in clause:
                # One symbol lookup counts as one evaluation
                actual_value = model[symbol]
                evaluations += 1

                if actual_value == expected_value:
                    clause_satisfied = True

            if not clause_satisfied:
                contradiction = True

        # Keep meals for which Recommend is entailed
        if contradiction:
            matching_ids.append(meal["id"])

    # --------------------------------------------------
    # STEP 5: Return recommendations and metrics
    # --------------------------------------------------
    elapsed_ms = (time.perf_counter() - start) * 1000

    return matching_ids, {
        "time_ms": elapsed_ms,
        "evaluations": evaluations
    }
