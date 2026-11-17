
import json
from data import load_meals
from logic_solver import recommend
from brute_force import expected

# Load all test cases
with open("tests.json", encoding="utf-8") as file:
    tests = json.load(file)

# Test every dataset size
for size in [100, 1000, 10000]:
    meals = load_meals("meals_" + str(size) + ".csv")

    print("\nDataset:", size)

    # Run each test case
    for test in tests:
        test_id = test["id"]
        requirements = test["requirements"]

        # Get results from the logic solver
        ids, metrics = recommend(meals, requirements)

        # Get correct results using brute force
        correct_ids = expected(meals, requirements)

        # Compare both results
        passed = sorted(ids) == sorted(correct_ids)

        print(
            test_id,
            "|", "PASS" if passed else "FAIL",
            "| Matches:", len(ids),
            "| Evaluations:", metrics["evaluations"]
        )

# --------------------------------------------------
# Additional edge-case tests for Role 2
# --------------------------------------------------

edge_cases = [
    ("No requirements", {}),
    ("Budget only", {"max_budget": 25}),
    ("Exact price", {"max_budget": 30}),
    ("Multiple allergies", {"allergies": ["Nuts", "Dairy"]}),
    ("Case and whitespace", {
        "cuisine": "  italian  ",
        "meal_time": " DINNER "
    }),
    ("Empty requirements", {
        "cuisine": "",
        "meal_time": "",
        "allergies": []
    })
]

meals = load_meals("sample_meals.csv")

print("\nEDGE CASE TESTS")

for name, requirements in edge_cases:
    ids, metrics = recommend(meals, requirements)
    correct_ids = expected(meals, requirements)

    passed = sorted(ids) == sorted(correct_ids)

    print(
        name,
        "|", "PASS" if passed else "FAIL",
        "| Matches:", len(ids),
        "| Evaluations:", metrics["evaluations"]
    )
