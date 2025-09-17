import os
from flask import Flask
from extensions import db, login_manager
from models import User
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)
app.config['SECRET_KEY'] = 'a-very-secure-secret-key-that-is-long'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "calorie_app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Blueprint Imports ---
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.bmi_routes import bmi_bp
from routes.diet_routes import diet_bp
from routes.food_routes import food_bp
from routes.ai_routes import ai_bp
from routes.dashboard_routes import dashboard_bp # <-- 1. ADD THIS IMPORT

# --- Blueprint Registrations ---
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(food_bp)
app.register_blueprint(ai_bp, url_prefix='/ai')
app.register_blueprint(dashboard_bp) # <-- 2. ADD THIS LINE TO REGISTER IT

@app.cli.command("init-db")
def init_db_command():
    with app.app_context():
        db.create_all()
    print("Initialized the database successfully.")

if __name__ == "__main__":
    app.run(debug=True)

