"""Role 1's correctness check: compare each solver with the answer key on every test and size.
Usage:  python check_solvers.py            (checks logic_solver and csp_solver)
        python check_solvers.py logic_solver
A solver module must define recommend(meals, requirements) -> (ids, metrics)."""
import importlib, json, sys
import data
from brute_force import expected

SIZES = (100, 1000, 10000)

def check(module_name):
    solver = importlib.import_module(module_name)
    with open("tests.json", encoding="utf-8") as f:
        tests = json.load(f)
    passed = total = 0
    for n in SIZES:
        meals = data.load_meals(f"meals_{n}.csv")
        for t in tests:
            total += 1
            want = expected(meals, t["requirements"])
            try:
                got, _metrics = solver.recommend(meals, t["requirements"])
                ok = sorted(got) == want
                note = "" if ok else f"returned {len(got)} ids, expected {len(want)}"
            except Exception as e:
                ok, note = False, f"crashed: {e!r}"
            passed += ok
            if not ok:
                print(f"  MISMATCH {module_name} size={n} test={t['id']}: {note}")
    print(f"{module_name}: {passed}/{total} passed")
    return passed == total

if __name__ == "__main__":
    names = sys.argv[1:] or ["logic_solver", "csp_solver"]
    results = []
    for name in names:
        try:
            results.append(check(name))
        except ModuleNotFoundError:
            print(f"{name}: file not found yet")
            results.append(False)
    sys.exit(0 if all(results) else 1)
