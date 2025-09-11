# app.py
from flask import Flask
from models import User
from extensions import db, login_manager
from routes import user_bp, bmi_bp, diet_bp, food_bp, auth_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a-very-secure-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.cli.command("init-db")
def init_db_command():
    db.create_all()
    print("Initialized the database.")

app.register_blueprint(user_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(food_bp, url_prefix='/food')
app.register_blueprint(auth_bp)


if __name__ == "__main__":
    app.run(debug=True)