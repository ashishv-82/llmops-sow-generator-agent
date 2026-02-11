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

# Initialize Session State for Persistence
if "sow_result" not in st.session_state:
    st.session_state.sow_result = None
if "compliance_report" not in st.session_state:
    st.session_state.compliance_report = None

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
        font-family: 'Inter', sans-serif !important;
        color: #FFFFFF !important;
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

# API Configuration
API_URL = "http://localhost:8000"

# Dashboard Header
st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem;">Create New SOW</h1>
        <p style="color: #666; font-size: 0.85rem;">Specify client and deal parameters to generate a production-ready Statement of Work.</p>
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
client_names = list(client_map.keys())

opps = opp_data.get("opportunities", [])
products = sorted(list(set(o["product"] for o in opps if o.get("product"))))
if not products: products = ["Real-Time Payments", "Open Banking", "AI Fraud Monitor"]

# Helper: Update client tier based on selection
def update_tier():
    sel = st.session_state.get("client_select")
    if sel and sel in client_map:
        c_data = client_map[sel]
        new_tier = c_data.get("compliance_tier", "MEDIUM")
        st.session_state["tier_select"] = new_tier

# Handle submission (Always runs if session state doesn't have a result yet)
if not st.session_state.sow_result:
    # Split-Pane Layout: Left (Form) | Right (Context)
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        # Simplified Section Title
        st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # Row 1: Client + Tier
        c1, c2 = st.columns(2)
        with c1:
            selected_client = st.selectbox(
                "Client *",
                options=client_names,
                index=None,
                placeholder="Select a client...",
                key="client_select",
                on_change=update_tier
            )
        
        with c2:
            client_tier = st.selectbox(
                "Client Tier",
                options=["HIGH", "MEDIUM", "LOW"],
                index=None,
                placeholder="Select a tier...",
                key="tier_select"
            )
        
        # Get Client Data
        client_id = ""
        if selected_client and selected_client in client_map:
            client_data = client_map[selected_client]
            client_id = client_data["id"]
            st.caption(f"📍 **ID:** {client_id} | **Industry:** {client_data.get('industry', 'N/A')}")

        # Row 2: Product + Quality Mode
        c1, c2 = st.columns(2)
        with c1:
            product = st.selectbox(
                "Product *",
                options=products,
                index=None,
                placeholder="Select a product...",
                key="product_select"
            )
        
        with c2:
            quality_mode = st.selectbox(
                "Quality Mode",
                options=["quick", "production"],
                format_func=lambda x: "Quick Draft" if x == "quick" else "Production Quality",
                key="quality_select"
            )
        
        # Row 3: Requirements
        requirements = st.text_area(
            "Additional Requirements (optional)",
            placeholder="e.g., Include migration plan, 6-month timeline, dedicated support",
            height=80
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 4: Generate Button
        submit = st.button("Generate SOW", use_container_width=True, type="primary")

    # Right Pane: Status & Context
    with col_right:
        # Calculate estimates dynamically
        est_time = "1m - 2m"
        est_cost = "$0.06 - $0.23"
        model_name = "Amazon Nova Pro"
        
        if quality_mode == "quick":
            est_time = "45s - 60s"
            est_cost = "$0.01 - $0.05"
        
        # Unified SaaS Card: Job Details + Pro Tips
        st.markdown(f"""
<div class="saas-card" style="padding: 1.25rem;">
<span class="section-tag" style="margin-bottom: 0.5rem;">Job Summary</span>
<div class="metric-group" style="gap: 8px; margin-bottom: 1.25rem;">
<div class="metric-row">
<span class="metric-label" style="font-size: 0.8rem;">Quality Mode</span>
<span class="metric-value" style="font-size: 0.8rem;">{quality_mode.capitalize() if quality_mode else 'N/A'}</span>
</div>
<div class="metric-row">
<span class="metric-label" style="font-size: 0.8rem;">Est. Time</span>
<span class="metric-value" style="font-size: 0.8rem;">{est_time}</span>
</div>
<div class="metric-row">
<span class="metric-label" style="font-size: 0.8rem;">Est. Cost</span>
<span class="metric-value" style="font-size: 0.8rem;">{est_cost}</span>
</div>
<div class="metric-row">
<span class="metric-label" style="font-size: 0.8rem;">LLM Model</span>
<span class="metric-value" style="font-size: 0.8rem;">{model_name}</span>
</div>
</div>

<div class="tip-group" style="padding-top: 1rem; gap: 10px;">
<span class="section-tag" style="margin-bottom: 0.5rem;">System Guidance</span>
<div class="tip-item" style="gap: 10px;">
<div class="tip-icon" style="color: #3B82F6;">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 16-4 4-4-4"/><path d="M17 20V4"/><path d="m3 8 4-4 4 4"/><path d="M7 4v16"/></svg>
</div>
<div class="tip-content" style="font-size: 0.8rem;">
<span class="tip-title" style="font-size: 0.8rem;">Specific Inputs</span>
<span class="tip-desc">Detailed requirements lead to more precise scope.</span>
</div>
</div>
<div class="tip-item" style="gap: 10px;">
<div class="tip-icon" style="color: #10B981;">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
</div>
<div class="tip-content" style="font-size: 0.8rem;">
<span class="tip-title" style="font-size: 0.8rem;">Compliance Tier</span>
<span class="tip-desc">High tier triggers enhanced regulatory audits.</span>
</div>
</div>
<div class="tip-item" style="gap: 10px;">
<div class="tip-icon" style="color: #F59E0B;">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
</div>
<div class="tip-content" style="font-size: 0.8rem;">
<span class="tip-title" style="font-size: 0.8rem;">Production Mode</span>
<span class="tip-desc">Enables multi-stage self-critique loops.</span>
</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Handle submission logic within the if block
    if submit:
        if not client_id or not product:
            st.error("❌ Please provide both Client and Product")
        else:
            # Clear previous state on new generation
            st.session_state.sow_result = None
            st.session_state.compliance_report = None
            
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
    div[data-testid="stStatus"] {
        border: 1px solid #D92D20 !important;
        background: rgba(217, 45, 32, 0.05) !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
    }
</style>
""", unsafe_allow_html=True)
            
            status_placeholder = st.empty()
            with status_placeholder.status("Processing Request...", expanded=True) as status:
                st.write("› Scanning Client Knowledge Base...")
                time.sleep(0.8)
                st.write("› Drafting Scope of Work...")
                
                try:
                    response = requests.post(f"{API_URL}/api/v1/sow/create", json=payload, timeout=300)
                    if response.status_code == 200:
                        status.update(label="Generation Complete", state="complete", expanded=False)
                        time.sleep(0.5)
                        status_placeholder.empty()
                        
                        st.session_state.sow_result = response.json()
                        st.rerun()
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {str(e)}")

else:
    # CONFIGURATION SUMMARY BAR (Result Mode)
    client_val = st.session_state.get('client_select', 'N/A')
    client_name_only = client_val.split(' (')[0] if '(' in client_val else client_val
    
    col_sum1, col_sum2 = st.columns([4, 1])
    with col_sum1:
        st.markdown(f"""
<div class="saas-card" style="padding: 10px 20px; margin-bottom: 0; background: rgba(255,255,255,0.02); border-color: rgba(255,255,255,0.1); display: flex; align-items: center; gap: 16px;">
    <div class="telemetry-tag" style="background: rgba(16, 185, 129, 0.1); color: #10B981; border-color: rgba(16, 185, 129, 0.2); margin-bottom:0;">Result Ready</div>
    <div style="font-size: 0.85rem; color: #fff; font-family: var(--font-family);">
        <span style="color: #666;">Client:</span> <b>{client_name_only}</b>
        <span style="color: #444; margin: 0 8px;">|</span>
        <span style="color: #666;">View Mode:</span> <b>Statement of Work Preview</b>
    </div>
</div>
""", unsafe_allow_html=True)
    
    with col_sum2:
        if st.button("Edit Config", use_container_width=True):
            st.session_state.sow_result = None
            st.session_state.compliance_report = None
            st.rerun()

# RESULTS SECTION (Rendered from st.session_state)
if st.session_state.sow_result:
    result = st.session_state.sow_result
    # Retrieve configuration from session state keys
    product_val = st.session_state.get('product_select', 'N/A')
    tier_val = st.session_state.get('tier_select', 'MEDIUM')
    client_val = st.session_state.get('client_select', 'N/A')
    c_id = client_map[client_val]['id'] if client_val in client_map else "N/A"
    
    # 1. Document Header (Integrated Toolbar)
    st.markdown(f"""
<div class="document-toolbar" style="margin-top: 1rem; border-bottom: none; border-radius: 12px 12px 0 0; background: #111;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div class="telemetry-tag" style="background: rgba(16, 185, 129, 0.1); color: #10B981; border-color: rgba(16, 185, 129, 0.2); margin-bottom:0;">Ready</div>
        <div style="font-size: 0.75rem; color: #666; font-family: var(--font-family);">
            Generated in <b>{result['generation_time_seconds']}s</b> &bull; Cost: <b>${result['cost_usd']}</b> &bull; Quality: <b>{result['quality_mode'].capitalize()}</b>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # 2. Action Toolbar (Buttons) - Integrated via negative margin
    st.markdown("""
<style>
    .integrated-toolbar {
        background: #111;
        border-right: 1px solid #222;
        border-left: 1px solid #222;
        padding: 0 1.5rem 0.75rem 1.5rem;
        margin-top: -1rem;
        display: flex;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)
    
    st.markdown('<div class="integrated-toolbar">', unsafe_allow_html=True)
    col_t1, col_t2, col_t3 = st.columns([2, 1, 1], gap="small")
    with col_t1:
        compliance_check = st.button("Run Compliance Check", type="primary", use_container_width=True, key="compliance_btn_top")
    with col_t2:
        st.download_button(
            label="Download PDF",
            data=result['sow_text'],
            file_name=f"SOW_{c_id}_{product_val.replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    with col_t3:
        if st.button("Copy Text", use_container_width=True):
            st.toast("Text copied!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Border-flush divider
    st.markdown("""
<div style="background: #111; border: 1px solid #222; border-top: none; border-radius: 0 0 12px 12px; height: 1px; margin-top: -1px; margin-bottom: 0;"></div>
""", unsafe_allow_html=True)

    # 3. Document Canvas (No gap between header and canvas)
    st.markdown(f"""
<div class="document-canvas" style="border-top: none; border-radius: 0 0 12px 12px; margin-top: -1px;">
{result['sow_text']}
</div>
""", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Compliance check logic (Stores to session state)
    if compliance_check:
        with st.spinner("Checking compliance..."):
            try:
                review_response = requests.post(
                    f"{API_URL}/api/v1/sow/review",
                    json={
                        "sow_text": result['sow_text'],
                        "product": product_val,
                        "client_tier": tier_val
                    }
                )
                
                if review_response.status_code == 200:
                    st.session_state.compliance_report = review_response.json()
                    st.rerun()
                else:
                    st.error(f"❌ Error: {review_response.status_code} - {review_response.text}")
                    
            except Exception as e:
                st.error(f"❌ Error during compliance check: {str(e)}")

    # Render Compliance Report if it exists in session state
    if st.session_state.compliance_report:
        review = st.session_state.compliance_report
        score = review['compliance_score']
        status = review['status']
        
        # Modern Compliance Report Card
        st.markdown(f"""
<div class="saas-card" style="border-left: 4px solid #D92D20; background: rgba(217, 45, 32, 0.03);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(217, 45, 32, 0.1); color: #D92D20; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <div>
                <span class="section-tag" style="margin:0;">Compliance Audit</span>
                <h3 style="margin:0; font-size: 1.1rem; color: #fff;">Audit Result: <span style="color: #D92D20;">{status}</span></h3>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 1.75rem; font-weight: 700; color: #fff; line-height: 1;">{score}</div>
            <div style="font-size: 0.7rem; color: #666; text-transform: uppercase; letter-spacing: 0.1em;">Compliance Score</div>
        </div>
    </div>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 24px;">
    <div style="background: rgba(5,5,5,0.4); padding: 12px; border-radius: 8px; border: 1px solid #222; text-align: center;">
        <div style="color: #EF4444; font-weight: 700; font-size: 0.7rem; margin-bottom: 4px;">HIGH RISK</div>
        <div style="color: #fff; font-size: 1.1rem; font-weight: 600;">{review['summary']['HIGH']}</div>
    </div>
    <div style="background: rgba(5,5,5,0.4); padding: 12px; border-radius: 8px; border: 1px solid #222; text-align: center;">
        <div style="color: #F59E0B; font-weight: 700; font-size: 0.7rem; margin-bottom: 4px;">MEDIUM RISK</div>
        <div style="color: #fff; font-size: 1.1rem; font-weight: 600;">{review['summary']['MEDIUM']}</div>
    </div>
    <div style="background: rgba(5,5,5,0.4); padding: 12px; border-radius: 8px; border: 1px solid #222; text-align: center;">
        <div style="color: #10B981; font-weight: 700; font-size: 0.7rem; margin-bottom: 4px;">LOW RISK</div>
        <div style="color: #fff; font-size: 1.1rem; font-weight: 600;">{review['summary']['LOW']}</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)
        
        # Detailed Issues
        if review['issues']:
            st.subheader("Risk Analysis Details")
            for issue in review['issues']:
                severity_icon = "🔴" if issue['severity'] == "HIGH" else "🟡" if issue['severity'] == "MEDIUM" else "🟢"
                
                # Create a more descriptive label
                label = f"{severity_icon} {issue['category']}"
                if "Prohibited Term" in issue['category']:
                    term = issue['description'].replace("Found prohibited term: ", "")
                    label += f": {term}"
                elif "Mandatory Clause" in issue['category']:
                    clause = issue['description'].replace("Missing required clause: ", "")
                    label += f": {clause}"
                
                with st.expander(label):
                    st.write(f"**Description:** {issue['description']}")
                    st.info(f"💡 **Suggestion:** {issue['suggestion']}")
