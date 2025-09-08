Calorie Tracker & Diet Planner 🥗
A dynamic web application built with Flask that allows users to calculate their Body Mass Index (BMI), receive personalized diet plans with detailed nutritional information, and track their history.

✨ Features
BMI Calculation: Users can input their name, weight, and height to get an accurate BMI calculation.

Dynamic Diet Plans: Based on the user's BMI and goals (weight loss, maintenance, or muscle gain), the app generates a unique diet plan.

Detailed Nutrition: Each diet plan includes an estimated daily total for calories, protein, carbs, fat, and sugar.

Custom Food Database: Users can add their own food items with detailed nutritional information to a persistent database.

User History: The application saves every BMI calculation and generated plan, allowing users to track their progress over time.

Interactive Frontend: A modern, responsive user interface with a hero image, smooth animations, and icons for a better user experience.

🛠️ Technologies Used
Backend: Python, Flask

Database: Flask-SQLAlchemy (with SQLite)

Frontend: HTML, CSS, Jinja2

Icons: Bootstrap Icons

📂 Project Structure
calorie_app/
├── app.py                  # Main Flask app entry point
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
│
├── routes/                 # All route blueprints
│   ├── bmi_routes.py       # Handles BMI calculation
│   ├── diet_logic.py       # Core logic for generating diet plans
│   ├── diet_routes.py      # Handles viewing plans and history
│   └── food_routes.py      # Handles adding and listing foods
│
├── static/                 # Static files (CSS, images)
│   ├── css/style.css
│   └── hero-image.jpg
│
└── templates/              # HTML files for rendering
    ├── base.html           # Common layout (header/footer)
    ├── index.html          # Homepage
    ├── bmi.html            # BMI form page
    ├── diet_result.html    # Diet results page
    ├── diet.html           # 'My Latest Plan' page
    ├── history.html        # User history page
    └── add_food.html       # Form to add custom foods
🚀 Setup and Installation
Follow these steps to get the application running on your local machine.

1. Clone the Repository
Bash

git clone <your-repository-url>
cd calorie_app
2. Create and Activate a Virtual Environment
Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
macOS / Linux:

Bash

python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Install all the required Python packages from the requirements.txt file.

Bash

pip install -r requirements.txt
▶️ Usage
1. Initialize the Database
Before running the app for the first time, you need to create the database and its tables. Run the following commands in your terminal:

Windows (Command Prompt):

Bash

set FLASK_APP=app.py
flask init-db
Windows (PowerShell):

Bash

$env:FLASK_APP = "app.py"
flask init-db
macOS / Linux:

Bash

export FLASK_APP=app.py
flask init-db
You should see a confirmation message: Initialized the database.

2. Run the Application
Start the Flask development server:

Bash

python app.py
The application will be running at http://127.0.0.1:5000. Open this URL in your web browser to use the app.
