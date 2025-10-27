import streamlit as st
import httpx

st.set_page_config(page_title="Gemini + LangGraph Chat", page_icon="🤖")

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🤖 Gemini + LangGraph (1-node)")

if "messages" not in st.session_state:
    # Seed with a lightweight system instruction
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Render history (skip system in chat bubbles)
for m in st.session_state.messages:
    if m["role"] == "user":
        with st.chat_message("user"):
            st.markdown(m["content"])
    elif m["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(m["content"])

prompt = st.chat_input("Type your message…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking…"):
        try:
            payload = {"messages": st.session_state.messages}
            r = httpx.post(f"{BACKEND_URL}/chat", json=payload, timeout=90.0)
            r.raise_for_status()
            data = r.json()
            ai = data.get("ai_message", "")
        except Exception as e:
            ai = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": ai})
    with st.chat_message("assistant"):
        st.markdown(ai)
