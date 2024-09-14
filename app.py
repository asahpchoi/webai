import os
import requests
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API endpoints
OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
SAMBANOVA_API_ENDPOINT = "https://api.sambanova.ai/v1/chat/completions"  # Replace with actual endpoint

@app.route("/")
def home():
    return render_template("index.html", token_usage=None, response_time=None)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    model = request.json.get("model")
    if not user_message or not model:
        return jsonify({"error": "No message or model provided"}), 400

    # Prepare the request payload
    payload = {
        "model": "gpt-4o-mini" if model == "openai" else "Meta-Llama-3.1-405B-Instruct",  # Replace with actual SambaNova model name
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
        # Record start time
        start_time = time.time()

        # Make the API request
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Record end time
        end_time = time.time()
        
        # Calculate response time
        response_time = end_time - start_time
        
        # Extract response data
        response_data = response.json()
        bot_response = response_data["choices"][0]["message"]["content"]
        
        # Extract token usage
        token_usage = response_data.get("usage", {})
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", 0)
        
        return jsonify({
            "response": bot_response,
            "response_time": round(response_time, 2),
            "token_usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }
        }), 200, {'Content-Type': 'application/json'}
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to get response from {model.capitalize()}: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
