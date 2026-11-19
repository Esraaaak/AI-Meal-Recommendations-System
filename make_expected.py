"""Build expected_results.json: the answer key for every test on every dataset size.
Run after changing the data or tests:  python make_expected.py"""
import json
import data
from brute_force import expected

SIZES = (100, 1000, 10000)

def main():
    with open("tests.json", encoding="utf-8") as f:
        tests = json.load(f)
    out = {}
    for n in SIZES:
        meals = data.load_meals(f"meals_{n}.csv")
        out[str(n)] = {t["id"]: expected(meals, t["requirements"]) for t in tests}
        print(n, {tid: len(ids) for tid, ids in out[str(n)].items()})
    with open("expected_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f)
    print("saved expected_results.json")

if __name__ == "__main__":
    main()
