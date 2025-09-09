from models import Food # Import the Food model from the database

def calculate_bmi(weight, height):
    """Calculates Body Mass Index (BMI)."""
    if height <= 0:
        return 0
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def generate_dynamic_meals(calorie_target):
 
    meal_plan = {"breakfast": [], "lunch": [], "dinner": []}
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}

    # --- KEY CHANGE: Fetch all food items directly from the database ---
    all_foods_from_db = Food.query.all()
    
    # If there are no foods in the database, return empty results
    if not all_foods_from_db:
        return meal_plan, totals

    # Convert the list of Food objects into a list of dictionaries for easier processing
    foods_list = []
    for food in all_foods_from_db:
        foods_list.append({
            "name": food.name,
            "calories": food.calories,
            "protein": food.protein,
            "carbs": food.carbs,
            "fat": food.fat,
            "sugar": food.sugar
        })

    # Sort foods by protein content for better meal composition
    sorted_foods = sorted(foods_list, key=lambda item: item['protein'], reverse=True)

    meal_targets = {
        "breakfast": calorie_target * 0.3,
        "lunch": calorie_target * 0.4,
        "dinner": calorie_target * 0.3
    }

    used_foods = set()

    for meal, target in meal_targets.items():
        current_meal_calories = 0
        for food_details in sorted_foods:
            if food_details['name'] not in used_foods and current_meal_calories + food_details['calories'] <= target:
                # Add food to the meal
                meal_plan[meal].append(food_details['name'])

                # Add its nutritional values to the daily total
                totals['calories'] += food_details['calories']
                totals['protein'] += food_details['protein']
                totals['carbs'] += food_details['carbs']
                totals['fat'] += food_details['fat']
                totals['sugar'] += food_details['sugar']

                current_meal_calories += food_details['calories']
                used_foods.add(food_details['name'])

    # Round totals for cleaner display
    for key in totals:
        totals[key] = round(totals[key], 1)

    return meal_plan, totals

def get_diet_plan(bmi, goal="maintain"):
    """Generates a diet plan based on BMI, user goal, and detailed nutritional data."""
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

    # Generate the dynamic meal plan and get the nutritional totals
    diet_plan, nutrition_totals = generate_dynamic_meals(calories)

    return {
        "category": category,
        "calories": calories,
        "meals": diet_plan,
        "totals": nutrition_totals
    }