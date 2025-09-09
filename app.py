from flask import Flask
from models import db
from routes.user_routes import user_bp
from routes.bmi_routes import bmi_bp
from routes.diet_routes import diet_bp
from routes.food_routes import food_bp

# Create the Flask application instance
app = Flask(__name__)

# --- Configuration ---
app.config['SECRET_KEY'] = 'a-very-secure-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Extensions ---
db.init_app(app)

# --- Define a CLI command to create the database tables ---
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    db.create_all()
    print("Initialized the database.")

# --- Register Blueprints ---
app.register_blueprint(user_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(food_bp, url_prefix='/api/food')

# --- Run the App ---
if __name__ == "__main__":
    app.run(debug=True)