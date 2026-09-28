"""
Memory Card Component

Member 4 ownership.

Renders memory browser with clickable cards.
"""

import streamlit as st
from typing import List, Callable, Optional
from datetime import datetime


# Memory type icons
MEMORY_TYPE_ICONS = {
    "preference": "📧",
    "requirement": "📋",
    "objection": "⚠️",
    "competitor": "🏢",
    "stakeholder": "👤",
    "pricing": "💰",
    "compliance": "🔒",
    "technical": "⚙️",
    "decision": "✅",
    "pattern": "🔄",
}


def render_memory_browser(
    memories: List,
    on_select: Callable = None,
    search_query: str = "",
):
    """Render memory browser sidebar with search and cards."""
    st.subheader("🧠 Memory Browser")
    
    # Search
    search = st.text_input("🔍 Search memories...", value=search_query, key="memory_search")
    
    # Filter memories
    filtered = memories
    if search:
        filtered = [m for m in memories if search.lower() in m.text.lower()]
    
    # Sort options
    sort_by = st.selectbox(
        "Sort by",
        ["Relevance", "Recency", "Frequency", "Confidence"],
        key="memory_sort"
    )
    
    # Apply sorting
    if sort_by == "Recency":
        filtered.sort(key=lambda m: m.metadata.get("last_seen", ""), reverse=True)
    elif sort_by == "Frequency":
        filtered.sort(key=lambda m: m.metadata.get("frequency", 0), reverse=True)
    elif sort_by == "Confidence":
        filtered.sort(key=lambda m: m.metadata.get("confidence", 0), reverse=True)
    
    # Render cards
    if not filtered:
        st.info("No memories yet. Start a conversation!")
    else:
        for memory in filtered:
            render_memory_card(memory, on_select)


def render_memory_card(memory, on_select: Callable = None):
    """Render a single memory card."""
    icon = MEMORY_TYPE_ICONS.get(memory.metadata.get("memory_type", ""), "📝")
    scope = memory.metadata.get("scope", "unknown")
    scope_color = "🔵" if scope == "project" else "🟢"
    frequency = memory.metadata.get("frequency", 1)
    confidence = memory.metadata.get("confidence", 0)
    
    freq_dots = "●" * min(frequency, 5) + "○" * max(0, 5 - frequency)
    
    # Card container
    with st.container():
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Main text
            st.markdown(f"**{icon} {memory.text}**")
            
            # Metadata badges
            badge_col1, badge_col2, badge_col3 = st.columns(3)
            badge_col1.caption(f"{scope_color} {scope.upper()}")
            badge_col2.caption(f"{freq_dots} {frequency}")
            badge_col3.caption(f"{confidence:.0%} conf")
            
            # Source quote preview
            quote = memory.metadata.get("source_quote", "")
            if quote:
                preview = quote[:80] + "..." if len(quote) > 80 else quote
                st.caption(f'"{preview}"')
            
            # Date range
            first = memory.metadata.get("first_seen", "")
            last = memory.metadata.get("last_seen", "")
            if first and last:
                try:
                    first_dt = datetime.fromisoformat(first.replace("Z", "+00:00"))
                    last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
                    if first_dt != last_dt:
                        st.caption(f"📅 {first_dt.strftime('%b %d')} – {last_dt.strftime('%b %d')}")
                except:
                    pass
        
        with col2:
            if st.button("🔍", key=f"view_{memory.id}", help="View details"):
                if on_select:
                    on_select(memory)


__all__ = [
    "render_memory_browser",
    "render_memory_card",
]