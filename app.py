import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return jsonify({"status": "Mythos Director Backend Running ✅"})

@app.route("/generate-scene", methods=["POST"])
def generate_scene():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    system_prompt = f"""
You are an Interactive Mythos Director.
The user gives you a story prompt and you respond ONLY with a valid JSON object.

Return this exact structure:
{{
  "story": "2-3 sentence story scene",
  "image_prompt": "detailed visual description for image generation",
  "voice_script": "1-2 sentences for narration",
  "choices": ["Choice 1", "Choice 2", "Choice 3"]
}}

User prompt: {prompt}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt
        )
        text = response.text.strip()

        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]

        result = json.loads(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)