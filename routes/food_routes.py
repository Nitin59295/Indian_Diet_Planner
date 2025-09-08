from flask import Blueprint, request, jsonify

food_bp = Blueprint('food_bp', __name__)

# Sample Indian food dataset (per serving in calories)
indian_foods = {
    "roti": 120,
    "rice": 200,
    "dal": 150,
    "paneer curry": 250,
    "chicken curry": 300,
    "sambar": 180,
    "idli": 70,
    "dosa": 160,
    "upma": 180,
    "poha": 160,
    "curd": 100,
    "milk": 90,
    "banana": 105,
    "apple": 80
}

# Route: List all foods
@food_bp.route('/list', methods=['GET'])
def list_foods():
    return jsonify(indian_foods)

# Route: Suggest diet plan based on calorie needs
@food_bp.route('/suggest', methods=['POST'])
def suggest_foods():
    data = request.get_json()
    calorie_needs = data.get("calories", 2000)

    plan = []
    total = 0

    # Simple greedy suggestion: keep adding foods until calories reached
    for food, cal in indian_foods.items():
        if total + cal <= calorie_needs:
            plan.append(food)
            total += cal

    return jsonify({
        "calorie_goal": calorie_needs,
        "suggested_meals": plan,
        "total_calories": total
    })
