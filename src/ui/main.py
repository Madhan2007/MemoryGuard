import streamlit as st
import asyncio
import json
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.harness.agent_harness import agent_loop
from src.memory.schema import DecisionType, MemoryDecision
from src.integrations.firebase_services import firebase_auth_service, firestore_service

st.set_page_config(
    page_title="MemoryGuard - Deal Intelligence Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

SCENARIOS = {
    "acme": "Acme Corp (Consolidation)",
    "northwind": "Northwind Health (Contamination)",
    "globex": "Globex Inc (Scope Isolation)",
    "initech": "Initech (Conflict Resolution)",
    "umbrella": "Umbrella Co (Lifecycle/Staleness)",
}

DECISION_COLORS = {
    "retain": "🟢",
    "merge": "🔵",
    "update": "🟡",
    "reject": "🔴",
    "needs_review": "🟠",
}

DECISION_LABELS = {
    "retain": "NEW",
    "merge": "MERGED",
    "update": "UPDATED",
    "reject": "REJECTED",
    "needs_review": "REVIEW",
}


def init_session_state():
    defaults = {
        "messages": [],
        "turn_id": 1,
        "current_deal": "acme",
        "current_rep": "rep-001",
        "conversation_id": None,
        "show_without_memory": False,
        "all_memories": [],
        "user": None,  # Authenticated user
        "auth_mode": "login",  # login, signup
        "custom_token": None,  # Firebase custom token for client SDK
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_conversation():
    st.session_state.messages = []
    st.session_state.turn_id = 1
    st.session_state.conversation_id = f"conv-{st.session_state.current_deal}"
    st.session_state.all_memories = []


def logout():
    """Clear user session and reset to login."""
    for key in ["user", "custom_token", "messages", "turn_id", "conversation_id", "all_memories"]:
        if key in st.session_state:
            del st.session_state[key]
    init_session_state()


async def process_turn(user_input: str):
    deal_id = st.session_state.current_deal
    rep_id = st.session_state.user.get("uid", "rep-001") if st.session_state.user else "rep-001"
    conv_id = st.session_state.conversation_id
    turn_id = st.session_state.turn_id

    result = await agent_loop.process_turn(
        user_input=user_input,
        deal_id=deal_id,
        rep_id=rep_id,
        conversation_id=conv_id,
        turn_id=turn_id,
        customer_name=deal_id,
    )

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "turn_id": turn_id,
    })
    st.session_state.messages.append({
        "role": "assistant",
        "content": result.answer,
        "turn_id": turn_id,
        "decisions": result.memory_decisions,
        "retrieved": result.retrieved_memories,
    })

    for dec in result.memory_decisions:
        if dec.decision in (DecisionType.RETAIN, DecisionType.MERGE, DecisionType.UPDATE):
            st.session_state.all_memories.append({
                "turn": turn_id,
                "decision": dec,
                "deal_id": deal_id,
            })

    st.session_state.turn_id += 1
    return result


def decision_badge(decision: MemoryDecision) -> str:
    color = DECISION_COLORS.get(decision.decision.value, "⚪")
    label = DECISION_LABELS.get(decision.decision.value, decision.decision.value.upper())
    scope_icon = "📁" if decision.scope.value == "project" else "👤"
    return f"{color} **{label}** {scope_icon} {decision.scope.value}"


def render_memory_card(decision: MemoryDecision, turn_num: int):
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(decision_badge(decision))
            st.markdown(f"*{decision.memory_text}*")
            st.caption(f"Turn {turn_num} • {decision.reason}")
            if decision.source_evidence:
                st.caption(f"💬 Source: \"{decision.source_evidence[0].quote[:120]}...\"")
        with col2:
            st.metric("Confidence", f"{decision.confidence:.0%}")
            if decision.merge_instruction:
                st.caption(f"🔗 Merged into: {decision.merge_instruction.target_memory_id[:8]}...")
            if decision.verification_status:
                status = decision.verification_status.value
                if status == "supported":
                    st.caption("✅ Supported")
                elif status == "unsupported":
                    st.caption("❌ Unsupported")
        st.divider()


def render_visual_flow():
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <span style="font-size: 1.5rem;">💬</span>
        <span style="font-size: 1.2rem; margin: 0 0.5rem;">→</span>
        <span style="font-size: 1.5rem;">✅</span>
        <span style="font-size: 1.2rem; margin: 0 0.5rem;">→</span>
        <span style="font-size: 1.5rem;">🗄️</span>
        <span style="font-size: 1.2rem; margin: 0 0.5rem;">→</span>
        <span style="font-size: 1.5rem;">🔍</span>
        <span style="font-size: 1.2rem; margin: 0 0.5rem;">→</span>
        <span style="font-size: 1.5rem;">💡</span>
        <span style="font-size: 1.2rem; margin: 0 0.5rem;">→</span>
        <span style="font-size: 1.5rem;">📈</span>
        <span style="font-size: 1.2rem; margin: 0 0.5rem;">→</span>
        <span style="font-size: 1.5rem;">🧠</span>
    </div>
    <div style="text-align: center; font-size: 0.8rem; color: #666; margin-top: -0.5rem;">
        Interaction → Verified Memory → Hindsight → Recall → Personalized Rec → Outcome → Verified Outcome → Future Learning
    </div>
    """, unsafe_allow_html=True)


def render_retrieved_memories(memories):
    if not memories:
        st.info("No prior memories recalled")
        return
    st.markdown("### 📚 Recalled Context")
    for m in memories:
        scope = m.get("metadata", {}).get("scope", "unknown")
        freq = m.get("metadata", {}).get("frequency", 1)
        score = m.get("score", 0)
        scope_icon = "📁" if scope == "project" else "👤"
        with st.expander(f"{scope_icon} {m['text'][:80]}... (freq={freq}, score={score:.2f})"):
            st.json(m.get("metadata", {}))


def render_login_page():
    """Render login/signup page."""
    st.title("🧠 MemoryGuard - Deal Intelligence Agent")
    st.caption("Verify what an AI agent should remember — before it learns from it.")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab_login:
            st.markdown("### Welcome Back")
            email = st.text_input("Email", placeholder="you@company.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            
            if st.button("Sign In", type="primary", use_container_width=True, key="btn_login"):
                if not email or not password:
                    st.error("Please enter email and password")
                else:
                    with st.spinner("Signing in..."):
                        result = asyncio.run(firebase_auth_service.sign_in_user(email, password))
                    
                    if result.get("success"):
                        st.session_state.user = {
                            "uid": result["uid"],
                            "email": result["email"],
                            "display_name": result["display_name"],
                            "profile": result.get("profile", {}),
                        }
                        st.session_state.custom_token = result.get("custom_token")
                        st.success("Signed in successfully!")
                        st.rerun()
                    else:
                        st.error(result.get("error", "Sign in failed"))
            
            st.markdown("---")
            st.caption("Demo credentials: Use any email/password (Firebase custom token will be generated)")
        
        with tab_signup:
            st.markdown("### Create Account")
            signup_email = st.text_input("Email", placeholder="you@company.com", key="signup_email")
            signup_password = st.text_input("Password", type="password", placeholder="•••••••• (min 6 chars)", key="signup_password")
            signup_name = st.text_input("Display Name", placeholder="John Doe", key="signup_name")
            
            if st.button("Create Account", type="primary", use_container_width=True, key="btn_signup"):
                if not signup_email or not signup_password or not signup_name:
                    st.error("Please fill all fields")
                elif len(signup_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    with st.spinner("Creating account..."):
                        result = asyncio.run(firebase_auth_service.create_user(signup_email, signup_password, signup_name))
                    
                    if result.get("success"):
                        st.success("Account created! Please sign in.")
                    else:
                        st.error(result.get("error", "Signup failed"))


def render_main_app():
    """Render the main authenticated app."""
    user = st.session_state.user
    
    # Header with user info
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("🧠 MemoryGuard - Deal Intelligence Agent")
        st.caption("Verify what an AI agent should remember — before it learns from it.")
    with col2:
        st.markdown(f"👤 **{user.get('display_name', 'User')}**")
        st.caption(user.get('email', ''))
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    render_visual_flow()
    st.divider()

    with st.sidebar:
        st.header("Deal Settings")
        deal = st.selectbox(
            "Select Deal",
            options=list(SCENARIOS.keys()),
            format_func=lambda x: SCENARIOS[x],
            index=list(SCENARIOS.keys()).index(st.session_state.current_deal),
        )
        if deal != st.session_state.current_deal:
            st.session_state.current_deal = deal
            reset_conversation()
            st.rerun()

        rep_id_display = st.session_state.user.get("uid", "rep-001")
        st.text_input("Your Rep ID", value=rep_id_display, disabled=True)
        
        if st.button("🔄 Reset Conversation", type="secondary"):
            reset_conversation()
            st.rerun()

        st.divider()
        
        st.session_state.show_without_memory = st.checkbox(
            "🔄 Show WITHOUT Memory (Ablation)",
            value=st.session_state.show_without_memory,
            help="Compare agent response with vs without memory"
        )

        st.divider()
        st.markdown("### Hero Demos")
        st.markdown("""
        **ACME** - Consolidation
        - Repeat "prefer email" 3x
        - Watch MERGE with frequency=3
        
        **NORTHWIND** - Contamination
        - Say "evaluating SOC2"
        - Agent hallucinates "SOC2 mandatory"
        - Watch REJECT (UNSUPPORTED)
        
        **GLOBEX** - Scope Isolation
        - Competitors stay in project bank
        - Rep preference goes to common bank
        
        **INITECH** - Conflict
        - Salesforce → HubSpot change
        - Watch UPDATE with conflict link
        
        **UMBRELLA** - Lifecycle
        - CTO leaves, VP Engineering joins
        - SAML → OIDC explicit change
        """)

    # Main content area
    col_chat, col_memories = st.columns([2, 1])

    with col_chat:
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
                    if msg["role"] == "assistant":
                        decisions = msg.get("decisions", [])
                        if decisions:
                            with st.expander("🧠 Memory Decisions", expanded=True):
                                for d in decisions:
                                    render_memory_card(d, msg.get("turn_id", 0))
                        
                        retrieved = msg.get("retrieved", [])
                        if retrieved:
                            with st.expander("📚 Recalled Context"):
                                render_retrieved_memories(retrieved)

        user_input = st.chat_input("Type your message...")
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            with st.spinner("Processing..."):
                result = asyncio.run(process_turn(user_input))
            
            st.rerun()

    with col_memories:
        st.markdown("### 📋 Memory Panel")
        
        if st.session_state.all_memories:
            for mem in st.session_state.all_memories:
                render_memory_card(mem["decision"], mem["turn"])
        else:
            st.info("No memories stored yet. Start a conversation!")
        
        st.divider()
        
        st.markdown("### ⚡ Quick Demo Actions")
        demo_inputs = {
            "acme": [
                "I prefer email for all deal communication",
                "Also, I still prefer email for updates",
                "Email is my primary communication channel",
            ],
            "northwind": [
                "We are evaluating SOC2 compliance",
                "We're also looking at HIPAA requirements",
            ],
            "globex": [
                "We're evaluating Gong and Chorus",
                "Our budget is around $120K annually",
                "I prefer email for communication",
            ],
            "initech": [
                "We need CRM integration with Salesforce",
                "Actually, we're migrating to HubSpot",
                "Procurement requires three quotes",
            ],
            "umbrella": [
                "We need SSO with SAML 2.0",
                "Our CTO is the technical champion",
                "Our CTO left. New VP Engineering wants OIDC",
            ],
        }
        
        current_inputs = demo_inputs.get(st.session_state.current_deal, [])
        for i, demo_input in enumerate(current_inputs):
            if st.button(f"💬 {demo_input[:30]}...", key=f"demo_{i}", use_container_width=True):
                with st.chat_message("user"):
                    st.markdown(demo_input)
                with st.spinner("Processing..."):
                    result = asyncio.run(process_turn(demo_input))
                st.rerun()


def main():
    init_session_state()
    
    # Initialize Firebase
    if not firebase_auth_service.is_configured():
        st.error("⚠️ Firebase not configured. Please add Firebase credentials to `.env` file.")
        st.info("See `.env.example` for required Firebase configuration.")
        st.stop()
    
    # Check authentication
    if not st.session_state.user:
        render_login_page()
    else:
        render_main_app()


if __name__ == "__main__":
    main()