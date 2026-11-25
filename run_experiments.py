import csv
import json
import matplotlib.pyplot as plt

from pathlib import Path
from statistics import mean
from data import load_meals
from brute_force import expected

import logic_solver
import csp_solver


# ==========================================
# 1. Experiment Configuration
# ==========================================

SIZES = [100, 1000, 10000]
REPEATS = 5

SOLVERS = {
    "Logic": logic_solver.recommend,
    "CSP": csp_solver.recommend
}

FIELDS = [
    "solver",
    "dataset_size",
    "test_id",
    "num_constraints",
    "matches",
    "avg_time_ms",
    "evaluations",
    "correct"
]


# ==========================================
# 2. Load Test Cases and Expected Results
# ==========================================

with open("tests.json", encoding="utf-8") as file:
    tests = json.load(file)

with open("expected_results.json", encoding="utf-8") as file:
    expected_results = json.load(file)


# ==========================================
# 3. Count Active Constraints
# ==========================================

def count_constraints(requirements):

    count = 0

    budget = requirements.get("max_budget")

    if budget is not None and budget != "":
        count += 1

    if str(requirements.get("cuisine") or "").strip():
        count += 1

    if str(requirements.get("meal_time") or "").strip():
        count += 1

    allergies = {
        " ".join(str(a).lower().split())
        for a in requirements.get("allergies") or []
        if str(a).strip()
    }

    count += len(allergies)

    return count


# ==========================================
# 4. Run One Experiment
# ==========================================

def run_experiment(solver_name, solver, meals,
                   test, expected_ids, errors):

    times = []
    evaluation_counts = []
    match_counts = []
    correctness = []

    requirements = test["requirements"]

    for repeat in range(REPEATS):

        try:

            matching_ids, metrics = solver(
                meals,
                requirements
            )

            times.append(metrics["time_ms"])
            evaluation_counts.append(metrics["evaluations"])
            match_counts.append(len(matching_ids))

            is_correct = (
                sorted(matching_ids) == sorted(expected_ids)
            )

            correctness.append(is_correct)

            if not is_correct:
                errors.append(
                    f"{solver_name}, Size {len(meals)}, "
                    f"{test['id']}, Run {repeat + 1}: "
                    "Incorrect matching IDs"
                )

        except Exception as error:

            errors.append(
                f"{solver_name}, Size {len(meals)}, "
                f"{test['id']}, Run {repeat + 1}: {error}"
            )

            correctness.append(False)

    complete = len(times) == REPEATS

    consistent = (
        len(set(evaluation_counts)) == 1
        and len(set(match_counts)) == 1
    )

    if complete and not consistent:
        errors.append(
            f"{solver_name}, Size {len(meals)}, "
            f"{test['id']}: Inconsistent metrics"
        )

    return {
        "solver": solver_name,
        "dataset_size": len(meals),
        "test_id": test["id"],
        "num_constraints": count_constraints(requirements),
        "matches": match_counts[0]
            if complete and consistent else "",
        "avg_time_ms": round(mean(times), 6)
            if complete else "",
        "evaluations": evaluation_counts[0]
            if complete and consistent else "",
        "correct": complete and consistent and all(correctness)
    }


# ==========================================
# 5. Test Sample Dataset
# ==========================================

def test_sample():

    if not Path("sample_meals.csv").exists():

        print("sample_meals.csv not found. Skipping sample test.")
        return

    meals = load_meals("sample_meals.csv")

    print("\nSample Dataset Test")

    errors = []

    for solver_name, solver in SOLVERS.items():

        passed = 0

        for test in tests:

            expected_ids = expected(
                meals,
                test["requirements"]
            )

            result = run_experiment(
                solver_name,
                solver,
                meals,
                test,
                expected_ids,
                errors
            )

            if result["correct"]:
                passed += 1

        print(f"{solver_name}: {passed}/{len(tests)} passed")

    if errors:
        raise RuntimeError("\n".join(errors))


# ==========================================
# 6. Run All Experiments
# ==========================================

def run_all_experiments():

    results = []
    errors = []

    for size in SIZES:

        meals = load_meals(f"meals_{size}.csv")

        if len(meals) != size:
            raise ValueError(
                f"Expected {size} meals, found {len(meals)}"
            )

        print(f"\nDataset Size: {size}")

        for solver_name, solver in SOLVERS.items():

            for test in tests:

                expected_ids = expected_results[
                    str(size)
                ][test["id"]]

                result = run_experiment(
                    solver_name,
                    solver,
                    meals,
                    test,
                    expected_ids,
                    errors
                )

                results.append(result)

                print(
                    f"{solver_name:5} | "
                    f"{test['id']} | "
                    f"Matches: {result['matches']} | "
                    f"Time: {result['avg_time_ms']} ms | "
                    f"Evaluations: {result['evaluations']} | "
                    f"Correct: {result['correct']}"
                )

    return results, errors


# ==========================================
# 7. Save Results to CSV
# ==========================================

def save_results(results):

    with open("results.csv", "w", newline="",
              encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nResults saved to results.csv")


# ==========================================
# 8. Print Correctness Table
# ==========================================

def print_correctness_table(results):

    print("\nCORRECTNESS TABLE")
    print("-" * 42)

    print(f"{'Dataset Size':<15}"
          f"{'Logic':<13}"
          f"{'CSP':<13}")

    print("-" * 42)

    for size in SIZES:

        logic_passed = sum(
            row["correct"]
            for row in results
            if row["solver"] == "Logic"
            and row["dataset_size"] == size
        )

        csp_passed = sum(
            row["correct"]
            for row in results
            if row["solver"] == "CSP"
            and row["dataset_size"] == size
        )

        logic_score = f"{logic_passed}/{len(tests)}"
        csp_score = f"{csp_passed}/{len(tests)}"

        print(f"{size:<15}"
              f"{logic_score:<13}"
              f"{csp_score:<13}")

    print("-" * 42)


# ==========================================
# 9. Calculate Average Metrics
# ==========================================

def average_metric(results, solver_name, metric):

    averages = []

    for size in SIZES:

        rows = [
            row for row in results
            if row["solver"] == solver_name
            and row["dataset_size"] == size
        ]

        if len(rows) == len(tests) and all(
            row["correct"] and row[metric] != ""
            for row in rows
        ):

            averages.append(
                mean(row[metric] for row in rows)
            )

        else:

            averages.append(float("nan"))

    return averages


# ==========================================
# 10. Execution Time Chart
# ==========================================

def plot_execution_time(results):

    plt.figure(figsize=(9, 5))

    for solver_name in SOLVERS:

        averages = average_metric(
            results,
            solver_name,
            "avg_time_ms"
        )

        plt.plot(
            SIZES,
            averages,
            marker="o",
            label=solver_name
        )

    plt.title("Average Execution Time vs Dataset Size")
    plt.xlabel("Dataset Size")
    plt.ylabel("Average Execution Time (ms)")
    plt.xscale("log")
    plt.xticks(SIZES, ["100", "1,000", "10,000"])
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "time_vs_dataset_size.png",
        dpi=300
    )

    plt.close()


# ==========================================
# 11. Evaluations Chart
# ==========================================

def plot_evaluations(results):

    plt.figure(figsize=(9, 5))

    for solver_name in SOLVERS:

        averages = average_metric(
            results,
            solver_name,
            "evaluations"
        )

        plt.plot(
            SIZES,
            averages,
            marker="o",
            label=solver_name
        )

    plt.title("Average Evaluations vs Dataset Size")
    plt.xlabel("Dataset Size")
    plt.ylabel("Average Number of Evaluations")
    plt.xscale("log")
    plt.xticks(SIZES, ["100", "1,000", "10,000"])
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        "evaluations_vs_dataset_size.png",
        dpi=300
    )

    plt.close()


# ==========================================
# 12. Save Experiment Errors
# ==========================================

def save_errors(errors):

    with open("experiment_errors.log", "w",
              encoding="utf-8") as file:

        for error in errors:
            file.write(error + "\n")

    if errors:
        print("\nErrors found. Check experiment_errors.log")
    else:
        print("\nNo experiment errors found.")


# ==========================================
# 13. Main Program
# ==========================================

def main():

    print("AI Meal Recommendation System")
    print("Role 4: Experiments and Analysis")

    test_sample()

    results, errors = run_all_experiments()

    save_results(results)

    print_correctness_table(results)

    plot_execution_time(results)

    plot_evaluations(results)

    save_errors(errors)

    print(f"\nTotal experiment results: {len(results)}")
    print("Experiments completed.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())