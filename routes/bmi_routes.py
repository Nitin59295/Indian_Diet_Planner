from flask import Blueprint, render_template, request
from .diet_logic import calculate_bmi, get_diet_plan
from models import db, UserHistory
from flask_login import login_required, current_user
import json

bmi_bp = Blueprint('bmi_bp', __name__)

@bmi_bp.route('/calculate-bmi', methods=['GET', 'POST'])
@login_required  
def bmi_page():
    if request.method == "POST":
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        goal = request.form['goal']

        bmi = calculate_bmi(weight, height)
        plan = get_diet_plan(current_user.id, bmi, goal)

        history_entry = UserHistory(
            name=name,
            weight=weight,
            height=height,
            bmi=bmi,
            goal=goal,
            diet_plan=json.dumps(plan),
            user_id=current_user.id  
        )
        db.session.add(history_entry)
        db.session.commit()

        return render_template("diet_result.html", name=name, bmi=bmi, plan=plan)

    return render_template("bmi.html")