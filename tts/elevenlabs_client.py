from elevenlabs import ElevenLabs

# voice_id → display label mapping for the UI
VOICES = {
    "21m00Tcm4TlvDq8ikWAM": "Rachel (warm, narrative)",
    "29vD33N1CtxCmqQRPOHJ": "Drew (confident, male)",
    "2EiwWnXFnvU5JabPnv8n": "Clyde (deep, grounded)",
    "AZnzlk1XvdvUeBnXmlld": "Domi (clear, energetic)",
    "EXAVITQu4vr4xnSDxMaL": "Bella (soft, conversational)",
    "pNInz6obpgDQGcFmaJgB": "Adam (neutral, authoritative)",
}

DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel


class ElevenLabsClient:
    def __init__(self, api_key: str):
        self._client = ElevenLabs(api_key=api_key)

    def synthesize(self, text: str, voice: str = DEFAULT_VOICE_ID) -> bytes:
        voice_id = voice if voice in VOICES else DEFAULT_VOICE_ID
        chunks = self._client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id="eleven_turbo_v2_5",
            output_format="mp3_44100_128",
        )
        return b"".join(chunks)
