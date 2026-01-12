import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_from_directory
api_key ="AIzaSyA6dl9aW2FWn6dBRkr53_L0v4-8T9NRJuI"

genai.configure(api_key=api_key)


app = Flask(__name__)

def get_date_plan(location, date_time, mood):
    """
    Generates a creative date plan using the Gemini API.

    Args:
        location (str): The user's current city or location.
        date_time (str): The desired date and time for the date.
        mood (str): The preferred mood or theme.

    Returns:
        str: The markdown-formatted date plan.
    """
    prompt = f"""
    You are a creative date planner for lovers assistant. Generate a detailed, engaging, and fun date plan for lovers based on the following information:
    - **Current Location:** {location}
    - **Desired Date and Time:** {date_time}
    - **Preferred Mood/Theme:** {mood}
    
    The plan must include:
    1. A catchy and fun name for the date.
    2. A detailed itinerary with a few distinct activities or locations.
    3. For each location:
        - The type of place (e.g., "Italian Restaurant," "Art Museum").
        - A short, creative description explaining why it fits the mood.
    4. A fun, short note about the weather to check. This should be a creative guess, not real data.

    The entire output must be formatted using markdown for clear headings, bolded text, and easy readability.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return send_from_directory('.', 'index_1.html')

@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate a date plan."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    location = data.get('location')
    date_time = data.get('date_time')
    mood = data.get('mood')

    if not all([location, date_time, mood]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        date_plan_text = get_date_plan(location, date_time, mood)
        return jsonify({'plan': date_plan_text})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)