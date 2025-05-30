from typing import List, Optional

import google.generativeai as genai
from app.config import settings

# ╭──────────────────────── Configuration ────────────────────────╮
genai.configure(api_key=settings.GEMINI_API_KEY)

# Choose the model you prefer; both work the same way:
#   - "models/gemini-pro"            (standard, 32k context)
#   - "models/gemini-1.5-pro-latest" (128k context, May 2025 preview)
MODEL_NAME = "models/gemini-1.5-flash"

# models = genai.list_models()
# for model in models:
#     print(model.name, "-", model.supported_generation_methods)
# Temperature, top-p etc. can be tuned here
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 512,
}

# Optional: add or adjust safety settings
SAFETY_SETTINGS = {
    # Example: block nothing (0) → allow full book quotes; tighten as you wish
    # "HARASSMENT": "BLOCK_NONE",
    # "HATE_SPEECH": "BLOCK_NONE",
}

# ╰───────────────────────────────────────────────────────────────╯

def call_gemini_api(
    prompt: str,
    *,
    system_prompt: Optional[str] = None,
    history: Optional[List[dict]] = None,
) -> str:
    """
    Send `prompt` to Gemini and return the assistant’s reply as plain text.
    """
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config=GENERATION_CONFIG,
        safety_settings=SAFETY_SETTINGS or None,
    )

    chat = model.start_chat(
        history=history or []
    )

    # If system_prompt is provided, prepend it to prompt
    if system_prompt:
        prompt = f"{system_prompt.strip()}\n\n{prompt.strip()}"

    response = chat.send_message(
        [prompt],
        stream=False
    )

    return response.text.strip()
