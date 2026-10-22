import json
from data import load_meals
from brute_force import expected

# 1. Read the tests
with open("tests.json", encoding="utf-8") as f:
    tests = json.load(f)

# 2. For each menu size, compute the correct answer for every test
results = {}
for size in (100, 1000, 10000):
    meals = load_meals(f"meals_{size}.csv")
    results[str(size)] = {t["id"]: expected(meals, t["requirements"]) for t in tests}

# 3. Save everything to a file
with open("expected_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f)

print("saved expected_results.json")