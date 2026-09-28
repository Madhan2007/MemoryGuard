"""
Comparison Component

Member 4 ownership.

Renders before/after comparison for demo.
"""

import streamlit as st


def render_comparison(before: str, after: str, context: str = ""):
    """Render before/after comparison for demo."""
    st.markdown("---")
    st.subheader("📊 Before / After Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Without Verified Memory**")
        st.info(before)
    with col2:
        st.markdown("**With Verified Memory**")
        st.success(after)
    
    if context:
        st.caption(f"Context: {context}")


__all__ = [
    "render_comparison",
]