import os
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    
    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    
    bot_response = response.choices[0].message.content
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
