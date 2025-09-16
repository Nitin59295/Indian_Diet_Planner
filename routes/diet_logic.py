from models import Food, User

default_indian_foods = {
    "roti": {"calories": 120, "protein": 4, "carbs": 25, "fat": 1, "sugar": 1, "image": "foods/roti.jpg"},
    "rice": {"calories": 200, "protein": 4, "carbs": 45, "fat": 0.5, "sugar": 0, "image": "foods/rice.jpg"},
    "dal": {"calories": 150, "protein": 9, "carbs": 25, "fat": 2, "sugar": 2, "image": "foods/dal.jpg"},
    "paneer curry": {"calories": 250, "protein": 18, "carbs": 8, "fat": 16, "sugar": 5, "image": "foods/paneer_curry.jpg"},
    "chicken curry": {"calories": 300, "protein": 25, "carbs": 7, "fat": 18, "sugar": 4, "image": "foods/chicken_curry.jpg"},
    "sambar": {"calories": 180, "protein": 8, "carbs": 30, "fat": 3, "sugar": 7, "image": "foods/sambar.jpg"},
    "idli": {"calories": 70, "protein": 2, "carbs": 16, "fat": 0.2, "sugar": 0, "image": "foods/idli.jpg"},
    "dosa": {"calories": 160, "protein": 3, "carbs": 30, "fat": 3, "sugar": 1, "image": "foods/dosa.jpg"},
    "upma": {"calories": 180, "protein": 4, "carbs": 35, "fat": 2, "sugar": 2, "image": "foods/upma.jpg"},
    "poha": {"calories": 160, "protein": 3, "carbs": 33, "fat": 1.5, "sugar": 4, "image": "foods/poha.jpg"},
    "curd": {"calories": 100, "protein": 11, "carbs": 10, "fat": 2, "sugar": 9, "image": "foods/curd.jpg"},
    "milk": {"calories": 90, "protein": 5, "carbs": 8, "fat": 3, "sugar": 8, "image": "foods/milk.jpg"},
    "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4, "sugar": 14, "image": "foods/banana.jpg"},
    "apple": {"calories": 80, "protein": 0.5, "carbs": 22, "fat": 0.3, "sugar": 18, "image": "foods/apple.jpg"}
}

def calculate_bmi(weight, height):
    if height <= 0: return 0
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def generate_dynamic_meals(calorie_target, user_id):
    meal_plan = {"breakfast": [], "lunch": [], "dinner": []}
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "sugar": 0}
    user_foods = Food.query.filter_by(user_id=user_id).all()
    user_food_dict = {
        food.name: {
            "calories": food.calories, "protein": food.protein,
            "carbs": food.carbs, "fat": food.fat, "sugar": food.sugar,
            "image": "foods/custom.png"
        } for food in user_foods
    }
    
    food_source = {}
    if not user_food_dict: food_source = default_indian_foods
    elif len(user_food_dict) < 10:
        food_source = default_indian_foods.copy()
        food_source.update(user_food_dict)
    else: food_source = user_food_dict

    sorted_foods = sorted(food_source.items(), key=lambda item: item[1]['protein'], reverse=True)
    meal_targets = {"breakfast": calorie_target * 0.3, "lunch": calorie_target * 0.4, "dinner": calorie_target * 0.3}
    used_foods = set()

    for meal, target in meal_targets.items():
        current_meal_calories = 0
        for food_name, details in sorted_foods:
            if food_name not in used_foods and current_meal_calories + details['calories'] <= target:
                food_details = details.copy()
                food_details['name'] = food_name
                meal_plan[meal].append(food_details)
                for key in totals:
                    if key in details: totals[key] += details[key]
                current_meal_calories += details['calories']
                used_foods.add(food_name)

    for key in totals: totals[key] = round(totals[key], 1)
    return meal_plan, totals

def get_diet_plan(user_id, bmi, goal="maintain"):
    if bmi < 18.5: category, calories = "Underweight", 2500
    elif 18.5 <= bmi < 24.9: category, calories = "Normal", 2200
    elif 25 <= bmi < 29.9: category, calories = "Overweight", 1800
    else: category, calories = "Obese", 1500

    if goal == "gain": calories += 500
    elif goal == "lose": calories -= 500

    meal_breakdown, nutrition_totals = generate_dynamic_meals(calories, user_id)
    timed_meal_plan = [
        {"time": "08:00 AM", "name": "Breakfast", "foods": meal_breakdown.get("breakfast", [])},
        {"time": "01:00 PM", "name": "Lunch", "foods": meal_breakdown.get("lunch", [])},
        {"time": "07:00 PM", "name": "Dinner", "foods": meal_breakdown.get("dinner", [])},
    ]

    return {
        "category": category,
        "calories": calories,
        "meals": timed_meal_plan,
        "totals": nutrition_totals
    }