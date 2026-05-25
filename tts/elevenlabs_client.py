from elevenlabs.client import ElevenLabs

# id → display label mapping for the UI
VOICES = {
    "rachel":  "Rachel (warm, narrative)",
    "drew":    "Drew (confident, male)",
    "clyde":   "Clyde (deep, grounded)",
    "domi":    "Domi (clear, energetic)",
    "bella":   "Bella (soft, conversational)",
    "adam":    "Adam (neutral, authoritative)",
}


class ElevenLabsClient:
    def __init__(self, api_key: str):
        self._client = ElevenLabs(api_key=api_key)

    def synthesize(self, text: str, voice: str = "rachel") -> bytes:
        voice_name = voice.capitalize() if voice in VOICES else "Rachel"
        chunks = self._client.generate(
            text=text,
            voice=voice_name,
            model="eleven_monolingual_v1",
        )
        return b"".join(chunks)
