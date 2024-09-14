import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# OpenAI API endpoint
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Prepare the request payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    
    # Set up the headers
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return jsonify({"error": "OpenAI API key not found"}), 500

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the API request
        response = requests.post(OPENAI_API_ENDPOINT, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        bot_response = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get response from OpenAI: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
