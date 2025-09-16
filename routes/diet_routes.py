# routes/diet_routes.py
from flask import Blueprint, render_template
# The line below was fixed by adding a '.' before 'diet_logic'
from .diet_logic import get_diet_plan
from models import UserHistory
from flask_login import login_required, current_user
import json

diet_bp = Blueprint("diet", __name__)

@diet_bp.route("/my-plan")
@login_required
def diet_page():
    latest_record = UserHistory.query.filter_by(user_id=current_user.id).order_by(UserHistory.id.desc()).first()
    
    plan_data = None
    if latest_record and latest_record.diet_plan:
        plan_data = json.loads(latest_record.diet_plan)

    return render_template("diet.html", record=latest_record, plan_data=plan_data)

@diet_bp.route('/history')
@login_required
def history():
    records = UserHistory.query.filter_by(user_id=current_user.id).order_by(UserHistory.id.desc()).all()
    return render_template("history.html", records=records)

