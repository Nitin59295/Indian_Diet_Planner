import os
import requests
import json
from flask import Blueprint, request, jsonify

ai_bp = Blueprint('ai', __name__)

# FIX: Switched to a different, reliable open-source model
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

@ai_bp.route("/recommend-meal", methods=["POST"])
def recommend_meal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    calories = data.get("calories")
    protein = data.get("protein")

    api_token = os.getenv("HF_API_TOKEN")
    if not api_token:
        return jsonify({"error": "API token not configured"}), 500
    
    headers = {"Authorization": f"Bearer {api_token}"}

    prompt = (
        f"You are an expert Indian nutritionist. A user needs a recommendation for a meal. "
        f"They have approximately {calories} calories and {protein}g of protein remaining for the day. "
        f"Recommend a single, healthy, and common Indian meal that fits these targets. "
        f"Your response must be ONLY a JSON object with the keys 'meal_name', 'calories', "
        f"'protein', 'carbs', and 'fat', with appropriate numerical values."
    )
    
    # The payload structure is slightly different for this model
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {"max_new_tokens": 150}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 503:
            return jsonify({"error": "AI model is loading, please try again in a moment."}), 503
        
        response.raise_for_status()
        
        result = response.json()
        generated_text = result[0]['generated_text']
        
        # Extract the JSON part of the response
        json_part = generated_text.split("[/INST]")[-1].strip()
        
        meal_recommendation = json.loads(json_part)
        
        return jsonify(meal_recommendation)

    except requests.exceptions.RequestException as e:
        # Provide a more specific error for 404
        if e.response and e.response.status_code == 404:
            return jsonify({"error": "The AI model was not found. The service might be temporarily down."}), 404
        return jsonify({"error": f"API request failed: {e}"}), 500
    except (json.JSONDecodeError, KeyError, IndexError):
        return jsonify({"error": "Failed to parse AI response. The model may have returned an invalid format."}), 500

