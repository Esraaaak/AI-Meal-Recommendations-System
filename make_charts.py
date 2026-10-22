import csv
import sys

import matplotlib
matplotlib.use("Agg")  # draw into image files, no window needed
import matplotlib.pyplot as plt

path = sys.argv[1] if len(sys.argv) > 1 else "results.csv"

# ---------- 1. Read the results ----------
rows = []
with open(path, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        try:
            rows.append({
                "solver": r["solver"],
                "size": int(r["dataset_size"]),
                "time": float(r["avg_time_ms"]),
                "evals": float(r["evaluations"]),
                "correct": str(r["correct"]).strip().lower() in ("true", "1", "yes"),
            })
        except (ValueError, KeyError):
            # a row with an error or an empty value (for example a solver crashed): skip it
            print("skipped a row that could not be read:", r)

if not rows:
    sys.exit("No usable rows in " + path)

solvers = sorted({r["solver"] for r in rows})
sizes = sorted({r["size"] for r in rows})


# ---------- 2. Average over the tests for each solver and size ----------
def average(solver, size, key):
    values = [r[key] for r in rows if r["solver"] == solver and r["size"] == size]
    return sum(values) / len(values)


STYLE = {"logic": ("tab:blue", "o"), "csp": ("tab:orange", "s")}  # colour, marker


def draw(key, title, ylabel, filename):
    plt.figure(figsize=(7, 4.5))
    for solver in solvers:
        colour, marker = STYLE.get(solver, ("tab:green", "^"))
        plt.plot(sizes, [average(solver, s, key) for s in sizes],
                 marker=marker, color=colour, linewidth=2, label=solver)
    plt.xscale("log")  # sizes are 100, 1000, 10000, so a log axis spaces them evenly
    plt.xticks(sizes, [str(s) for s in sizes])
    plt.xlabel("Number of meals in the menu")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print("saved", filename)


draw("time", "Average running time vs. menu size",
     "Average time per test (ms)", "chart_time_vs_size.png")
draw("evals", "Average evaluations vs. menu size",
     "Average evaluations per test", "chart_evaluations_vs_size.png")

# ---------- 3. Correctness table ----------
print()
print("Correctness (tests passed / tests run)")
print("solver".ljust(10) + "".join(str(s).rjust(12) for s in sizes))
for solver in solvers:
    line = solver.ljust(10)
    for s in sizes:
        mine = [r for r in rows if r["solver"] == solver and r["size"] == s]
        line += (str(sum(r["correct"] for r in mine)) + "/" + str(len(mine))).rjust(12)
    print(line)