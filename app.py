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
    user_message = request.json["message"]
    
    # Prepare the request payload
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    }
    
    # Set up the headers
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    # Make the API request
    response = requests.post(OPENAI_API_ENDPOINT, json=payload, headers=headers)
    
    if response.status_code == 200:
        bot_response = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": bot_response})
    else:
        return jsonify({"error": "Failed to get response from OpenAI"}), 500

if __name__ == "__main__":
    app.run(debug=True)
