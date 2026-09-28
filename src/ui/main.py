"""
MemoryGuard Streamlit Application

Member 4 ownership.

Main entry point for the Streamlit demo application.
"""

import streamlit as st
import asyncio
from datetime import datetime

from ..harness.agent_harness import AgentLoop, AgentResponse
from ..integrations.hindsight_client import HindsightClient
from ..integrations.groq_client import GroqClient
from ..memory.memory_guard import MemoryGuard
from ..harness.session import InMemorySessionStore
from ..integrations.config import get_config, Config

from .components.chat import render_chat, render_input
from .components.memory_card import render_memory_browser
from .components.decision_panel import render_decision_panel
from .components.provenance import render_provenance
from .components.promotion import render_promotion
from .components.comparison import render_comparison
from .components.status import render_status


# Page config
st.set_page_config(
    page_title="MemoryGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Initialize session state
def init_session_state():
    """Initialize all session state variables."""
    if "agent_loop" not in st.session_state:
        config = get_config()
        hindsight = HindsightClient(config)
        groq = GroqClient(config)
        memoryguard = MemoryGuard()  # TODO: inject proper dependencies
        session_store = InMemorySessionStore()
        st.session_state.agent_loop = AgentLoop(hindsight, groq, memoryguard, session_store)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "current_memories" not in st.session_state:
        st.session_state.current_memories = []
    
    if "selected_memory" not in st.session_state:
        st.session_state.selected_memory = None
    
    if "last_response" not in st.session_state:
        st.session_state.last_response = None
    
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "deal_id" not in st.session_state:
        st.session_state.deal_id = "deal-acme-001"
    
    if "rep_id" not in st.session_state:
        st.session_state.rep_id = "rep-001"
    
    if "demo_mode" not in st.session_state:
        st.session_state.demo_mode = False


def render_header():
    """Render application header with controls."""
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.title("🛡️ MemoryGuard")
        st.caption("Verify what an AI agent should remember — before it remembers it.")
    
    with col2:
        deal_options = {
            "deal-acme-001": "Acme Corp",
            "deal-globex-001": "Globex Corp",
            "deal-northwind-001": "Northwind Traders",
            "deal-initech-001": "Initech",
            "deal-umbrella-001": "Umbrella Corp",
        }
        selected_deal = st.selectbox(
            "Deal",
            options=list(deal_options.keys()),
            format_func=lambda x: deal_options.get(x, x),
            index=list(deal_options.keys()).index(st.session_state.deal_id) if st.session_state.deal_id in deal_options else 0,
        )
        if selected_deal != st.session_state.deal_id:
            st.session_state.deal_id = selected_deal
            st.session_state.chat_history = []
            st.session_state.current_memories = []
            st.rerun()
    
    with col3:
        rep_options = {
            "rep-001": "Sarah Chen",
            "rep-002": "Marcus Johnson",
            "rep-003": "Priya Patel",
            "rep-004": "David Kim",
            "rep-005": "Lisa Wang",
        }
        selected_rep = st.selectbox(
            "Rep",
            options=list(rep_options.keys()),
            format_func=lambda x: rep_options.get(x, x),
            index=list(rep_options.keys()).index(st.session_state.rep_id) if st.session_state.rep_id in rep_options else 0,
        )
        if selected_rep != st.session_state.rep_id:
            st.session_state.rep_id = selected_rep
            st.session_state.chat_history = []
            st.session_state.current_memories = []
            st.rerun()
    
    with col4:
        st.button("🔄 Clear Chat", on_click=clear_chat)
        st.button("🎬 Demo Mode", on_click=toggle_demo)


def clear_chat():
    """Clear chat history and memories."""
    st.session_state.chat_history = []
    st.session_state.current_memories = []
    st.session_state.selected_memory = None
    st.session_state.last_response = None


def toggle_demo():
    """Toggle demo mode."""
    st.session_state.demo_mode = not st.session_state.demo_mode


async def process_user_message(user_input: str):
    """Process user message through agent loop."""
    st.session_state.processing = True
    
    try:
        response = await st.session_state.agent_loop.process_turn(
            user_input=user_input,
            deal_id=st.session_state.deal_id,
            rep_id=st.session_state.rep_id,
        )
        
        st.session_state.last_response = response
        st.session_state.current_memories = response.recalled_memories
        
        # Add to chat history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now(),
        })
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response.response_text,
            "timestamp": datetime.now(),
            "metadata": {
                "candidates": len(response.candidate_memories),
                "decisions": [d.decision.value for d in response.memory_decisions],
            }
        })
        
        # Auto-select first decision for demo
        if response.memory_decisions:
            st.session_state.selected_memory = response.memory_decisions[0]
        
    except Exception as e:
        st.error(f"Error processing message: {e}")
    finally:
        st.session_state.processing = False


def main():
    """Main Streamlit application."""
    init_session_state()
    render_header()
    
    # Main layout
    col_browser, col_chat = st.columns([1, 3], gap="large")
    
    with col_browser:
        render_memory_browser(st.session_state.current_memories, on_select=on_memory_select)
    
    with col_chat:
        render_chat(st.session_state.chat_history)
        user_input = render_input()
        
        if user_input and not st.session_state.processing:
            asyncio.run(process_user_message(user_input))
            st.rerun()
    
    # Decision panel (bottom, full width)
    if st.session_state.selected_memory:
        render_decision_panel(st.session_state.selected_memory)
        if st.session_state.last_response:
            # Find the decision for this memory
            for decision in st.session_state.last_response.memory_decisions:
                if decision.memory_text == st.session_state.selected_memory.text:
                    render_provenance(decision.provenance)
                    break
    
    # Status bar
    render_status(
        hindsight_ok=True,  # TODO: check actual status
        llm_ok=True,
        memoryguard_ok=True,
        processing=st.session_state.processing,
    )


def on_memory_select(memory):
    """Handle memory card selection."""
    st.session_state.selected_memory = memory


if __name__ == "__main__":
    main()