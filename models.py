# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserHistory(db.Model):
    # ... (this class remains the same) ...
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    goal = db.Column(db.String(20))
    diet_plan = db.Column(db.Text)

# --- ADD THIS NEW MODEL ---
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    sugar = db.Column(db.Float, nullable=True) # Making sugar optional