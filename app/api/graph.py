from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph
from app.api.llm_providers.gemini import generate_chat_response

class ChatState(TypedDict):
    messages: List[Dict[str, str]]

def llm_node(state: ChatState) -> ChatState:
    ai_text = generate_chat_response(state["messages"])
    return {
        "messages": state["messages"] + [{"role": "assistant", "content": ai_text}]
    }

def build_graph():
    sg = StateGraph(ChatState)
    sg.add_node("llm", llm_node)
    sg.set_entry_point("llm")
    sg.set_finish_point("llm")
    return sg.compile()
