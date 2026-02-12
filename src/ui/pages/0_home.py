import sys
from pathlib import Path

import streamlit as st

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css

# Page Config
st.set_page_config(
    page_title="Cuscal | Select Agent",
    page_icon="🟥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply centralized styles
apply_custom_css()

# Custom Homepage Content
st.markdown(
    """
<div class="cuscal-header">
    <div class="logo-container">
        Cuscal <span class="logo-square"></span>
    </div>
    <a href="#" class="login-link">Log In</a>
</div>

<div class="hero-section">
    <div class="hero-title">Select an Agent</div>
    <div class="hero-subtitle">
        Enterprise-grade AI for secure workflows. Deploy specialized agents for SOW generation, auditing, and intelligence.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# 4-Column Grid
col1, col2, col3, col4 = st.columns(4)

# ICONS (Feather Icons mostly)
ICON_EDIT = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-edit-2"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>"""
ICON_SHIELD = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-shield"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>"""
ICON_BRAIN = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-cpu"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>"""
ICON_BOOK = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-book-open"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>"""
ARROW_RIGHT = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>"""

with col1:
    st.markdown(
        f"""
    <a href="generate_sow" class="agent-card">
        <div class="card-icon icon-sow">{ICON_EDIT}</div>
        <div class="card-title">Create SOW</div>
        <div class="card-description">
            Synthesis of requirements into legal frameworks. Auto-drafting enabled for rapid deployment.
        </div>
        <div class="card-action">
            Start Drafting
            <span class="card-arrow">→</span>
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
    <a href="review_sow" class="agent-card">
        <div class="card-icon icon-audit">{ICON_SHIELD}</div>
        <div class="card-title">Review SOW</div>
        <div class="card-description">
            Automated compliance scrutiny and risk audit. SLA protocol validation active.
        </div>
        <div class="card-action">
            Start Audit
            <span class="card-arrow">→</span>
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
    <a href="client_research" class="agent-card">
        <div class="card-icon icon-intel">{ICON_BRAIN}</div>
        <div class="card-title">Client Research</div>
        <div class="card-description">
            Deep memory retrieval. Analyze transaction history & entity compatibility effortlessly.
        </div>
        <div class="card-action">
            Explore Intel
            <span class="card-arrow">→</span>
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""
    <a href="product_research" class="agent-card">
        <div class="card-icon icon-kb">{ICON_BOOK}</div>
        <div class="card-title">Product Research</div>
        <div class="card-description">
            Comprehensive technical library. Search specs, APIs, and integration guides instantly.
        </div>
        <div class="card-action">
            Query Base
            <span class="card-arrow">→</span>
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )
