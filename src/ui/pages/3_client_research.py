"""
Client Research page.
"""

import streamlit as st
import requests
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css, main_header

st.set_page_config(page_title="Client Research", page_icon="👥", layout="wide")

# Apply shared styles
apply_custom_css()

# Header
main_header(
    "Client Research",
    "Explore client information, compliance tiers, and historical data."
)

# API endpoint (hidden in sidebar)
with st.sidebar:
    st.header("Configuration")
    API_URL = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="FastAPI backend URL"
    )

st.markdown("---")

import json

# Load Mock Data
@st.cache_data
def load_crm_data():
    try:
        data_path = root_path / "data"
        with open(data_path / "mock_crm.json", "r") as f:
            crm_data = json.load(f)
        return crm_data
    except Exception as e:
        return {"clients": []}

crm_data = load_crm_data()
clients = crm_data.get("clients", [])
client_map = {f"{c['name']} ({c['id']})": c['id'] for c in clients}
client_names = [""] + list(client_map.keys())

st.subheader("Search Client Data")

with st.form("client_research_form"):
    selected_client = st.selectbox(
        "Select Client",
        options=client_names,
        placeholder="Choose a client from CRM...",
        help="Select a client to view their details"
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
                    f"{API_URL}/api/v1/research/client",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    client_data = result.get('client_data', {})
                    
                    if 'error' in client_data:
                        st.error(f"❌ {client_data['error']}")
                    else:
                        # Display in Card style
                        st.markdown("""
                        <div class="glass-card feature-card">
                            <h3>{}</h3>
                            <p>Checking compliance tier: <b>{}</b></p>
                        </div>
                        """.format(client_data.get('name', 'Unknown'), client_data.get('compliance_tier', 'N/A')), unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Industry", client_data.get('industry', 'N/A'))
                        col2.metric("Region", client_data.get('region', 'N/A'))
                        col3.metric("Revenue", f"${client_data.get('total_revenue', 0):,}")
                        
                        # Contacts
                        if 'contacts' in client_data:
                            st.markdown("### 👤 Contacts")
                            for contact in client_data['contacts']:
                                st.info(f"**{contact.get('name')}** ({contact.get('role')}) - {contact.get('email')}")

                        # Opportunities & SOWs
                        col_opp, col_sow = st.columns(2)
                        
                        with col_opp:
                            st.markdown("### 💼 Recent Opportunities")
                            opps = result.get('opportunities', [])
                            if opps:
                                for opp in opps:
                                    with st.expander(f"{opp.get('name')} (${opp.get('value', 0):,})"):
                                        st.write(f"Status: {opp.get('status')}")
                                        st.write(f"Close Date: {opp.get('close_date')}")
                            else:
                                st.write("No opportunities found.")

                        with col_sow:
                            st.markdown("### 📄 Historical SOWs")
                            sows = result.get('historical_sows', [])
                            if sows:
                                for sow in sows:
                                    st.markdown(f"- **{sow.get('title')}** ({sow.get('year')})")
                            else:
                                st.write("No historical SOWs found.")
                                
                elif response.status_code == 404:
                    st.warning(f"⚠️ Client not found")
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
