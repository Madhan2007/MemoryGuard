"""
Status Component

Member 4 ownership.

Renders system status indicators.
"""

import streamlit as st


def render_status(hindsight_ok: bool, llm_ok: bool, memoryguard_ok: bool, processing: bool):
    """Render system status indicators."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if hindsight_ok:
            st.metric("Hindsight", "🟢 Connected")
        else:
            st.metric("Hindsight", "🔴 Disconnected")
    
    with col2:
        if llm_ok:
            st.metric("LLM", "🟢 Ready")
        else:
            st.metric("LLM", "🔴 Error")
    
    with col3:
        if memoryguard_ok:
            st.metric("MemoryGuard", "🟢 Active")
        else:
            st.metric("MemoryGuard", "🔴 Error")
    
    with col4:
        if processing:
            st.metric("Status", "🔄 Processing...")
        else:
            st.metric("Status", "⏸️ Idle")


__all__ = [
    "render_status",
]