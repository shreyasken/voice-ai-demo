document.addEventListener("DOMContentLoaded", async () => {
  const textInput = document.getElementById("text-input");
  const charCount = document.getElementById("char-count");
  const compareBtn = document.getElementById("compare-btn");

  // ── Populate voice dropdowns from /voices endpoint ──
  try {
    const res = await fetch("/voices");
    const data = await res.json();
    populateSelect("voice-elevenlabs", data.elevenlabs);
    populateSelect("voice-openai", data.openai);
  } catch {
    populateSelect("voice-elevenlabs", { rachel: "Rachel", drew: "Drew", clyde: "Clyde" });
    populateSelect("voice-openai", { alloy: "Alloy", echo: "Echo", nova: "Nova" });
  }

  // ── Character counter ──
  textInput.addEventListener("input", () => {
    charCount.textContent = textInput.value.length;
  });

  // ── Individual generate buttons ──
  document.querySelectorAll(".generate-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const provider = btn.dataset.provider;
      synthesize(provider);
    });
  });

  // ── Compare both ──
  compareBtn.addEventListener("click", async () => {
    setButtonLoading(compareBtn, true);
    await Promise.all([synthesize("elevenlabs"), synthesize("openai")]);
    setButtonLoading(compareBtn, false);
  });

  // ── Core synthesis function ──
  async function synthesize(provider) {
    const text = textInput.value.trim();
    if (!text) {
      showError(provider, "Please enter some text first.");
      return;
    }

    const voice = document.getElementById(`voice-${provider}`).value;
    const btn = document.querySelector(`#card-${provider} .generate-btn`);
    const audioContainer = document.getElementById(`audio-${provider}`);
    const audioEl = audioContainer.querySelector("audio");
    const latencyEl = audioContainer.querySelector(".latency-badge");

    hideError(provider);
    setButtonLoading(btn, true);

    const start = performance.now();

    try {
      const res = await fetch("/synthesize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, provider, voice }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ error: "Unknown error" }));
        throw new Error(err.error || `HTTP ${res.status}`);
      }

      const blob = await res.blob();
      const elapsed = ((performance.now() - start) / 1000).toFixed(2);

      const url = URL.createObjectURL(blob);
      if (audioEl.src) URL.revokeObjectURL(audioEl.src);
      audioEl.src = url;
      latencyEl.textContent = `Generated in ${elapsed}s`;

      audioContainer.hidden = false;
      audioEl.play();
    } catch (err) {
      showError(provider, err.message);
    } finally {
      setButtonLoading(btn, false);
    }
  }

  // ── Helpers ──
  function populateSelect(id, voices) {
    const sel = document.getElementById(id);
    sel.innerHTML = "";
    for (const [value, label] of Object.entries(voices)) {
      const opt = document.createElement("option");
      opt.value = value;
      opt.textContent = label;
      sel.appendChild(opt);
    }
  }

  function setButtonLoading(btn, loading) {
    btn.disabled = loading;
    btn.querySelector(".btn-text").hidden = loading;
    btn.querySelector(".btn-spinner").hidden = !loading;
  }

  function showError(provider, message) {
    const el = document.getElementById(`err-${provider}`);
    el.textContent = message;
    el.hidden = false;
  }

  function hideError(provider) {
    document.getElementById(`err-${provider}`).hidden = true;
  }
});
