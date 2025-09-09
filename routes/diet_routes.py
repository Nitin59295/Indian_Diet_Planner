# routes/diet_routes.py
from flask import Blueprint, render_template
from models import UserHistory
import json

diet_bp = Blueprint("diet", __name__)

@diet_bp.route("/my-plan")
def diet_page():
    """Fetches the most recent diet plan from the database."""
    latest_record = UserHistory.query.order_by(UserHistory.id.desc()).first()

    plan_data = None
    if latest_record and latest_record.diet_plan:
        plan_data = json.loads(latest_record.diet_plan)

    return render_template("diet.html", record=latest_record, plan_data=plan_data)


@diet_bp.route('/history')
def history():
    """Fetches all historical records from the database."""
    records = UserHistory.query.order_by(UserHistory.id.desc()).all()
    return render_template("history.html", records=records)