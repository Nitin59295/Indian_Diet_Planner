from models import Food, User # We need the User model to check for the user

# --- NEW: Default Food Data ---
# This list will be used as a fallback if a user has no custom foods.
default_indian_foods = {
    "roti": {"calories": 120, "protein": 4, "carbs": 25, "fat": 1, "sugar": 1},
    "rice": {"calories": 200, "protein": 4, "carbs": 45, "fat": 0.5, "sugar": 0},
    "dal": {"calories": 150, "protein": 9, "carbs": 25, "fat": 2, "sugar": 2},
    "paneer curry": {"calories": 250, "protein": 18, "carbs": 8, "fat": 16, "sugar": 5},
    "chicken curry": {"calories": 300, "protein": 25, "carbs": 7, "fat": 18, "sugar": 4},
    "sambar": {"calories": 180, "protein": 8, "carbs": 30, "fat": 3, "sugar": 7},
    "idli": {"calories": 70, "protein": 2, "carbs": 16, "fat": 0.2, "sugar": 0},
    "dosa": {"calories": 160, "protein": 3, "carbs": 30, "fat": 3, "sugar": 1},
    "upma": {"calories": 180, "protein": 4, "carbs": 35, "fat": 2, "sugar": 2},
    "poha": {"calories": 160, "protein": 3, "carbs": 33, "fat": 1.5, "sugar": 4},
    "curd": {"calories": 100, "protein": 11, "carbs": 10, "fat": 2, "sugar": 9},
    "milk": {"calories": 90, "protein": 5, "carbs": 8, "fat": 3, "sugar": 8},
    "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4, "sugar": 14},
    "apple": {"calories": 80, "protein": 0.5, "carbs": 22, "fat": 0.3, "sugar": 18}
}


def calculate_bmi(weight, height):
    """Calculates Body Mass Index (BMI)."""
    if height <= 0:
        return 0
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)


def generate_dynamic_meals(calorie_target, user_id):
    """
    Creates a meal plan. It prioritizes a user's custom foods, but
    falls back to a default list if the user has none.
    """
    meal_plan = {"breakfast": [], "lunch": [], "dinner": []}
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}
    
    # --- KEY CHANGE: Check for user's custom foods ---
    user_foods = Food.query.filter_by(user_id=user_id).all()
    
    food_source = {}
    
    if user_foods:
        # If the user has custom foods, convert them to the dictionary format we need
        for food in user_foods:
            food_source[food.name] = {
                "calories": food.calories, "protein": food.protein,
                "carbs": food.carbs, "fat": food.fat, "sugar": food.sugar
            }
    else:
        # If the user has no custom foods, use the default list
        food_source = default_indian_foods

    # Sort foods by protein content for better meal composition
    sorted_foods = sorted(food_source.items(), key=lambda item: item[1]['protein'], reverse=True)

    meal_targets = {
        "breakfast": calorie_target * 0.3,
        "lunch": calorie_target * 0.4,
        "dinner": calorie_target * 0.3
    }

    used_foods = set()

    for meal, target in meal_targets.items():
        current_meal_calories = 0
        for food_name, details in sorted_foods:
            if food_name not in used_foods and current_meal_calories + details['calories'] <= target:
                meal_plan[meal].append(food_name)

                # Add its nutritional values to the daily total
                for key in totals:
                    totals[key] += details[key]

                current_meal_calories += details['calories']
                used_foods.add(food_name)

    # Round totals for cleaner display
    for key in totals:
        totals[key] = round(totals[key], 1)

    return meal_plan, totals


def get_diet_plan(user_id, bmi, goal="maintain"):
    """Generates a diet plan based on BMI, user goal, and available food data."""
    if bmi < 18.5:
        category = "Underweight"
        calories = 2500
    elif 18.5 <= bmi < 24.9:
        category = "Normal"
        calories = 2200
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        calories = 1800
    else:
        category = "Obese"
        calories = 1500

    if goal == "gain":
        calories += 500
    elif goal == "lose":
        calories -= 500

    # Generate the dynamic meal plan using the user's ID
    diet_plan, nutrition_totals = generate_dynamic_meals(calories, user_id)

    return {
        "category": category,
        "calories": calories,
        "meals": diet_plan,
        "totals": nutrition_totals
    }
