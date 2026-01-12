import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai

# --- Configuration & Setup ---

# 1. Load API Key from environment variable for security
# It's crucial to set this variable in your environment, e.g., using `export GEMINI_API_KEY='your_key'` in the terminal.
API_KEY = os.environ.get('AIzaSyBn_h2jDTcOB0s17TH-iVHQHue8Phh1ck8')


genai.configure(api_key=API_KEY)
app = Flask(__name__)

# --- Helper Function for Gemini API Interaction ---

def get_date_plan(location, date_time, mood):
    """
    Generates a creative date plan using the Gemini API with a three-part itinerary.

    Args:
        location (str): The user's current city or location.
        date_time (str): The desired date and time for the date.
        mood (str): The preferred mood or theme, chosen from a predefined list.

    Returns:
        str: The markdown-formatted date plan.
    """
    # 2. Enhanced prompt for a three-part date plan
    prompt = f"""
    You are a creative date planner assistant. Generate a detailed, engaging, and fun date plan for a single user.

    Here is the user's information:
    - **Current Location:** {location}
    - **Desired Date and Time:** {date_time}
    - **Preferred Mood/Theme:** {mood}

    The plan must include:
    1. A catchy and fun name for the date.
    2. A detailed itinerary with three distinct parts:
        - The Meet-Up: A low-key starting point.
        - The Main Event: The primary activity or location.
        - The Nightcap: A relaxing or memorable way to end the date.
    3. For each location, provide:
        - The type of place (e.g., "Italian Restaurant," "Art Museum").
        - A short, creative description explaining why it fits the mood.
    4. A fun, short note about the weather to check. This should be a creative guess, not real data.

    The entire output must be formatted using markdown with clear headings, bolded text, and easy readability.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# --- Flask Routes and Endpoints ---

@app.route('/')
def index():
    """Serves the main HTML file for the application."""
    return send_from_directory('.', 'index_1.html')

@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate a date plan based on user input."""
    # 5. More robust error handling
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON input"}), 400

        location = data.get('location')
        date_time = data.get('date_time')
        mood = data.get('mood')

        if not all([location, date_time, mood]):
            return jsonify({"error": "Missing required fields: 'location', 'date_time', and 'mood'"}), 400

        date_plan_text = get_date_plan(location, date_time, mood)
        return jsonify({'plan': date_plan_text})

    except Exception as e:
        # Catch and return a generic server-side error message
        print(f"An error occurred: {e}")
        return jsonify({"error": "A server-side error occurred. Please try again later."}), 500

# --- Server Execution ---

# 4. Use a main block for proper server execution
if __name__ == "__main__":
    # In a production environment, set debug to False
    app.run(debug=True)