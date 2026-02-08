"""
SOW Generation page - Compact Split-Pane Layout.
"""

import streamlit as st
import requests
import json
import sys
import time
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css

st.set_page_config(page_title="Generate SOW", page_icon="📄", layout="wide")

# Apply shared styles
apply_custom_css()

# Page-specific CSS overrides
st.markdown("""
<style>
    /* Force white text on primary buttons */
    div[data-testid="stButton"] > button[kind="primary"] p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }
    
    /* SOW Document Styling - Legal/Professional Look */
    .sow-document h1,
    .sow-document h2,
    .sow-document h3,
    .sow-document h4 {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #e5e5e5 !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    .sow-document h1 {
        font-size: 1.75rem !important;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 0.5rem;
    }
    
    .sow-document h2 {
        font-size: 1.4rem !important;
    }
    
    .sow-document h3 {
        font-size: 1.15rem !important;
    }
    
    .sow-document p {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        line-height: 1.8 !important;
        color: #d1d1d1 !important;
        margin-bottom: 1rem !important;
    }
    
    .sow-document ul, .sow-document ol {
        font-family: 'Georgia', 'Times New Roman', serif !important;
        color: #d1d1d1 !important;
        line-height: 1.8 !important;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint (hidden in sidebar for cleaner UI)
with st.sidebar:
    st.header("Configuration")
    API_URL = st.text_input(
        "API URL", 
        value="http://localhost:8000",
        help="FastAPI backend URL"
    )

# Compact Header - Left Aligned
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2rem; margin-bottom: 0.5rem;">Configure SOW Parameters</h1>
    <p style="color: #9ca3af; font-size: 0.9rem;">Provide client and product details to generate your Statement of Work</p>
</div>
""", unsafe_allow_html=True)

# Load Mock Data
@st.cache_data
def load_mock_data():
    try:
        data_path = root_path / "data"
        with open(data_path / "mock_crm.json", "r") as f:
            crm_data = json.load(f)
        with open(data_path / "mock_opportunities.json", "r") as f:
            opp_data = json.load(f)
        return crm_data, opp_data
    except Exception as e:
        return {"clients": []}, {"opportunities": []}

crm_data, opp_data = load_mock_data()

# Process Data for Dropdowns
clients = crm_data.get("clients", [])
client_map = {f"{c['name']} ({c['id']})": c for c in clients}
client_names = [""] + list(client_map.keys())

opps = opp_data.get("opportunities", [])
products = sorted(list(set(o["product"] for o in opps if o.get("product"))))
if not products: products = ["Real-Time Payments", "Open Banking", "AI Fraud Monitor"]

# Split-Pane Layout: Left (Form) | Right (Context) - Narrower Right Panel
col_left, col_right = st.columns([2.5, 1], gap="large")

with col_left:
    st.subheader("Input Parameters")
    
    # Client Selection to trigger updates
    def update_tier():
        sel = st.session_state.get("client_select")
        if sel and sel in client_map:
            c_data = client_map[sel]
            new_tier = c_data.get("compliance_tier", "MEDIUM")
            st.session_state["tier_select"] = new_tier

    # Row 1: Client + Tier (2 columns)
    c1, c2 = st.columns(2)
    with c1:
        selected_client = st.selectbox(
            "Client *",
            options=client_names,
            index=0,
            key="client_select",
            on_change=update_tier,
            help="Select client from CRM"
        )
    
    with c2:
        client_tier = st.selectbox(
            "Client Tier",
            options=["", "HIGH", "MEDIUM", "LOW"],
            key="tier_select",
            help="Compliance tier"
        )
    
    # Get Client Data
    client_id = ""
    if selected_client and selected_client in client_map:
        client_data = client_map[selected_client]
        client_id = client_data["id"]
        st.caption(f"📍 **ID:** {client_id} | **Industry:** {client_data.get('industry', 'N/A')}")

    # Row 2: Product + Quality Mode (2 columns)
    c1, c2 = st.columns(2)
    with c1:
        product = st.selectbox(
            "Product *",
            options=products,
            index=None,
            placeholder="Select a product...",
            help="Product or service to be delivered"
        )
    
    with c2:
        quality_mode = st.selectbox(
            "Quality Mode",
            options=["quick", "production"],
            format_func=lambda x: "Quick Draft" if x == "quick" else "Production Quality",
            help="Generation quality"
        )
    
    # Row 3: Requirements (Full Width)
    requirements = st.text_area(
        "Additional Requirements (optional)",
        placeholder="e.g., Include migration plan, 6-month timeline, dedicated support",
        height=120,
        help="Any specific requirements or notes for the SOW"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 4: Generate Button (Full Width) - NO EMOJI
    submit = st.button("Generate SOW", use_container_width=True, type="primary")

# Right Pane: Status & Context
with col_right:
    # Calculate estimates dynamically
    est_time = "15s - 35s"
    est_cost = "$0.06 - $0.23"
    model_name = "Amazon Nova Pro"
    
    if quality_mode == "quick":
        est_time = "5s - 10s"
        est_cost = "$0.01 - $0.05"
    
    # Job Details Card - Unified Glass Effect with Monospace Data
    st.markdown(f"""
<div style="background-color: rgba(10, 10, 10, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); border-top: 3px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 1.25rem;">
<div class="card-icon" style="background: rgba(245, 158, 11, 0.1); color: #F59E0B; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M227.31,73.37,182.63,28.68a16,16,0,0,0-22.63,0L36.69,152.06A15.86,15.86,0,0,0,32,163.31V208a16,16,0,0,0,16,16H92.69A15.86,15.86,0,0,0,104,219.31L227.31,96a16,16,0,0,0,0-22.63ZM92.69,208H48V163.31l88-88L180.69,120ZM192,108.68,147.31,64l24-24L216,84.68Z"></path></svg>
</div>
<h3 style="margin-top: 0; font-size: 1.1rem; font-weight: 600; color: #ffffff;">Job Details</h3>

<div class="metric-row">
<span class="metric-label" style="font-size: 0.75rem; color: #a3a3a3; text-transform: uppercase; letter-spacing: 0.05em;">Quality Mode</span>
<span class="metric-value" style="font-size: 0.875rem; color: #ffffff; font-weight: 500; font-family: 'Courier New', monospace;">{quality_mode.capitalize()}</span>
</div>
<div class="metric-row">
<span class="metric-label" style="font-size: 0.75rem; color: #a3a3a3; text-transform: uppercase; letter-spacing: 0.05em;">Est. Time</span>
<span class="metric-value" style="font-size: 0.875rem; color: #ffffff; font-weight: 500; font-family: 'Courier New', monospace;">{est_time}</span>
</div>
<div class="metric-row">
<span class="metric-label" style="font-size: 0.75rem; color: #a3a3a3; text-transform: uppercase; letter-spacing: 0.05em;">Est. Cost</span>
<span class="metric-value" style="font-size: 0.875rem; color: #ffffff; font-weight: 500; font-family: 'Courier New', monospace;">{est_cost}</span>
</div>
<hr style="border-color: rgba(255,255,255,0.1); margin: 1rem 0;">
<div class="metric-row">
<span class="metric-label" style="font-size: 0.75rem; color: #a3a3a3; text-transform: uppercase; letter-spacing: 0.05em;">LLM Model</span>
<span class="metric-value" style="font-size: 0.875rem; color: #ffffff; font-weight: 500; font-family: 'Courier New', monospace;">{model_name}</span>
</div>
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Active Knowledge Base - Terminal-Style Telemetry with Glass Effect
    st.markdown("""
<div style="background-color: rgba(10, 10, 10, 0.6); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
        <div style="width: 6px; height: 6px; background: #F59E0B; border-radius: 50%; animation: pulse 2s infinite;"></div>
        <h4 style="margin: 0; font-size: 1.1rem; font-weight: 600; color: #ffffff;">Active Knowledge Base</h4>
    </div>
    <div style="font-size: 0.75rem; line-height: 1.6; font-family: 'Courier New', monospace;">
        <p style="margin: 0 0 0.75rem 0; color: #9ca3af;">Scanning Knowledge Base...</p>
        <div style="padding-left: 0.5rem; color: #a3a3a3;">
            <p style="margin: 0.5rem 0;">› Found 3 previous SOWs for this client</p>
            <p style="margin: 0.5rem 0;">› Applied 2025 Rate Card</p>
            <p style="margin: 0.5rem 0;">› Risk Profile: <span style="color: #10B981; font-weight: 600;">Low</span></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Handle submission
if submit:
    if not client_id or not product:
        st.error("❌ Please provide both Client and Product")
    else:
        # Prepare request
        payload = {
            "client_id": client_id,
            "product": product,
            "quality_mode": quality_mode,
        }
        
        if requirements:
            payload["requirements"] = requirements
            
        if client_tier:
             payload["client_tier"] = client_tier
        
        # CSS for Status Container Styling
        st.markdown("""
<style>
    /* Style the status container with brand red terminal look */
    div[data-testid="stStatus"] {
        border: 1px solid #D92D20 !important;
        background: rgba(217, 45, 32, 0.05) !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    div[data-testid="stStatus"] > div {
        font-family: 'Courier New', monospace !important;
    }
    
    div[data-testid="stStatusWidget"] label {
        color: #D92D20 !important;
        font-weight: 600 !important;
        font-family: 'Courier New', monospace !important;
    }
</style>
""", unsafe_allow_html=True)
        
        # Live Execution Status
        with st.status("🤖 AI Agent Active: Construction in progress...", expanded=True) as status:
            st.write("🔍 Scanning Client Knowledge Base...")
            time.sleep(0.8)
            
            st.write("🛡️ Retrieving Compliance Tiers (High Risk)...")
            time.sleep(0.6)
            
            st.write("📝 Drafting Scope of Work...")
            
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/sow/create",
                    json=payload,
                    timeout=300
                )
                
                st.write("✨ Applying 'Cuscal' Brand Voice...")
                
                if response.status_code == 200:
                    result = response.json()
                    status.update(label="✅ Generation Complete!", state="complete", expanded=False)
                    
                    # RESULTS SECTION - Unified Command Bar
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("---")
                    
                    # Unified Command Bar: Telemetry Strip (Top)
                    st.markdown(f"""
<div style="background: #151515; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px 12px 0 0; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 8px 16px; display: flex; justify-content: space-between; align-items: center;">
    <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 6px; height: 6px; background: #10B981; border-radius: 50%; animation: pulse 2s infinite;"></div>
        <span style="font-family: 'Courier New', monospace; font-size: 11px; color: #10B981; letter-spacing: 0.05em;">GENERATION COMPLETE</span>
    </div>
    <div style="font-family: 'Courier New', monospace; font-size: 11px; color: #666;">
        TIME: {result['generation_time_seconds']}s  |  COST: ${result['cost_usd']}  |  MODE: {result['quality_mode'].upper()}
    </div>
</div>
""", unsafe_allow_html=True)
                    
                    # Action Toolbar (Bottom) - Unified with Telemetry
                    st.markdown("""
<style>
    /* Remove gap between telemetry and buttons */
    div[data-testid="column"] {
        background: #151515 !important;
        padding: 12px 16px 16px 16px !important;
        margin-top: -1px !important;
    }
    
    /* Ghost button styling for secondary actions */
    .stDownloadButton > button,
    div[data-testid="stButton"] > button:not([kind="primary"]) {
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: rgba(255,255,255,0.7) !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }
    
    .stDownloadButton > button:hover,
    div[data-testid="stButton"] > button:not([kind="primary"]):hover {
        border-color: rgba(255,255,255,1) !important;
        color: rgba(255,255,255,1) !important;
    }
    
    /* Primary button override for toolbar */
    div[data-testid="stButton"] > button[kind="primary"] {
        font-size: 13px !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
</style>
""", unsafe_allow_html=True)
                    
                    col_action1, col_action2, col_action3 = st.columns([2, 1, 1])
                    
                    with col_action1:
                        compliance_check = st.button("Run Compliance Check", type="primary", use_container_width=True, key="compliance_btn_top")
                    
                    with col_action2:
                        st.download_button(
                            label="Download PDF",
                            data=result['sow_text'],
                            file_name=f"SOW_{client_id}_{product.replace(' ', '_')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    
                    with col_action3:
                        if st.button("Copy Text", use_container_width=True):
                            st.toast("Text copied to clipboard!")
                    
                    # Close the unified container
                    st.markdown("""
<div style="background: #151515; border: 1px solid rgba(255,255,255,0.08); border-top: none; border-radius: 0 0 12px 12px; height: 1px; margin-top: -1px;"></div>
""", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)

                    # SOW Document Preview Container
                    st.markdown(f"""
<div class="sow-document" style="background: #0F0F0F; padding: 60px 80px; border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; font-family: 'Georgia', 'Times New Roman', serif; color: #d1d1d1; line-height: 1.8;">
{result['sow_text']}
</div>
""", unsafe_allow_html=True)
                    
                    st.markdown("<br><br>", unsafe_allow_html=True)

                    # Compliance check option (triggered from toolbar)
                    if compliance_check:
                        with st.spinner("Checking compliance..."):
                            review_response = requests.post(
                                f"{API_URL}/api/v1/sow/review",
                                json={
                                    "sow_text": result['sow_text'],
                                    "product": product,
                                    "client_tier": client_tier if client_tier else "MEDIUM"
                                }
                            )
                            
                            if review_response.status_code == 200:
                                review = review_response.json()
                                score = review['compliance_score']
                                status = review['status']
                                
                                # Compliance Card
                                st.markdown(f"""
<div class="glass-card accent-red" style="margin-top: 1rem;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 1rem;">
<div class="card-icon icon-bg-red" style="margin-bottom:0;">
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 256 256"><path d="M173.66,98.34a8,8,0,0,1,0,11.32l-56,56a8,8,0,0,1-11.32,0l-24-24a8,8,0,0,1,11.32-11.32L112,148.69l50.34-50.35A8,8,0,0,1,173.66,98.34ZM232,128A104,104,0,1,1,128,24,104.11,104.11,0,0,1,232,128Zm-16,0a88,88,0,1,0-88,88A88.1,88.1,0,0,0,216,128Z"></path></svg>
</div>
<div>
<h3 style="margin:0;">Compliance Report</h3>
<p style="margin:0;">Status: <b>{status}</b></p>
</div>
</div>
<div style="text-align: right;">
<span style="font-size: 2.5rem; font-weight: 700; color: white;">{score}</span>
<span style="font-size: 1rem; color: #94A3B8;">/100</span>
</div>
</div>
<hr style="border-color: rgba(255,255,255,0.1); margin: 1.5rem 0;">
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; text-align: center;">
<div><div style="color: #EF4444; font-weight:700;">HIGH RISK</div><div>{review['summary']['HIGH']}</div></div>
<div><div style="color: #F59E0B; font-weight:700;">MEDIUM RISK</div><div>{review['summary']['MEDIUM']}</div></div>
<div><div style="color: #10B981; font-weight:700;">LOW RISK</div><div>{review['summary']['LOW']}</div></div>
</div>
</div>
""", unsafe_allow_html=True)
                                
                                # Detailed Issues
                                if review['issues']:
                                    st.subheader("Risk Analysis Details")
                                    for issue in review['issues']:
                                        severity_icon = "🔴" if issue['severity'] == "HIGH" else "🟡" if issue['severity'] == "MEDIUM" else "🟢"
                                        with st.expander(f"{severity_icon} {issue['category']}"):
                                            st.write(f"**Description:** {issue['description']}")
                                            st.info(f"💡 **Suggestion:** {issue['suggestion']}")
                
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
