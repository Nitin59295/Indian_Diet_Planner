from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Food
from flask_login import login_required, current_user

food_bp = Blueprint('food_bp', __name__)

@food_bp.route('/list', methods=['GET'])
@login_required
def list_foods():
    user_foods = Food.query.filter_by(user_id=current_user.id).all()
    foods_dict = [
        {"name": food.name, "calories": food.calories, "protein": food.protein, "carbs": food.carbs, "fat": food.fat, "sugar": food.sugar}
        for food in user_foods
    ]
    return jsonify(foods_dict)

@food_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_food():
    if request.method == 'POST':
        new_food = Food(
            name=request.form['name'],
            calories=float(request.form['calories']),
            protein=float(request.form['protein']),
            carbs=float(request.form['carbs']),
            fat=float(request.form['fat']),
            sugar=float(request.form['sugar'] or 0),
            user_id=current_user.id  
        )
        db.session.add(new_food)
        db.session.commit()
        # --- IMPROVED UX ---
        flash(f"'{new_food.name}' was successfully added to your food list!")
        return redirect(url_for('food_bp.add_food'))
        
    return render_template('add_food.html')