"""
Client Research page.
"""

import sys
from pathlib import Path

import requests
import streamlit as st

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css, main_header

st.set_page_config(page_title="Client Research", page_icon="👥", layout="wide")

# Apply shared styles
apply_custom_css()

# Header
main_header("Client Research", "Explore client information, compliance tiers, and historical data.")

# API Configuration
API_URL = "http://localhost:8000"

import json


# Load Mock Data
@st.cache_data
def load_crm_data():
    try:
        data_path = root_path / "data"
        with open(data_path / "mock_crm.json") as f:
            crm_data = json.load(f)
        return crm_data
    except Exception:
        return {"clients": []}


crm_data = load_crm_data()
clients = crm_data.get("clients", [])
client_map = {f"{c['name']} ({c['id']})": c["id"] for c in clients}
client_names = [""] + list(client_map.keys())

st.subheader("Search Client Data")

with st.form("client_research_form"):
    selected_client = st.selectbox(
        "Select Client",
        options=client_names,
        placeholder="Choose a client from CRM...",
        help="Select a client to view their details",
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submit_client = st.form_submit_button("🔍 Research Client", use_container_width=True)

if submit_client:
    if not selected_client:
        st.error("❌ Please select a client")
    else:
        client_id_val = client_map[selected_client]
        payload = {"client_id": client_id_val}

        with st.spinner("Researching client..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/research/client", json=payload, timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    client_data = result.get("client_data", {})

                    if "error" in client_data:
                        st.error(f"❌ {client_data['error']}")
                    else:
                        # --- HELPER LOGIC ---
                        def get_initials(name):
                            return "".join([n[0] for n in name.split()[:2]]).upper()

                        def get_status_pill(status):
                            status = status or "Unknown"
                            s_lower = status.lower()
                            if "won" in s_lower:
                                return "pill-green"
                            if "progress" in s_lower or "negotiation" in s_lower:
                                return "pill-amber"
                            return "pill-grey"

                        tier = client_data.get("compliance_tier", "N/A")
                        tier_class = "pill-red-outline" if tier == "HIGH" else "pill-grey"

                        # --- HERO SECTION ---
                        st.markdown(
                            f"""
                        <div style="margin-bottom: 2rem;">
                            <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; align-items: center; display: flex; gap: 1rem;">
                                {client_data.get('name', 'Unknown')}
                                <span class="status-pill {tier_class}">{tier}</span>
                            </h1>
                            <p style="color: #737373; font-size: 1.1rem;">{client_data.get('notes', '')}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        # --- METRICS CARD ---
                        st.markdown(
                            f"""
                        <div class="glass-metrics-card">
                            <div>
                                <span class="hero-metric-label">Industry</span>
                                <span class="hero-metric-value">{client_data.get('industry', 'N/A')}</span>
                            </div>
                            <div>
                                <span class="hero-metric-label">Region</span>
                                <span class="hero-metric-value">{client_data.get('region', 'N/A')}</span>
                            </div>
                            <div>
                                <span class="hero-metric-label">Revenue</span>
                                <span class="hero-metric-value">${client_data.get('total_revenue', 0):,}</span>
                            </div>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                        # --- MAIN CONTENT GRID ---
                        col_left, col_right = st.columns([1, 1.5], gap="large")

                        # --- CONTACTS (LEFT) ---
                        with col_left:
                            st.markdown("### Contacts")
                            if "contacts" in client_data:
                                for contact in client_data["contacts"]:
                                    c_name = contact.get("name", "Unknown")
                                    c_role = contact.get("role", "N/A")
                                    c_email = contact.get("email", "")
                                    initials = get_initials(c_name)

                                    st.markdown(
                                        f"""
                                    <div class="user-card">
                                        <div class="avatar-circle">{initials}</div>
                                        <div class="user-info">
                                            <span class="user-name">{c_name}</span>
                                            <span class="user-role">{c_role}</span>
                                            <span class="user-role" style="font-size: 0.75rem; color: #555;">{c_email}</span>
                                        </div>
                                    </div>
                                    """,
                                        unsafe_allow_html=True,
                                    )
                            else:
                                st.info("No contacts found.")

                        # --- OPPORTUNITIES (RIGHT) ---
                        with col_right:
                            st.markdown("### Recent Opportunities")
                            opps = result.get("opportunities", [])

                            if opps:
                                opp_html = '<div class="opp-list">'
                                for opp in opps:
                                    o_name = opp.get("name", "Unknown")
                                    o_val = opp.get("value", 0)
                                    o_status = opp.get("status", "Unknown")
                                    o_date = opp.get("close_date") or opp.get("end_date") or "N/A"

                                    pill_cls = get_status_pill(o_status)

                                    opp_html += f"""
<div class="opp-row">
    <div class="opp-main">
        <span class="opp-title">{o_name}</span>
        <div class="opp-meta">
            <span class="status-pill {pill_cls}">{o_status}</span>
            <span>• {o_date}</span>
        </div>
    </div>
    <span class="opp-value">${o_val:,}</span>
</div>
"""
                                opp_html += "</div>"
                                st.markdown(opp_html, unsafe_allow_html=True)
                            else:
                                st.info("No opportunities found.")

                            # Little spacer
                            st.markdown("<br><br>", unsafe_allow_html=True)

                            st.markdown("### Historical SOWs")
                            sows = result.get("historical_sows", [])
                            if sows:
                                for sow in sows:
                                    st.markdown(
                                        f"""
                                    <div style="padding: 0.75rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); color: #888; font-size: 0.9rem; display: flex; align-items: center; gap: 10px;">
                                        <div style="background: rgba(255,255,255,0.1); width: 24px; height: 24px; border-radius: 4px; display: flex; align-items: center; justify-content: center;">📄</div>
                                        <div>
                                            <strong>{sow.get('title')}</strong>
                                            <span style="color: #555; margin-left: 8px;">{sow.get('year')}</span>
                                        </div>
                                    </div>
                                    """,
                                        unsafe_allow_html=True,
                                    )
                            else:
                                st.write("No historical SOWs found.")

                elif response.status_code == 404:
                    st.warning("⚠️ Client not found")
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
