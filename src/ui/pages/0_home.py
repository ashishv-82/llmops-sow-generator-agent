import streamlit as st
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css, main_header

# Warm Dark Mode Design System - Homepage
st.set_page_config(page_title="SOW Generator", page_icon="📄", layout="wide")

# Apply centralized styles
apply_custom_css()

# Homepage-specific CSS (only cards and layout)
st.markdown("""
<style>
    /* The "Cockpit" Layout - No Scroll (Homepage specific) */
    [data-testid="stAppViewContainer"] {
        height: 100vh !important;
        overflow: hidden !important;
    }
    
    [data-testid="stMain"] {
        height: 100vh !important;
        overflow: hidden !important;
        display: flex;
        flex-direction: column;
    }
    
    .block-container {
        padding: 0 3rem !important;
        max-width: 100% !important;
        height: 100vh !important;
        display: flex;
        flex-direction: column;
    }
    
    /* Card Styles (Homepage specific) */
    .stealth-card {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        text-decoration: none !important;
        display: flex;
        flex-direction: column;
        position: relative;
        height: 100%;
    }
    
    .stealth-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 60px -10px rgba(0, 0, 0, 0.5), 
                    inset 0 0 20px rgba(255, 255, 255, 0.03);
        border-color: rgba(255, 255, 255, 0.08);
    }
    
    .stealth-card h3 {
        margin: 1rem 0 0.75rem 0;
        font-size: 1.875rem;
        font-weight: 700;
        letter-spacing: -0.025em;
    }
    
    .stealth-card p {
        margin: 0;
        color: #a3a3a3;
        line-height: 1.6;
        font-size: 0.9rem;
        min-height: 3rem;
        flex-grow: 1;
    }
    
    /* Icon Containers - Brand Red Accent */
    .card-icon-container {
        width: 44px;
        height: 44px;
        background: rgba(217, 45, 32, 0.1);
        border: 1px solid rgba(217, 45, 32, 0.2);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .stealth-card:hover .card-icon-container {
        background: rgba(217, 45, 32, 0.2);
        border-color: rgba(217, 45, 32, 0.4);
        box-shadow: 0 0 15px rgba(217, 45, 32, 0.4);
    }
    
    .card-icon-container svg {
        width: 22px;
        height: 22px;
        color: #D92D20;
    }
    
    /* Card Meta */
    .card-meta {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        font-size: 0.75rem;
        color: #737373;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Card Grid - 2 Columns */
    .card-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin: 1.5rem 0;
        flex-grow: 1;
        align-content: start;
    }
</style>
""", unsafe_allow_html=True)

# SVG Icons
ICON_EDIT = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M227.31,73.37,182.63,28.68a16,16,0,0,0-22.63,0L36.69,152.06A15.86,15.86,0,0,0,32,163.31V208a16,16,0,0,0,16,16H92.69A15.86,15.86,0,0,0,104,219.31L227.31,96a16,16,0,0,0,0-22.63ZM92.69,208H48V163.31l88-88L180.69,120ZM192,108.68,147.31,64l24-24L216,84.68Z"></path></svg>"""

ICON_CHECKLIST = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32ZM173.66,98.34l-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,137.37l50.34-50.35a8,8,0,0,1,11.32,11.32Z"></path></svg>"""

ICON_USERS = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M117.25,157.92a60,60,0,1,0-66.5,0A95.83,95.83,0,0,0,3.53,195.63a8,8,0,1,0,13.4,8.74,80,80,0,0,1,134.14,0,8,8,0,0,0,13.4-8.74A95.83,95.83,0,0,0,117.25,157.92ZM40,108a44,44,0,1,1,44,44A44.05,44.05,0,0,1,40,108Zm210.14,98.7a8,8,0,0,1-11.07-2.33A79.83,79.83,0,0,0,172,168a8,8,0,0,1,0-16,44,44,0,1,0-16.34-84.87,8,8,0,1,1-5.94-14.85,60,60,0,0,1,55.53,105.64,95.83,95.83,0,0,1,47.22,37.71A8,8,0,0,1,250.14,206.7Z"></path></svg>"""

ICON_PACKAGE = """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M223.68,66.15,135.68,18a15.88,15.88,0,0,0-15.36,0l-88,48.17a16,16,0,0,0-8.32,14v95.64a16,16,0,0,0,8.32,14l88,48.17a15.88,15.88,0,0,0,15.36,0l88-48.17a16,16,0,0,0,8.32-14V80.18A16,16,0,0,0,223.68,66.15ZM128,32l80.34,44L128,120,47.66,76ZM40,90l80,43.78v85.79L40,175.82Zm96,129.57V133.82L216,90v85.78Z"></path></svg>"""

# Header
main_header("SOW Generator Agent", "Enterprise AI Platform for Statement of Work Automation")

# Card Grid
col1, col2 = st.columns(2)

with col1:
    # Card 1: Create SOW
    st.markdown(f"""
    <a href="Generate_SOW" class="stealth-card">
        <div class="card-icon-container">
            {ICON_EDIT}
        </div>
        <h3>Create SOW</h3>
        <p>Generate a professional Statement of Work with AI-powered templates</p>
        <div class="card-meta">Fastest • Production Ready</div>
    </a>
    """, unsafe_allow_html=True)
    
    # Card 3: Client Research
    st.markdown(f"""
    <a href="Client_Research" class="stealth-card">
        <div class="card-icon-container">
            {ICON_USERS}
        </div>
        <h3>Client Research</h3>
        <p>Access client history, requirements, and compliance tiers from CRM</p>
        <div class="card-meta">CRM Integrated</div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    # Card 2: Review SOW
    st.markdown(f"""
    <a href="Review_SOW" class="stealth-card">
        <div class="card-icon-container">
            {ICON_CHECKLIST}
        </div>
        <h3>Review SOW</h3>
        <p>Run compliance checks and validate against legal requirements</p>
        <div class="card-meta">Compliance • Risk Analysis</div>
    </a>
    """, unsafe_allow_html=True)
    
    # Card 4: Product Research
    st.markdown(f"""
    <a href="Product_Research" class="stealth-card">
        <div class="card-icon-container">
            {ICON_PACKAGE}
        </div>
        <h3>Product Research</h3>
        <p>Explore product specifications and SLA requirements</p>
        <div class="card-meta">Knowledge Base</div>
    </a>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    © 2024 Enterprise AI Platform • v2.1.0 • Built with Streamlit
</div>
""", unsafe_allow_html=True)
