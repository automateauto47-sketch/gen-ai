import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from ai_engine import generate_scene_package

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({"status": "Mythos Director Backend Running ✅"})


@app.route("/generate-scene", methods=["POST"])
def generate_scene():
    data = request.get_json()
    prompt = data.get("prompt", "")
    history = data.get("history", [])

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        result = generate_scene_package(prompt, history)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
