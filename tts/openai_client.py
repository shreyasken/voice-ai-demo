from openai import OpenAI

VOICES = {
    "alloy":   "Alloy (neutral, versatile)",
    "echo":    "Echo (male, conversational)",
    "fable":   "Fable (expressive, British)",
    "onyx":    "Onyx (deep, authoritative)",
    "nova":    "Nova (female, warm)",
    "shimmer": "Shimmer (female, clear)",
}


class OpenAITTSClient:
    def __init__(self, api_key: str):
        self._client = OpenAI(api_key=api_key)

    def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        if voice not in VOICES:
            voice = "alloy"
        response = self._client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
        )
        return response.content
