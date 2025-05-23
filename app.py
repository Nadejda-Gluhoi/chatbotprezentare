from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from gpt_logic import handle_user_message
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    prompt = data.get("message", "")
    name = data.get("name", "Vizitator")

    if not prompt:
        return jsonify({"reply": "Te rog, scrie un mesaj."})

    response = handle_user_message(prompt, name)
    return jsonify({"reply": response})

if __name__ == "__main__":
    app.run(debug=True)
