"""
Streamlit main application for SOW Generator.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css

# Page config
st.set_page_config(
    page_title="SOW Generator Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply shared styles
apply_custom_css()

# Define Pages with Material Icons (No Emojis!)
pages = [
    st.Page("pages/0_home.py", title="Dashboard", icon=":material/dashboard:", default=True),
    st.Page("pages/1_generate_sow.py", title="Generate SOW", icon=":material/note_add:"),
    st.Page("pages/2_review_sow.py", title="Review SOW", icon=":material/verified_user:"),
    st.Page("pages/3_client_research.py", title="Client Research", icon=":material/search:"),
    st.Page("pages/4_product_research.py", title="Product Research", icon=":material/inventory_2:"),
]

# Navigation
pg = st.navigation(pages)

# Status Footer in Sidebar
with st.sidebar:
    st.markdown("""
        <div class="status-footer">
            <div style="margin-bottom: 1.5rem;">
                <div class="status-text" style="font-size: 0.75rem;">SYSTEM STATUS</div>
                <div style="display: flex; align-items: center; margin-top: 0.5rem;">
                    <span class="status-dot"></span>
                    <span style="color: rgba(16, 185, 129, 0.9); font-size: 0.875rem; letter-spacing: 0.15em; font-weight: 600;">OPERATIONAL</span>
                </div>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <div class="status-text" style="font-size: 0.75rem;">AI MODEL</div>
                <div class="status-value" style="margin-top: 0.5rem; font-size: 1rem; font-weight: 700;">NOVA_PRO</div>
            </div>
            <div style="margin-bottom: 1.5rem;">
                <div class="status-text" style="font-size: 0.75rem;">RECENT ACTIVITY</div>
                <div class="status-value" style="margin-top: 0.5rem; font-size: 1rem; font-weight: 700;">3</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Run the app
pg.run()
