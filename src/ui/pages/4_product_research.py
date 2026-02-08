"""
Product Research page.
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

st.set_page_config(page_title="Product Research", page_icon="📦", layout="wide")

# Apply shared styles
apply_custom_css()

# Header
main_header(
    "Product Research",
    "Query the product knowledge base for features, pricing, and technical specs."
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
def load_opp_data():
    try:
        data_path = root_path / "data"
        with open(data_path / "mock_opportunities.json", "r") as f:
            opp_data = json.load(f)
        return opp_data
    except Exception as e:
        return {"opportunities": []}

opp_data = load_opp_data()
opps = opp_data.get("opportunities", [])
product_list = sorted(list(set(o["product"] for o in opps if o.get("product"))))
if not product_list: product_list = ["Real-Time Payments", "Open Banking", "AI Fraud Monitor"] # Fallback

st.subheader("Search Knowledge Base")

with st.form("product_research_form"):
    product_name = st.selectbox(
        "Product Name",
        options=product_list,
        placeholder="Select a product...",
        help="Product or service name"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    submit_product = st.form_submit_button("🔍 Research Product", use_container_width=True)

if submit_product:
    if not product_name:
        st.error("❌ Please select a product")
    else:
        with st.spinner("Researching product..."):
            try:
                response = requests.post(
                    f"{API_URL}/api/v1/research/product",
                    json={"product_name": product_name},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    p_info = result.get('product_info', {})
                    
                    st.markdown(f"## 📦 {p_info.get('name', 'Product')}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Category", p_info.get('category', 'N/A'))
                    col2.metric("Pricing", p_info.get('pricing_model', 'N/A'))
                    col3.metric("SLA Tier", "High Availability") # Mock data usually
                    
                    st.markdown("---")
                    
                    col_feat, col_req = st.columns(2)
                    
                    with col_feat:
                        st.markdown("### ✨ Features")
                        features = result.get('features', [])
                        if features:
                            for f in features:
                                st.markdown(f"- {f}")
                        else:
                            st.info("No features listed.")
                            
                    with col_req:
                        st.markdown("### ⚙️ Technical Requirements")
                        reqs = result.get('requirements', {})
                        if reqs:
                            for k, v in reqs.items():
                                st.markdown(f"**{k.replace('_', ' ').title()}**: {v}")
                        else:
                            st.info("No requirements listed.")
                            
                elif response.status_code == 404:
                    st.warning(f"⚠️ Product not found")
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
