from models import Food 

def calculate_bmi(weight, height):
    if height <= 0:
        return 0
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def generate_dynamic_meals(calorie_target, user_id):

    meal_plan = {"breakfast": [], "lunch": [], "dinner": []}
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}

    # --- KEY CHANGE: Fetch foods for the specific user from the database ---
    user_foods = Food.query.filter_by(user_id=user_id).all()
    
    if not user_foods:
        return meal_plan, totals

    foods_list = []
    for food in user_foods:
        foods_list.append({
            "name": food.name,
            "calories": food.calories,
            "protein": food.protein,
            "carbs": food.carbs,
            "fat": food.fat,
            "sugar": food.sugar
        })

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
                meal_plan[meal].append(food_details['name'])

                totals['calories'] += food_details['calories']
                totals['protein'] += food_details['protein']
                totals['carbs'] += food_details['carbs']
                totals['fat'] += food_details['fat']
                totals['sugar'] += food_details['sugar']

                current_meal_calories += food_details['calories']
                used_foods.add(food_details['name'])

    for key in totals:
        totals[key] = round(totals[key], 1)

    return meal_plan, totals

def get_diet_plan(user_id, bmi, goal="maintain"):
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

    diet_plan, nutrition_totals = generate_dynamic_meals(calories, user_id)

    return {
        "category": category,
        "calories": calories,
        "meals": diet_plan,
        "totals": nutrition_totals
    }