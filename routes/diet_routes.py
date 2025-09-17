# calorie_app/routes/diet_routes.py
from flask import Blueprint, render_template, Response, redirect, url_for, flash
from models import db, UserHistory # Make sure to import db
from flask_login import login_required, current_user
import json
from weasyprint import HTML

diet_bp = Blueprint("diet", __name__)

@diet_bp.route("/my-plan")
@login_required
def diet_page():
    latest_record = UserHistory.query.filter_by(user_id=current_user.id).order_by(UserHistory.id.desc()).first()
    plan_data = json.loads(latest_record.diet_plan) if latest_record and latest_record.diet_plan else None
    return render_template("diet.html", record=latest_record, plan_data=plan_data)

@diet_bp.route('/history')
@login_required
def history():
    records = UserHistory.query.filter_by(user_id=current_user.id).order_by(UserHistory.id.desc()).all()
    return render_template("history.html", records=records)

@diet_bp.route('/delete-history', methods=['POST'])
@login_required
def delete_history():
    try:
        # Delete all history records for the current user
        UserHistory.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('Your history has been successfully deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting your history: {e}', 'error')
    
    return redirect(url_for('diet.history'))

@diet_bp.route('/download-plan')
@login_required
def download_plan():
    latest_record = UserHistory.query.filter_by(user_id=current_user.id).order_by(UserHistory.id.desc()).first()
    if not latest_record: return "No plan found to download.", 404

    plan_data = json.loads(latest_record.diet_plan)
    html_for_pdf = render_template('plan_pdf.html', record=latest_record, plan_data=plan_data)
    pdf = HTML(string=html_for_pdf).write_pdf()

    return Response(pdf, mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=diet_plan.pdf'})