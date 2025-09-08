from flask import Blueprint, render_template, request

diet_bp = Blueprint("diet", __name__)

@diet_bp.route("/diet", methods=["GET", "POST"])
def diet_page():
    diet_plan = None

    if request.method == "POST":
        goal = request.form["goal"]

        if goal == "lose":
            diet_plan = ["Oats + Fruits", "Salad + Grilled Chicken", "Soup + Vegetables"]
        elif goal == "maintain":
            diet_plan = ["Rice + Dal + Vegetables", "Chapati + Paneer", "Milk + Nuts"]
        elif goal == "gain":
            diet_plan = ["Eggs + Peanut Butter", "Chicken + Rice", "Protein Shake + Nuts"]

    return render_template("diet.html", diet_plan=diet_plan)
