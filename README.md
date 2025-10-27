# Gemini + LangGraph (single-node) + FastAPI + Streamlit

A minimal end-to-end chatbot using:
- **LangGraph** with a single node
- **Gemini** as the LLM
- **FastAPI** exposing one `/chat` endpoint
- **Streamlit** UI that talks to the API

## Features
- Send full message history, get back the **last AI message** + full updated history.
- Easy to swap Gemini model via env var.

---

## Prereqs
- Python 3.10+ recommended
- A Gemini API key from Google AI Studio

---

## Setup: virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
````

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configure environment

Copy `.env.example` → `.env` and set:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-1.5-pro
```

---

## Run the API (FastAPI)

```bash
uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000
```

Test with curl:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
        "messages":[
          {"role":"system","content":"You are helpful."},
          {"role":"user","content":"Hello! Who are you?"}
        ]
      }'
```

You should get JSON with `ai_message` and the updated `messages` array.

---

## Run the UI (Streamlit)

In a second terminal:

```bash
streamlit run app/ui/streamlit_app.py
```

By default, it calls `http://127.0.0.1:8000`.
If your API runs elsewhere, create `.streamlit/secrets.toml`:

```toml
BACKEND_URL = "http://localhost:8000"
```

Then refresh the Streamlit page.

---

## Project layout

```
app/
  api/
    main.py        # FastAPI app with /chat
    graph.py       # LangGraph single-node graph
    schemas.py     # Pydantic models
    llm_providers/
      gemini.py    # Gemini wrapper
  core/
    config.py      # Loads GEMINI_API_KEY / model name
  ui/
    streamlit_app.py
```

---

## Notes

* This demo DOES NOT stream tokens; it does a simple request/response. You can add streaming later.
* The single LangGraph node (`llm_node`) just calls Gemini with the full history and appends the AI reply.
* Roles: `"user"`, `"assistant"`, and optional `"system"` (inlined as an instruction in the first call).

## Troubleshooting

* If you see `GEMINI_API_KEY is not set`, make sure `.env` is in the project root and you ran the app from that directory.
* If requests hang, check that the API is running on the expected host:port and that Streamlit’s `BACKEND_URL` matches.

Happy hacking! 🎉

