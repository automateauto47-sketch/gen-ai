import os
import json
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from google.cloud import aiplatform
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

load_dotenv()

app = Flask(__name__)
CORS(app)

# Gemini client
client = genai.Client(vertexai=True, project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1")

# Vertex AI init
vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location="us-central1",
    credentials=None
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

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
        # Step 1: Generate story with Gemini
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

        # Step 2: Generate image with Imagen
        imagen = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        images = imagen.generate_images(
            prompt=result["image_prompt"],
            number_of_images=1,
            aspect_ratio="16:9"
        )
        image_bytes = images[0]._image_bytes
        result["image_base64"] = base64.b64encode(image_bytes).decode("utf-8")

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)