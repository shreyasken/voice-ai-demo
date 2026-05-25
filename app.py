from flask import Flask, request, jsonify, send_file
from io import BytesIO
import os
from dotenv import load_dotenv

from tts.elevenlabs_client import ElevenLabsClient
from tts.openai_client import OpenAITTSClient

load_dotenv()

app = Flask(__name__, static_folder="static", static_url_path="")

_elevenlabs = None
_openai_tts = None


def get_elevenlabs():
    global _elevenlabs
    if _elevenlabs is None:
        key = os.getenv("ELEVENLABS_API_KEY")
        if not key:
            raise ValueError("ELEVENLABS_API_KEY not set in environment")
        _elevenlabs = ElevenLabsClient(api_key=key)
    return _elevenlabs


def get_openai():
    global _openai_tts
    if _openai_tts is None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        _openai_tts = OpenAITTSClient(api_key=key)
    return _openai_tts


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/voices")
def voices():
    from tts.elevenlabs_client import VOICES as EL_VOICES
    from tts.openai_client import VOICES as OAI_VOICES
    return jsonify({"elevenlabs": EL_VOICES, "openai": OAI_VOICES})


@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    provider = data.get("provider", "openai")
    voice = data.get("voice", "")

    if not text:
        return jsonify({"error": "Text is required"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text exceeds 5000 character limit"}), 400
    if provider not in ("elevenlabs", "openai"):
        return jsonify({"error": "Invalid provider"}), 400

    try:
        if provider == "elevenlabs":
            audio_bytes = get_elevenlabs().synthesize(text, voice)
        else:
            audio_bytes = get_openai().synthesize(text, voice)

        return send_file(BytesIO(audio_bytes), mimetype="audio/mpeg", as_attachment=False)
    except ValueError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": f"Synthesis failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
