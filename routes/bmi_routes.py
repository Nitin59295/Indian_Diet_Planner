from flask import Blueprint, render_template, request

bmi_bp = Blueprint("bmi", __name__)

@bmi_bp.route("/bmi", methods=["GET", "POST"])
def bmi_form():
    bmi = None
    category = None

    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"]) / 100  # convert cm → meters
        bmi = round(weight / (height ** 2), 2)

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

    return render_template("bmi.html", bmi=bmi, category=category)
