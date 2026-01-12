import google.generativeai as genai
import os
from flask import Flask, request, jsonify, send_from_directory

# ... (rest of your imports)

api_key = "paste your API key here"

# ------------------------------------------------------------------
# 💡 FIX: Set the API endpoint explicitly.
# ------------------------------------------------------------------
genai.configure(
    api_key=api_key,
    transport='rest',  # Ensure it uses the REST transport
    # Set the endpoint to the default public endpoint
    # This is crucial for accessing models outside of a Google Cloud Project region.
    client_options={'api_endpoint': 'https://generativelanguage.googleapis.com'} 
)
# ------------------------------------------------------------------

app = Flask(__name__)

# ... (rest of your functions and routes)
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
    You are a creative date planner for two lovers. Generate a detailed, engaging, and fun dating plan for lovers based on the following information:
    - **Current Location:** {location}
    - **Desired Date and Time:** {date_time}
    - **Preferred Mood/Theme:** {mood}
    
    The plan must include:
    first of check if the data is correct like the date is not expired or the location is valid. (dont show the user this)
    1. A catchy and fun name for the date.
    2. A detailed itinerary with a few distinct activities or locations.
    3. For each activity, use a level 2 markdown heading (##) for clear separation, and include:
        - The type of place (e.g., "Italian Restaurant," "Art Museum").
        - A short, creative description explaining why it fits the mood.
    4. A fun, short note about the weather to check. This should be a creative guess, not real data.

    The entire output must be formatted using markdown for clear headings, bolded text, and easy readability.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

## Flask Routes

@app.route('/')
def index():
    """Serves the xindex.html (Credits page)."""
    # Assumes index.html is in the same directory as this Python file.
    return send_from_directory('.', 'xindex.html')

@app.route('/main_project.html')
def main_project():
    """Serves the xmain_project.html (Date Plan Generator)."""
    # Assumes xmain_project.html is in the same directory as this Python file.
    return send_from_directory('.', 'xmain_project.html')

@app.route('/generate', methods=['POST'])
def generate():
    """API endpoint to generate a date plan by calling the Gemini API."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input: No JSON data received"}), 400

    location = data.get('location')
    date_time = data.get('date_time')
    mood = data.get('mood')

    if not all([location, date_time, mood]):
        return jsonify({"error": "Missing required fields: location, date_time, or mood"}), 400

    try:
        # Call the function to get the date plan from Gemini
        date_plan_text = get_date_plan(location, date_time, mood)
        return jsonify({'plan': date_plan_text})
    except Exception as e:
        # Log the detailed error (for debugging) and return a generic error message
        print(f"Error during plan generation: {e}")
        return jsonify({"error": "An internal server error occurred while generating the plan. Please check the API key and connection."}), 500

# Add routes for the image files so they load correctly on the credit page
@app.route('/<filename>')
def serve_file(filename):
    """Serves static files (like images)."""
    # This serves files like IMG_20250905_134745096 (1).jpg
    return send_from_directory('.', filename)

if __name__ == "__main__":
    # Ensure all HTML and image files are in the same folder as this Python script.
    app.run(debug=True)