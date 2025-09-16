# calorie_app/routes/ai_routes.py

import os
import json
from flask import Blueprint, request, jsonify
import google.generativeai as genai

ai_bp = Blueprint('ai', __name__)

# --- Configure the Gemini API ---
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Warning: Gemini API key not found in .env file.")
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
# -----------------------------

@ai_bp.route("/recommend-meal", methods=["POST"])
def recommend_meal():
    data = request.get_json()
    if not data: return jsonify({"error": "Invalid input"}), 400
    calories, protein = data.get("calories"), data.get("protein")

    prompt = (
        f"You are an expert Indian nutritionist. A user has {calories} calories and {protein}g of protein "
        f"remaining for the day. Recommend a single, healthy, and common Indian meal that fits these targets. "
        f"Provide ONLY the JSON object with keys 'meal_name', 'calories', 'protein', 'carbs', and 'fat'."
    )
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        return jsonify(json.loads(response.text))
    except Exception as e:
        return jsonify({"error": f"An error occurred with the Gemini API: {e}"}), 500

@ai_bp.route("/analyze-meal", methods=["POST"])
def analyze_meal():
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    description = data.get("description")
    prompt = (
        f"You are a nutritional analysis expert. Analyze the following meal description and estimate its nutritional content. "
        f"Meal: '{description}'. "
        f"Your response must be ONLY a JSON object with keys 'total_calories', 'total_protein', 'total_carbs', and 'total_fat', with estimated numerical values."
    )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        return jsonify(json.loads(response.text))
    except Exception as e:
        return jsonify({"error": f"An error occurred with the Gemini API: {e}"}), 500

@ai_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
    if not data or 'calories' not in data:
        return jsonify({"error": "Invalid input"}), 400

    calories = data.get('calories')
    preference = data.get('preference', 'a standard balanced diet') # Default preference

    prompt = (
        f"You are an expert diet planner. Generate a full day Indian meal plan for a target of {calories} calories, "
        f"following a preference for '{preference}'. "
        f"Your response must be ONLY a JSON object. The top-level keys must be 'breakfast', 'lunch', and 'dinner'. "
        f"Each of these keys should contain a list of food objects. Each food object must have keys 'name' (string), 'calories' (integer), and 'protein' (integer)."
    )

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        config = genai.GenerationConfig(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=config)
        return jsonify(json.loads(response.text))
    except Exception as e:
        return jsonify({"error": f"An error occurred with the Gemini API: {e}"}), 500

# --- NEW ENDPOINT: ASK ANYTHING CHATBOT ---
@ai_bp.route("/ask-anything", methods=["POST"])
def ask_anything():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    question = data.get("question")
    prompt = (
        f"You are a friendly and knowledgeable nutritionist specializing in Indian diets. A user has a question. "
        f"Provide a clear, helpful, and concise answer in plain text. Do not use markdown or JSON formatting. "
        f"The user's question is: '{question}'"
    )

    try:
        # Note: We do NOT use JSON mode here because we want a conversational text answer.
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        # We wrap the plain text answer in a JSON object for the frontend.
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": f"An error occurred with the Gemini API: {e}"}), 500