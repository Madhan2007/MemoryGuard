"""
Provenance Visualization Component

Member 4 ownership.

Renders full provenance chain from source to decision.
"""

import streamlit as st
from typing import List


def render_provenance(provenance):
    """Render full provenance chain."""
    if not provenance:
        return
    
    st.markdown("---")
    st.subheader("📜 Provenance Chain")
    
    # Source quotes
    st.markdown("**Source Quotes:**")
    for i, quote in enumerate(provenance.source_quotes):
        st.markdown(f"{i+1}. \"{quote}\"")
    
    # Decision chain
    st.markdown("**Decision Steps:**")
    for step in provenance.decision_chain:
        col1, col2, col3 = st.columns([2, 1, 3])
        status = "✅" if step.result == "PASS" else "❌"
        col1.markdown(f"**{step.step}**")
        col2.markdown(f"{status} {step.result}")
        col3.markdown(step.reason)
    
    # Metadata
    with st.expander("🔧 Technical Details"):
        st.json({
            "source_conversation_id": provenance.source_conversation_id,
            "source_turn_ids": provenance.source_turn_ids,
            "extraction_method": provenance.extraction_method,
            "verifier_model": provenance.verifier_model,
            "verification_timestamp": provenance.verification_timestamp.isoformat() if hasattr(provenance.verification_timestamp, 'isoformat') else str(provenance.verification_timestamp),
            "audit_id": provenance.audit_id,
        })


__all__ = [
    "render_provenance",
]