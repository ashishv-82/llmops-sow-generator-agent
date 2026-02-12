"""
Streamlit main application for SOW Generator.
"""

import sys
from pathlib import Path

import streamlit as st

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.agent.config import config
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

# Get model name from config and format it
model_name = config.bedrock_model_id.upper().replace("APAC.AMAZON.", "").replace(":", " ")

# Status Footer in Sidebar
with st.sidebar:
    st.markdown(
        f"""<div class="sidebar-footer">
<!-- System Status -->
<div class="status-section">
<div class="status-row">
<span class="status-dot"></span>
<span class="status-text">All Systems Operational</span>
</div>
<div class="engine-info">Powered by {model_name}</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

# Run the app
pg.run()
