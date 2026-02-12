"""
Product Research page.
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

st.set_page_config(page_title="Product Research", page_icon="📦", layout="wide")

# Apply shared styles
apply_custom_css()

# Header
main_header(
    "Product Research",
    "Query the product knowledge base for features, pricing, and technical specs.",
)

# API Configuration
API_URL = "http://localhost:8000"

import json


# Load Mock Data
@st.cache_data
def load_opp_data():
    try:
        data_path = root_path / "data"
        with open(data_path / "mock_opportunities.json") as f:
            opp_data = json.load(f)
        return opp_data
    except Exception:
        return {"opportunities": []}


opp_data = load_opp_data()
opps = opp_data.get("opportunities", [])
product_list = sorted(list(set(o["product"] for o in opps if o.get("product"))))
if not product_list:
    product_list = ["Real-Time Payments", "Open Banking", "AI Fraud Monitor"]  # Fallback

st.subheader("Search Knowledge Base")

with st.form("product_research_form"):
    product_name = st.selectbox(
        "Product Name",
        options=product_list,
        placeholder="Select a product...",
        help="Product or service name",
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
                    timeout=30,
                )

                if response.status_code == 200:
                    result = response.json()
                    p_info = result.get("product_info", {})

                    # --- HERO SECTION ---
                    cat = p_info.get("category", "N/A")
                    # Color code category pill if possible (mock logic)
                    cat_pill = (
                        "pill-amber"
                        if "Security" in cat
                        else "pill-green" if "Payments" in cat else "pill-grey"
                    )

                    st.markdown(
                        f"""
                    <div style="margin-bottom: 2rem;">
                        <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; align-items: center; display: flex; gap: 1rem;">
                            {p_info.get('name', 'Product')}
                            <span class="status-pill {cat_pill}">{cat}</span>
                        </h1>
                        <p style="color: #737373; font-size: 1.1rem;">{p_info.get('description', '')}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # --- METRICS CARD ---
                    # Using the same glass-metrics-card class
                    st.markdown(
                        f"""
                    <div class="glass-metrics-card">
                        <div>
                            <span class="hero-metric-label">Pricing Model</span>
                            <span class="hero-metric-value" style="font-size: 1rem;">{p_info.get('pricing_model', 'N/A')}</span>
                        </div>
                        <div>
                            <span class="hero-metric-label">SLA Tier</span>
                            <span class="hero-metric-value">{p_info.get('sla_tier', 'Standard')}</span>
                        </div>
                        <div>
                            <span class="hero-metric-label">Source</span>
                            <span class="hero-metric-value" style="font-size: 1rem; color: #888;">Knowledge Base</span>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                    # --- DETAILS GRID ---
                    col_feat, col_req = st.columns(2, gap="large")

                    with col_feat:
                        st.markdown("### ✨ Key Features")
                        features = result.get("features", [])
                        if features:
                            for f in features:
                                # Using a card-like style for list items
                                st.markdown(
                                    f"""
                                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; color: #ddd; font-size: 0.9rem;">
                                    {f}
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("No features listed.")

                    with col_req:
                        st.markdown("### ⚙️ Technical Requirements")
                        reqs = result.get("requirements", {})
                        if reqs:
                            for k, v in reqs.items():
                                key_fmt = k.replace("_", " ").title()
                                st.markdown(
                                    f"""
                                <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                                    <span style="color: #737373; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;">{key_fmt}</span>
                                    <span style="color: #fff; font-weight: 500; text-align: right; max-width: 60%;">{v}</span>
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("No requirements listed.")

                elif response.status_code == 404:
                    st.warning("⚠️ Product not found")
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
