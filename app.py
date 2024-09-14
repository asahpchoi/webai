import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API endpoints
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
SAMBANOVA_API_ENDPOINT = "https://api.sambanova.ai/chat/completions"  # Replace with actual endpoint

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    model = request.json.get("model")
    if not user_message or not model:
        return jsonify({"error": "No message or model provided"}), 400

    # Prepare the request payload
    payload = {
        "model": "gpt-4o-mini" if model == "openai" else "sambanova-model",  # Replace with actual SambaNova model name
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    
    # Set up the headers and endpoint based on the selected model
    if model == "openai":
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return jsonify({"error": "OpenAI API key not found"}), 500
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        api_endpoint = OPENAI_API_ENDPOINT
    else:  # SambaNova
        api_key = os.environ.get('SAMBANOVA_API_KEY')
        if not api_key:
            return jsonify({"error": "SambaNova API key not found"}), 500
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        api_endpoint = SAMBANOVA_API_ENDPOINT
    
    try:
        # Make the API request
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        bot_response = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get response from {model.capitalize()}: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
