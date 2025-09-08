from flask import Flask
from routes.bmi_routes import bmi_bp
from routes.diet_routes import diet_bp
from routes.user_routes import user_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(diet_bp)

if __name__ == "__main__":
    app.run(debug=True)
