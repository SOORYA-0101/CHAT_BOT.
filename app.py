import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

app = Flask(__name__)
# Enable CORS for all routes, allowing the frontend to communicate with the backend
CORS(app)

# Initialize Gemini API client
gemini_api_key = os.getenv("GEMINI_API_KEY")
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)

@app.route('/')
def home():
    return send_from_directory('.', 'ASHU_AI.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Fetch dynamically to avoid global caching issues
    current_key = os.getenv("GEMINI_API_KEY")

    if not current_key:
        return jsonify({"error": "Gemini API key is missing. Please add it to the .env file."}), 500

    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Pass the key dynamically for this specific request
        genai.configure(api_key=current_key)
        
        print(f"DEBUG: Processing request using API Key starting with: {current_key[:10]}...")
        
        # We use the gemini-flash-latest model as it has better free tier limits and stability
        model = genai.GenerativeModel('gemini-flash-latest', 
            system_instruction="You are ASHUU AI, a professional and helpful study companion. You help students with their academic queries in a concise, structured, and pedagogical manner. Format your responses using markdown when appropriate."
        )
        
        response = model.generate_content(user_message)
        bot_reply = response.text
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("Error connecting to Gemini:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting ASHUU AI Backend on http://0.0.0.0:5000")
    # Bind to 0.0.0.0 to allow network access
    app.run(host='0.0.0.0', debug=True, port=5000)
