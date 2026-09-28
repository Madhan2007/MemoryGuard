"""
Promotion Visualization Component

Member 4 ownership.

Renders cross-scope promotion events.
"""

import streamlit as st


def render_promotion(promotion_event):
    """Render memory promotion event."""
    if not promotion_event:
        return
    
    st.markdown("---")
    st.subheader("📈 Memory Promotion")
    
    from_icon = "🟢" if promotion_event.from_scope == "common" else "🔵"
    to_icon = "🟢" if promotion_event.to_scope == "common" else "🔵"
    
    st.markdown(f"**From:** {from_icon} {promotion_event.from_scope.value.upper()}")
    st.markdown(f"**To:** {to_icon} {promotion_event.to_scope.value.upper()}")
    st.markdown(f"**Reason:** {promotion_event.reason}")
    st.markdown(f"**Trigger:** {promotion_event.trigger}")


__all__ = [
    "render_promotion",
]