"""
Decision Panel Component

Member 4 ownership.

Renders MemoryGuard decision details with reason and evidence.
"""

import streamlit as st
from typing import List, Optional


def render_decision_panel(decision, memory=None):
    """Render MemoryGuard decision panel."""
    if not decision:
        return
    
    st.markdown("---")
    st.subheader("🛡️ MemoryGuard Decision")
    
    # Decision badge
    decision_colors = {
        "retain": "🟢",
        "merge": "🔵",
        "update": "🟠",
        "reject": "🔴",
        "needs_review": "🟡",
    }
    badge = decision_colors.get(decision.decision.value, "⚪")
    
    st.markdown(f"### {badge} **{decision.decision.value.upper()}** — {decision.confidence:.0%} confidence")
    
    # Scope badge
    scope_badge = "🔵 PROJECT" if decision.scope.value == "project" else "🟢 COMMON"
    st.caption(f"Scope: {scope_badge}")
    
    # Reason
    st.markdown(f"**Reason:** {decision.reason}")
    
    # Source evidence
    if decision.source_evidence:
        with st.expander("📋 Source Evidence", expanded=True):
            for i, ev in enumerate(decision.source_evidence):
                st.markdown(f"{i+1}. > {ev.quote}")
                st.caption(f"Turn {ev.turn_id} • {ev.conversation_id[:8]}")
    
    # Merge details
    if decision.decision.value == "merge" and decision.merge_instruction:
        with st.expander("🔄 Merge Details"):
            st.markdown(f"**Target Memory:** {decision.merge_instruction.target_memory_id}")
            st.markdown(f"**New Frequency:** {decision.merge_instruction.new_frequency}")
            st.markdown(f"**New Evidence Count:** {decision.merge_instruction.new_evidence_count}")
            st.markdown(f"**Strategy:** {decision.merge_instruction.merge_strategy}")
    
    # Conflicts
    if decision.conflicts:
        with st.expander("⚠️ Conflicts Detected"):
            for c in decision.conflicts:
                st.warning(f"Conflicts with {c.conflicting_memory_id}: {c.conflict_type}")
                if c.resolution:
                    st.info(f"Resolution: {c.resolution}")
    
    # Similar memories
    if decision.similar_memories:
        with st.expander("🔗 Similar Memories"):
            for m in decision.similar_memories:
                st.markdown(f"- {m.memory_id} (similarity: {m.similarity_score:.2f}) - {m.reason}")
    
    # Audit info
    with st.expander("🔧 Technical Details"):
        st.json({
            "audit_id": decision.audit_id,
            "decision": decision.decision.value,
            "confidence": decision.confidence,
            "scope": decision.scope.value,
        })


__all__ = [
    "render_decision_panel",
]