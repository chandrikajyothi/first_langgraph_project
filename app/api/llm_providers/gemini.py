from typing import List, Dict
import google.generativeai as genai
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)
_model = genai.GenerativeModel(model_name=settings.gemini_model)

def _to_gemini_history(messages: List[Dict[str, str]]) -> List[Dict]:
    """
    Convert [{'role':'user'|'assistant'|'system','content':str}, ...]
    into Gemini 'contents' format. Gemini expects roles 'user' or 'model'.
    We'll inline any 'system' message as a first user instruction.
    """
    contents: List[Dict] = []
    for m in messages:
        role = m.get("role", "user")
        text = m.get("content", "")

        if role == "assistant":
            contents.append({"role": "model", "parts": [text]})
        elif role == "system":
            contents.append({"role": "user", "parts": [f"[System instruction]: {text}"]})
        else:  # "user" or anything else
            contents.append({"role": "user", "parts": [text]})

    return contents

def generate_chat_response(messages: List[Dict[str, str]]) -> str:
    """
    Calls Gemini with the full history and returns the assistant's reply text.
    """
    contents = _to_gemini_history(messages)
    resp = _model.generate_content(contents)
    return (resp.text or "").strip()
