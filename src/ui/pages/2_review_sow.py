"""
SOW Review page.
"""

import io
import sys
from pathlib import Path

import requests
import streamlit as st

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css

try:
    from pypdf import PdfReader

    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document

    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

st.set_page_config(page_title="Review SOW", page_icon="✅", layout="wide")

# Apply shared styles
apply_custom_css()

# Page-specific CSS overrides (Matches Generate SOW)
st.markdown(
    """
<style>
    /* Force white text on primary buttons */
    div[data-testid="stButton"] > button[kind="primary"] p,
    div[data-testid="stFormSubmitButton"] button p {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    /* Force Red Background on Form Submit - High Specificity */
    div[data-testid="stFormSubmitButton"] button {
        background-color: #D92D20 !important;
        border: none !important;
        color: white !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State
if "review_result" not in st.session_state:
    st.session_state.review_result = None

# Header
# Dashboard Header
st.markdown(
    """
    <div style="margin-bottom: 1.5rem;">
        <h1 style="font-size: 1.75rem; font-weight: 700; margin-bottom: 0.25rem;">Review Statement of Work</h1>
        <p style="color: #666; font-size: 0.85rem;">Analyze SOWs for compliance with mandatory clauses and prohibited terms.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# API Configuration
API_URL = "http://localhost:8000"

# System Guidance (Sidebar) - REMOVED to align with Generate SOW page
# with st.sidebar:
#    ...

# Layout: Upload & Input
col_upload, col_settings = st.columns([2, 1], gap="medium")

sow_text = ""

with col_upload:
    # 1. Upload Section
    st.markdown('<span class="section-tag">Document Source</span>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload SOW (PDF, DOCX, MD, TXT)",
        type=["pdf", "docx", "md", "txt"],
        help="Drag and drop your SOW file here",
    )

    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_type == "pdf":
                if HAS_PDF:
                    reader = PdfReader(uploaded_file)
                    text = []
                    for page in reader.pages:
                        text.append(page.extract_text())
                    sow_text = "\n".join(text)
                    st.success(f"✅ Extracted {len(sow_text)} chars from PDF")
                else:
                    st.error("❌ pypdf library missing.")

            elif file_type in ["docx", "doc"]:
                if HAS_DOCX:
                    doc = Document(uploaded_file)
                    text = [p.text for p in doc.paragraphs]
                    sow_text = "\n".join(text)
                    st.success(f"✅ Extracted {len(sow_text)} chars from DOCX")
                else:
                    st.error("❌ python-docx library missing.")

            else:  # md, txt
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                sow_text = stringio.read()
                st.success(f"✅ Loaded {uploaded_file.name}")

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    sow_text_input = st.text_area(
        "SOW Content",
        value=sow_text,
        height=400,
        placeholder="Paste SOW text here if not uploading...",
        help="Edit content before analyzing",
    )

with col_settings:
    # 2. Configuration
    st.markdown('<span class="section-tag">Analysis Settings</span>', unsafe_allow_html=True)

    with st.form("review_settings"):
        product = st.text_input("Product Name", placeholder="e.g., Real-Time Payments")
        client_tier = st.selectbox("Client Tier", ["HIGH", "MEDIUM", "LOW", ""])
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.form_submit_button(
            "🔍 Analyze SOW", type="primary", use_container_width=True
        )

    # Review Guidance (Moved from Sidebar) - Wrapped in SaaS Card
    st.markdown(
        """
<div class="saas-card">
<div class="tip-group" style="padding-top: 0; border-top: none; gap: 10px;">
<span class="section-tag" style="margin-bottom: 0.5rem;">Review Guidance</span>
<div class="tip-item" style="gap: 10px;">
<div class="tip-icon" style="color: #D92D20;">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
</div>
<div class="tip-content" style="font-size: 0.8rem;">
<span class="tip-title" style="font-size: 0.8rem;">Compliance Scan</span>
<span class="tip-desc">Checks against mandatory clauses.</span>
</div>
</div>
<div class="tip-item" style="gap: 10px;">
<div class="tip-icon" style="color: #F59E0B;">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
</div>
<div class="tip-content" style="font-size: 0.8rem;">
<span class="tip-title" style="font-size: 0.8rem;">Risk Analysis</span>
<span class="tip-desc">Graded severity for all issues.</span>
</div>
</div>
<div class="tip-item" style="gap: 10px;">
<div class="tip-icon" style="color: #3B82F6;">
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
</div>
<div class="tip-content" style="font-size: 0.8rem;">
<span class="tip-title" style="font-size: 0.8rem;">Audit Trail</span>
<span class="tip-desc">Logged for QA purposes.</span>
</div>
</div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

# Analysis Logic
if analyze_btn:
    if not sow_text_input:
        st.error("❌ Please provide SOW content")
    else:
        with st.spinner("Analyzing compliance rules... This may take 1-2 minutes with Nova Pro."):
            # Construct payload
            payload = {"sow_text": sow_text_input}
            if product:
                payload["product"] = product
            if client_tier:
                payload["client_tier"] = client_tier

            try:
                response = requests.post(f"{API_URL}/api/v1/sow/review", json=payload, timeout=300)

                if response.status_code == 200:
                    st.session_state.review_result = response.json()
                    # Store input text too for display
                    st.session_state.review_text = sow_text_input
                    st.rerun()
                else:
                    st.error(f"API Error: {response.text}")

            except requests.exceptions.Timeout:
                st.error("❌ Request timed out.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to API.")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Render Results
if st.session_state.review_result:
    result = st.session_state.review_result
    sow_content = st.session_state.get("review_text", "")

    score = result["compliance_score"]
    status = result["status"]
    summary = result["summary"]
    issues = result.get("issues", [])

    st.markdown("<br>", unsafe_allow_html=True)

    # 1. Action Toolbar
    st.markdown(
        """
<style>
    .integrated-toolbar {
        background: #111;
        border: 1px solid #222;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="integrated-toolbar">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(
            f"**Analysis Complete** &nbsp; <span style='color:#666'>|</span> &nbsp; Score: **{score}/100**",
            unsafe_allow_html=True,
        )
    with c2:
        if st.button("Clear Results", type="secondary", use_container_width=False):
            st.session_state.review_result = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. Compliance Report (Top-Posted)
    st.markdown(
        f"""
<div class="saas-card" style="border-left: 4px solid #D92D20; background: rgba(217, 45, 32, 0.03); margin-bottom: 2rem;">
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
        <div style="color: #fff; font-size: 1.1rem; font-weight: 600;">{summary.get('HIGH', 0)}</div>
    </div>
    <div style="background: rgba(5,5,5,0.4); padding: 12px; border-radius: 8px; border: 1px solid #222; text-align: center;">
        <div style="color: #F59E0B; font-weight: 700; font-size: 0.7rem; margin-bottom: 4px;">MEDIUM RISK</div>
        <div style="color: #fff; font-size: 1.1rem; font-weight: 600;">{summary.get('MEDIUM', 0)}</div>
    </div>
    <div style="background: rgba(5,5,5,0.4); padding: 12px; border-radius: 8px; border: 1px solid #222; text-align: center;">
        <div style="color: #10B981; font-weight: 700; font-size: 0.7rem; margin-bottom: 4px;">LOW RISK</div>
        <div style="color: #fff; font-size: 1.1rem; font-weight: 600;">{summary.get('LOW', 0)}</div>
    </div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    # Detailed Issues
    if issues:
        st.subheader("Risk Analysis Details")
        for issue in issues:
            severity_icon = (
                "🔴"
                if issue["severity"] == "HIGH"
                else "🟡" if issue["severity"] == "MEDIUM" else "🟢"
            )

            # Create a more descriptive label
            label = f"{severity_icon} {issue['category']}"
            if "Prohibited Term" in issue["category"]:
                term = issue["description"].replace("Found prohibited term: ", "")
                label += f": {term}"
            elif "Mandatory Clause" in issue["category"]:
                clause = issue["description"].replace("Missing required clause: ", "")
                label += f": {clause}"

            with st.expander(label):
                st.write(f"**Description:** {issue['description']}")
                st.info(f"💡 **Suggestion:** {issue['suggestion']}")
    else:
        st.balloons()
        st.success("🎉 No compliance issues found! Perfect score.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Document Canvas
    if sow_content:
        st.markdown(
            '<span class="section-tag" style="margin-left: 4px;">Analyzed Document</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
    <div class="document-canvas" style="border-radius: 12px; margin-top: 0.5rem;">
    {sow_content}
    </div>
    """,
            unsafe_allow_html=True,
        )
