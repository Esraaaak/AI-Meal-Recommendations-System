import csv
import random

# Each ingredient and the allergens it contains.
ALLERGEN_OF = {
    # contain allergens
    "almond": ["Nuts"], "walnut": ["Nuts"], "cheese": ["Dairy"], "milk": ["Dairy"],
    "cream": ["Dairy"], "butter": ["Dairy"], "flour": ["Gluten"], "pasta": ["Gluten"],
    "bread": ["Gluten"], "egg": ["Eggs"], "mayonnaise": ["Eggs"], "shrimp": ["Seafood"],
    "tuna": ["Seafood"], "tofu": ["Soy"], "soy sauce": ["Soy", "Gluten"],
    # no allergens
    "chicken": [], "beef": [], "lamb": [], "rice": [], "tomato": [], "onion": [],
    "garlic": [], "spices": [], "lentils": [], "chickpeas": [], "potato": [],
    "lettuce": [], "cucumber": [], "olive oil": [], "lemon": [],
}
CUISINES = ["Italian", "Arabic", "Indian", "Asian", "American", "Mexican"]
MEAL_TIMES = ["Breakfast", "Lunch", "Dinner"]


def _split(text):
    """'Gluten|Dairy' -> ['Gluten', 'Dairy'];  '' -> []"""
    return [x for x in text.split("|") if x]


def load_meals(path):
    """Read a meals CSV file and return a list of meals."""
    meals = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            meals.append({
                "id": int(row["id"]),
                "name": row["name"],
                "price": int(row["price"]),
                "cuisine": row["cuisine"],
                "ingredients": _split(row["ingredients"]),
                "allergens": _split(row["allergens"]),
                "meal_times": _split(row["meal_times"]),
            })
    return meals


def generate(n, seed=40):
    """Create n random meals. The same seed always gives the same meals."""
    rng = random.Random(seed)
    names = list(ALLERGEN_OF)
    meals = []
    for i in range(1, n + 1):
        ingredients = rng.sample(names, rng.randint(3, 5))
        allergens = sorted({a for ing in ingredients for a in ALLERGEN_OF[ing]})
        meals.append({
            "id": i,
            "name": f"Meal {i}",
            "price": rng.randint(5, 120),
            "cuisine": rng.choice(CUISINES),
            "ingredients": ingredients,
            "allergens": allergens,
            "meal_times": rng.sample(MEAL_TIMES, rng.randint(1, 2)),
        })
    return meals


def save_meals(meals, path):
    """Write meals to a CSV file in the agreed format."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "price", "cuisine", "ingredients", "allergens", "meal_times"])
        for m in meals:
            w.writerow([m["id"], m["name"], m["price"], m["cuisine"],
                        "|".join(m["ingredients"]), "|".join(m["allergens"]),
                        "|".join(m["meal_times"])])


if __name__ == "__main__":
    for n in (100, 1000, 10000):
        save_meals(generate(n), f"meals_{n}.csv")
        print("created", f"meals_{n}.csv")