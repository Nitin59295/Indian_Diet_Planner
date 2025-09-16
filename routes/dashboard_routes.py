from flask import Blueprint, render_template
from flask_login import login_required

# This creates the 'dashboard' blueprint
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # This tells Flask to show the 'ai_dashboard.html' page
    return render_template('ai_dashboard.html')

