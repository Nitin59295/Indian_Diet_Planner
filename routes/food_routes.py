# routes/food_routes.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models import db, Food # <-- Import the Food model, not the old dictionary

food_bp = Blueprint('food_bp', __name__)

@food_bp.route('/list', methods=['GET'])
def list_foods():
    """Returns a JSON list of all foods from the database."""
    all_foods = Food.query.all()
    # Convert the list of Food objects into a list of dictionaries
    foods_dict = [
        {
            "name": food.name,
            "calories": food.calories,
            "protein": food.protein,
            "carbs": food.carbs,
            "fat": food.fat,
            "sugar": food.sugar
        }
        for food in all_foods
    ]
    return jsonify(foods_dict)

@food_bp.route('/suggest', methods=['POST'])
def suggest_foods():
    """Suggests a meal plan based on a calorie target using foods from the database."""
    data = request.get_json()
    calorie_needs = data.get("calories", 2000)

    # Get all foods from the database
    all_foods = Food.query.all()
    
    plan = []
    total_calories = 0

    for food in all_foods:
        if total_calories + food.calories <= calorie_needs:
            plan.append(food.name)
            total_calories += food.calories

    return jsonify({
        "calorie_goal": calorie_needs,
        "suggested_meals": plan,
        "total_calories": total_calories
    })

@food_bp.route('/add', methods=['GET', 'POST'])
def add_food():
    """Handles adding a new food item to the database."""
    if request.method == 'POST':
        new_food = Food(
            name=request.form['name'],
            calories=float(request.form['calories']),
            protein=float(request.form['protein']),
            carbs=float(request.form['carbs']),
            fat=float(request.form['fat']),
            sugar=float(request.form['sugar'] or 0) # Default to 0 if empty
        )
        db.session.add(new_food)
        db.session.commit()
        # Redirect to a page showing all foods, which we can create or reuse
        return redirect(url_for('user.index'))
        
    return render_template('add_food.html')