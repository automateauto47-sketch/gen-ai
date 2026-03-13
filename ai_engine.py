import os
import base64
import json
import logging
from dotenv import load_dotenv

from google import genai
from google.oauth2 import service_account
from google.cloud import texttospeech
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── Clients (lazy-init singletons) ───────────────────────────────────────────

_gemini_client = None
_tts_client = None
_vertexai_ready = False


def _get_gemini_client() -> genai.Client:
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        )
    return _gemini_client


def _get_tts_client() -> texttospeech.TextToSpeechClient:
    global _tts_client
    if _tts_client is None:
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if creds_path:
            credentials = service_account.Credentials.from_service_account_file(
                creds_path
            )
            _tts_client = texttospeech.TextToSpeechClient(credentials=credentials)
        else:
            # Falls back to ADC (Application Default Credentials) for Cloud Run
            _tts_client = texttospeech.TextToSpeechClient()
    return _tts_client


def _init_vertexai():
    global _vertexai_ready
    if not _vertexai_ready:
        vertexai.init(
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        )
        _vertexai_ready = True


# ─── SYSTEM PROMPT ─────────────────────────────────────────────────────────────

DIRECTOR_SYSTEM_PROMPT = """
You are the Interactive Mythos Director — a cinematic AI storyteller.

Your role: craft immersive, evolving story worlds in response to user prompts.
Maintain continuity with prior story events. Never contradict established lore.

For every turn, respond ONLY with a valid JSON object using this exact structure:
{
  "story": "A vivid 2-3 sentence narrative scene (100-150 words). Use present tense.",
  "image_prompt": "A precise, detailed visual description (lighting, mood, style, subject). Optimized for Imagen 3.",
  "voice_script": "1-2 clean sentences for cinematic narration. No special characters.",
  "choices": ["Choice A", "Choice B", "Choice C"]
}

Style rules:
- Tone: dark, cinematic, mythic
- Avoid clichés; use vivid, specific imagery
- choices must meaningfully branch the story
- voice_script must be suitable for text-to-speech (no em-dashes, no markdown)
"""


# ─── 1. GEMINI — Story Generation ─────────────────────────────────────────────

def generate_story(prompt: str, history: list[dict] | None = None) -> dict:
    """
    Call Gemini to produce a structured story scene.

    Args:
        prompt:  The current user input / choice.
        history: List of prior turns [{"role": "user"|"model", "parts": [{"text": "..."}]}]

    Returns:
        Parsed dict with keys: story, image_prompt, voice_script, choices
    """
    client = _get_gemini_client()
    history = history or []

    # Build the conversation contents list
    contents = [
        # Inject system persona as first user message (Vertex GenAI SDK style)
        {"role": "user", "parts": [{"text": DIRECTOR_SYSTEM_PROMPT}]},
        {"role": "model", "parts": [{"text": "Understood. I am the Interactive Mythos Director. Send your first prompt."}]},
        *history,
        {"role": "user", "parts": [{"text": prompt}]},
    ]

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=contents,
        config={"temperature": 0.9, "max_output_tokens": 1024},
    )

    raw = response.text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1] if len(parts) >= 2 else raw
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        result = json.loads(raw.strip())
    except json.JSONDecodeError as e:
        logger.error("Gemini returned non-JSON: %s", raw)
        raise ValueError(f"Gemini response could not be parsed as JSON: {e}") from e

    # Validate required keys
    required = {"story", "image_prompt", "voice_script", "choices"}
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Gemini response missing keys: {missing}")

    return result


# ─── 2. IMAGEN — Image Generation ─────────────────────────────────────────────

def generate_image(image_prompt: str) -> str:
    """
    Generate a scene illustration using Imagen 3 via Vertex AI.

    Args:
        image_prompt: Detailed visual description from Gemini.

    Returns:
        Base64-encoded PNG/JPEG string.
    """
    _init_vertexai()

    model_name = os.getenv("IMAGEN_MODEL", "imagen-3.0-generate-001")
    imagen = ImageGenerationModel.from_pretrained(model_name)

    # Enrich the prompt with cinematic style guidance
    styled_prompt = (
        f"{image_prompt}. "
        "Cinematic lighting, highly detailed digital painting, "
        "dark fantasy aesthetic, 16:9 widescreen composition, "
        "photorealistic textures, dramatic atmosphere."
    )

    try:
        images = imagen.generate_images(
            prompt=styled_prompt,
            number_of_images=1,
            aspect_ratio="16:9",
            safety_filter_level="block_some",
            person_generation="allow_adult",
        )
        image_bytes = images[0]._image_bytes
    except Exception as e:
        logger.error("Imagen generation failed: %s", e)
        raise RuntimeError(f"Image generation failed: {e}") from e

    return base64.b64encode(image_bytes).decode("utf-8")


# ─── 3. TTS — Cinematic Voice Narration ───────────────────────────────────────

# Available cinematic voices (swap via env var NARRATOR_VOICE)
NARRATOR_VOICES = {
    "journey-d":  ("en-US", "en-US-Journey-D",  texttospeech.SsmlVoiceGender.MALE),
    "journey-f":  ("en-US", "en-US-Journey-F",  texttospeech.SsmlVoiceGender.FEMALE),
    "neural2-j":  ("en-US", "en-US-Neural2-J",  texttospeech.SsmlVoiceGender.MALE),
    "studio-q":   ("en-US", "en-US-Studio-Q",   texttospeech.SsmlVoiceGender.MALE),
}


def _build_ssml(text: str) -> str:
    """Wrap narration text in SSML for a slower, dramatic delivery."""
    # Escape XML special characters
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        '<speak>'
        '  <prosody rate="slow" pitch="-2st">'
        f'    <break time="400ms"/>{safe}<break time="600ms"/>'
        '  </prosody>'
        '</speak>'
    )


def generate_audio(voice_script: str) -> str:
    """
    Convert narration text to cinematic MP3 audio using Google Cloud TTS.

    Args:
        voice_script: Clean narration text from Gemini.

    Returns:
        Base64-encoded MP3 string.
    """
    client = _get_tts_client()

    voice_key = os.getenv("NARRATOR_VOICE", "journey-d")
    lang_code, voice_name, ssml_gender = NARRATOR_VOICES.get(
        voice_key, NARRATOR_VOICES["journey-d"]
    )

    ssml_text = _build_ssml(voice_script)

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice_params = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        name=voice_name,
        ssml_gender=ssml_gender,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.90,   # slightly slower for drama
        pitch=-1.5,           # deeper tone
        effects_profile_id=["large-home-entertainment-class-device"],
    )

    try:
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config,
        )
    except Exception as e:
        logger.error("TTS synthesis failed: %s", e)
        raise RuntimeError(f"Audio generation failed: {e}") from e

    return base64.b64encode(response.audio_content).decode("utf-8")


# ─── 4. FULL PIPELINE ─────────────────────────────────────────────────────────

def generate_scene_package(prompt: str, history: list[dict] | None = None) -> dict:
    """
    Orchestrate the full Gemini → Imagen → TTS pipeline for one story turn.

    Args:
        prompt:  User input or chosen story branch.
        history: Prior conversation turns for continuity.

    Returns:
        dict with keys: story, image_prompt, voice_script, choices,
                        image_base64, audio_base64
    """
    logger.info("▶ Generating story scene…")
    scene = generate_story(prompt, history)

    logger.info("▶ Generating scene illustration…")
    try:
        scene["image_base64"] = generate_image(scene["image_prompt"])
    except Exception as e:
        logger.warning("Image generation skipped: %s", e)
        scene["image_base64"] = None

    logger.info("▶ Generating voice narration…")
    try:
        scene["audio_base64"] = generate_audio(scene["voice_script"])
    except Exception as e:
        logger.warning("Audio generation skipped: %s", e)
        scene["audio_base64"] = None

    logger.info("✅ Scene package ready.")
    return scene
