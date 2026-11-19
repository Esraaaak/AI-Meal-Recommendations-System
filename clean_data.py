"""Role 1: clean the real New York restaurant menus dataset.

Source: Kaggle New York restaurant menus, provided as archive.zip with
    menu_data.csv      -> Restaurant, Item, Price
    restaurant_data.csv -> Name, URL, Cuisine, Address, Full_URL, Full_URL

This script is a documented reconstruction of the cleaning pipeline. The
rules below match the published meals.csv in structure and conventions, but
the original project used more refined keyword lists, so the derived labels
produced here may differ from the committed CSVs. It never overwrites the
committed files: output goes to cleaned_output/ by default.

Cleaning steps
    1. Parse prices (strip '$' and commas), drop invalid/non-positive prices,
       and cap prices at 200.
    2. Drop duplicate dishes using (restaurant, item, price), ignoring case.
    3. Cuisine = first tag in restaurant_data.csv's Cuisine field;
       'American (New)' is folded into 'American'; anything rare becomes
       'Other'.
    4. Allergens are derived from dish-name keywords (approximate).
    5. Meal times are derived from dish-name keywords:
       'breakfast' -> Breakfast, 'lunch' -> Lunch, 'dinner' -> Dinner,
       otherwise Lunch|Dinner.

Run: python3 clean_data.py
"""

import csv
import io
import re
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "archive.zip"
OUT_DIR = HERE / "cleaned_output"

ALLOWED_CUISINES = {
    "Diner", "American", "Chinese", "Japanese", "Italian", "Deli Food",
    "Burgers", "Latin American", "Asian", "Mexican", "Chicken", "Indian",
    "Other",
}

# Keyword lists used to derive allergens from dish names (approximate).
ALLERGEN_KEYWORDS = {
    "Nuts": ["nut", "nuts", "peanut", "peanuts", "almond", "almonds",
             "cashew", "cashews", "walnut", "walnuts", "pecan", "pecans",
             "pistachio", "pistachios", "pesto", "nutella"],
    "Dairy": ["cheese", "cream", "milkshake", "milk", "ice cream", "butter",
              "yogurt", "feta", "mozzarella", "parmesan", "parmigiana",
              "quesadilla", "cheeseburger", "custard", "dairy"],
    "Gluten": ["sandwich", "burger", "wrap", "pizza", "cake", "toast",
               "pancake", "pancakes", "bagel", "bread", "wheat", "flour",
               "noodle", "noodles", "pasta", "hero", "roll", "pita",
               "tortilla", "pastry", "panini", "multigrain", "french",
               "pie", "sub"],
    "Eggs": ["egg", "eggs", "omelette", "omelet", "benedict"],
    "Seafood": ["shrimp", "salmon", "tuna", "fish", "seafood", "sushi",
                "crab", "lobster", "calamari", "scallop", "scallops",
                "sashimi", "prawn", "prawns", "clam", "clams", "oyster",
                "oysters", "squid", "mussel", "mussels", "eel",
                "anchovy", "sardine"],
    "Soy": ["teriyaki", "tofu", "soy", "bean curd", "miso", "edamame",
            "tempeh"],
}

MEAL_TIME_KEYWORDS = {
    "Breakfast": ["breakfast"],
    "Lunch": ["lunch"],
    "Dinner": ["dinner"],
}


def parse_price(text):
    """Return an int price, or None if the value cannot be parsed."""
    cleaned = re.sub(r"[^0-9.]", "", str(text))
    try:
        value = int(float(cleaned))
    except (TypeError, ValueError):
        return None
    if value <= 0 or value > 200:
        return None
    return value


def normalise_cuisine(tag):
    tag = (tag or "").strip()
    if tag == "American (New)":
        return "American"
    if tag in ALLOWED_CUISINES:
        return tag
    return "Other"


def build_cuisine_map(reader):
    """Restaurant name -> first cuisine tag, normalised to the allowed list."""
    mapping = {}
    for row in reader:
        name = (row.get("Name") or "").strip()
        if not name or name in mapping:
            continue
        tags = [t.strip() for t in (row.get("Cuisine") or "").split(",") if t.strip()]
        mapping[name] = normalise_cuisine(tags[0]) if tags else "Other"
    return mapping


def derive_allergens(name):
    text = name.lower()
    found = []
    for allergen, words in ALLERGEN_KEYWORDS.items():
        if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in words):
            found.append(allergen)
    return found


def derive_meal_times(name):
    text = name.lower()
    for label, words in MEAL_TIME_KEYWORDS.items():
        if any(w in text for w in words):
            return [label]
    return ["Lunch", "Dinner"]


def clean():
    if not ARCHIVE.exists():
        raise SystemExit("archive.zip not found next to clean_data.py")

    with zipfile.ZipFile(ARCHIVE) as z:
        with z.open("restaurant_data.csv") as f:
            cuisine_map = build_cuisine_map(
                csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
            )
        with z.open("menu_data.csv") as f:
            menu = list(
                csv.DictReader(io.TextIOWrapper(f, encoding="utf-8", errors="replace"))
            )

    seen = set()
    meals = []
    for row in menu:
        price = parse_price(row.get("Price"))
        if price is None:
            continue

        restaurant = (row.get("Restaurant") or "").strip()
        name = (row.get("Item") or "").strip()
        if not name:
            continue

        key = (restaurant.lower(), name.lower(), price)
        if key in seen:
            continue
        seen.add(key)

        meals.append({
            "id": len(meals) + 1,
            "name": name,
            "price": price,
            "cuisine": cuisine_map.get(restaurant, "Other"),
            "allergens": derive_allergens(name),
            "meal_times": derive_meal_times(name),
        })

    return meals


def write_csv(path, meals):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "name", "price", "cuisine", "allergens", "meal_times"]
        )
        writer.writeheader()
        for meal in meals:
            writer.writerow({
                "id": meal["id"],
                "name": meal["name"],
                "price": meal["price"],
                "cuisine": meal["cuisine"],
                "allergens": "|".join(meal["allergens"]),
                "meal_times": "|".join(meal["meal_times"]),
            })


def main():
    meals = clean()
    OUT_DIR.mkdir(exist_ok=True)

    write_csv(OUT_DIR / "meals.csv", meals)
    for n in (100, 1000, 10000):
        write_csv(OUT_DIR / f"meals_{n}.csv", meals[:n])

    print(f"Cleaned {len(meals)} meals")
    for n in (100, 1000, 10000):
        print(f"  wrote meals_{n}.csv ({min(n, len(meals))} rows)")
    print(f"Output folder: {OUT_DIR}")
    print("Note: derived labels are approximate; compare with the committed CSVs.")


if __name__ == "__main__":
    main()
