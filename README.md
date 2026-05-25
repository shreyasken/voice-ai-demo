# Voice AI Demo — ElevenLabs vs OpenAI TTS

A lightweight web app for comparing two leading text-to-speech APIs side-by-side. Enter any text, select a voice from each provider, generate audio, and hear the difference in real time.

Built to explore the product and technical tradeoffs between ElevenLabs and OpenAI TTS — two APIs I've evaluated in production contexts for voice-driven products.

---

## Demo

> **[Add a GIF or screenshot here once running]**
>
> Suggested: record a short Loom or screen capture showing the comparison flow and embed it here. That alone will double the time recruiters spend on this repo.

---

## Tech Stack

| Layer     | Choice          | Why                                                   |
|-----------|-----------------|-------------------------------------------------------|
| Backend   | Python / Flask  | Minimal overhead; easy to swap TTS providers as a module |
| Frontend  | Vanilla JS/CSS  | No build step — the API comparison is the demo, not the framework |
| TTS APIs  | ElevenLabs + OpenAI | Side-by-side comparison is the core product insight |
| Config    | python-dotenv   | Safe key management; no secrets in code              |

---

## Quickstart

### 1. Clone and set up

```bash
git clone https://github.com/shreyasken/voice-ai-demo.git
cd voice-ai-demo
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
cp .env.example .env
# Edit .env and add your keys:
#   ELEVENLABS_API_KEY=...
#   OPENAI_API_KEY=...
```

Get your keys:
- ElevenLabs: [elevenlabs.io](https://elevenlabs.io) — free tier includes ~10k characters/month
- OpenAI: [platform.openai.com](https://platform.openai.com) — TTS is billed per character (~$15/1M chars for `tts-1`)

### 3. Run

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

---

## Project Structure

```
voice-ai-demo/
├── app.py                  # Flask routes and provider wiring
├── tts/
│   ├── elevenlabs_client.py  # ElevenLabs synthesis module
│   └── openai_client.py      # OpenAI TTS synthesis module
├── static/
│   ├── index.html            # Single-page UI
│   ├── style.css             # Dark theme, responsive grid
│   └── script.js             # Fetch API, audio playback, latency timing
├── .env.example              # Key template (safe to commit)
├── requirements.txt
└── README.md
```

---

## Product Thinking

### Why I built this

I spent two years at Audible building and shipping an AI voice production platform — a product that let publishers and authors generate voice replicas and narrate content at scale without a recording studio. In that work, the most consequential early decision was **which TTS provider to build on**, and that decision wasn't just a technical benchmark. It involved evaluating latency, voice expressiveness, pricing curves, API reliability, and how each provider's roadmap would age alongside our own.

This demo is a working artifact of that reasoning process. Rather than reading API docs and forming opinions, I wanted something I could hand to a PM, an engineer, or a content creator and say: *here — listen to both, and tell me what you notice.*

### The problem this solves

Anyone evaluating TTS APIs for a product faces the same friction: the providers' demo pages are curated and don't reflect your actual content. You need to hear your specific text — a piece of narration, a support script, a product description — in both systems before you have a meaningful opinion. This app makes that a 30-second workflow instead of a half-day integration exercise.

### What I found (PM lens)

**ElevenLabs** excels at warmth and emotional range. For long-form narrative content (audiobooks, podcasts, documentary-style video), its prosody is noticeably more human. The tradeoff: higher latency (often 2–4x OpenAI on short strings) and a more complex pricing model once you scale.

**OpenAI TTS** is fast, consistent, and predictable. For product surfaces where voice is functional — voice assistants, interactive tutorials, dynamic notifications — the slight flatness in delivery is a non-issue, and the speed and pricing simplicity become meaningful advantages.

**The insight that matters for product decisions**: neither API is universally better. The right choice is downstream of your use case, your latency SLA, and your content type. A creator-facing publishing tool and a customer support bot should not use the same TTS provider.

### What I'd build next

If this were a product and not a demo, the next iteration would instrument every synthesis request with character count, latency, provider, and a user satisfaction signal (a simple thumbs-up/thumbs-down after playback). After 1,000 sessions, you'd have real data on which provider wins for which content type — and that's the dataset that turns an engineering evaluation into a product strategy.

### How this connects to my work

This prototype reflects the same thinking I applied at Audible when scoping ML infrastructure decisions: **don't let the fastest API win by default; let the use case define the constraints, then pick the provider that fits inside them.** The $4B GMV authentication system I led at scale required the same discipline — picking primitives based on failure modes and growth curves, not just what was easiest to integrate today.

---

## Extending this project

| Idea | What it would demonstrate |
|------|--------------------------|
| Add a voice cloning endpoint | ElevenLabs supports uploading a voice sample — surfaces real IP/trust tradeoffs |
| Stream audio instead of buffering | Reduces perceived latency; relevant for real-time use cases |
| Add a per-request cost tracker | Surfaces pricing model differences in a concrete way |
| Persist comparisons to a DB | Turns the demo into a lightweight evaluation harness |

---

## License

MIT
