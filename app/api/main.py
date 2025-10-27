from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.graph import build_graph
from app.api.schemas import ChatRequest, ChatResponse, Message

app = FastAPI(title="LangGraph + Gemini (1-node)")

# Open CORS for local dev / Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

graph = build_graph()

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    state = {"messages": [m.model_dump() for m in req.messages]}
    result = graph.invoke(state)  # runs the single LLM node
    ai_text = result["messages"][-1]["content"] if result["messages"] else ""

    return ChatResponse(
        ai_message=ai_text,
        messages=[Message(**m) for m in result["messages"]],
    )
