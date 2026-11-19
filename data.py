import csv

def load_meals(path):
    """Read a meals CSV and return a list of meal dictionaries.
    Keys: id (int), name, price (int), cuisine, allergens (list), meal_times (list)."""
    meals = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            meals.append({
                "id": int(row["id"]),
                "name": row["name"],
                "price": int(row["price"]),
                "cuisine": row["cuisine"],
                "allergens": [a for a in row["allergens"].split("|") if a],
                "meal_times": [t for t in row["meal_times"].split("|") if t],
            })
    return meals
