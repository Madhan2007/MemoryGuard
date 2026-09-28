"""
Chat Component

Member 4 ownership.

Renders conversation history and input.
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional


def render_chat(history: List[Dict[str, Any]]):
    """Render conversation history."""
    if not history:
        st.info("💬 Start a conversation to see memories in action")
        return
    
    for msg in history:
        role = msg.get("role", "assistant")
        content = msg.get("content", "")
        timestamp = msg.get("timestamp", datetime.now())
        metadata = msg.get("metadata", {})
        
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(content)
                st.caption(timestamp.strftime("%H:%M"))
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(content)
                if metadata:
                    with st.expander("🔧 Metadata"):
                        st.json(metadata)
                st.caption(timestamp.strftime("%H:%M"))


def render_input() -> Optional[str]:
    """Render chat input and return user input if submitted."""
    return st.chat_input("Type your message...", disabled=st.session_state.get("processing", False))


__all__ = [
    "render_chat",
    "render_input",
]