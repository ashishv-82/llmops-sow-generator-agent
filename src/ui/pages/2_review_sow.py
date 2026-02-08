"""
SOW Review page.
"""

import streamlit as st
import requests
import io
import sys
from pathlib import Path

# Add project root to sys.path
root_path = Path(__file__).parent.parent.parent.parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

from src.ui.components.styles import apply_custom_css, main_header
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

# Header
main_header(
    "Review Statement of Work",
    "Check compliance issues against mandatory clauses and risk factors."
)

# API endpoint (hidden)
with st.sidebar:
    st.header("Configuration")
    API_URL = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="FastAPI backend URL"
    )

st.markdown("---")

# Layout: Upload & Input
col_upload, col_settings = st.columns([3, 1])

sow_text = ""

with col_upload:
    st.subheader("1. Upload or Paste SOW")
    
    uploaded_file = st.file_uploader(
        "Upload SOW (PDF, DOCX, MD, TXT)", 
        type=["pdf", "docx", "md", "txt"],
        help="Drag and drop your SOW file here"
    )
    
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1].lower()
        try:
            if file_type == 'pdf':
                if HAS_PDF:
                    reader = PdfReader(uploaded_file)
                    text = []
                    for page in reader.pages:
                        text.append(page.extract_text())
                    sow_text = "\n".join(text)
                    st.success(f"✅ Extracted {len(sow_text)} chars from PDF")
                else:
                    st.error("❌ pypdf library missing.")
            
            elif file_type in ['docx', 'doc']:
                if HAS_DOCX:
                    doc = Document(uploaded_file)
                    text = [p.text for p in doc.paragraphs]
                    sow_text = "\n".join(text)
                    st.success(f"✅ Extracted {len(sow_text)} chars from DOCX")
                else:
                    st.error("❌ python-docx library missing.")
            
            else: # md, txt
                stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
                sow_text = stringio.read()
                st.success(f"✅ Loaded {uploaded_file.name}")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

    sow_text_input = st.text_area(
        "SOW Content",
        value=sow_text,
        height=300,
        placeholder="Paste SOW text here if not uploading...",
        help="Edit content before analyzing"
    )

with col_settings:
    st.subheader("2. Configuration")
    with st.form("review_settings"):
        product = st.text_input("Product Name", placeholder="e.g., Real-Time Payments")
        client_tier = st.selectbox("Client Tier", ["HIGH", "MEDIUM", "LOW", ""])
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.form_submit_button("🔍 Analyze SOW", use_container_width=True)

# Analysis Logic
if analyze_btn:
    if not sow_text_input:
        st.error("❌ Please provide SOW content")
    else:
        with st.spinner("Analyzing compliance rules... This may take 1-2 minutes with Nova Pro."):
            # Construct payload
            payload = {"sow_text": sow_text_input}
            if product: payload["product"] = product
            if client_tier: payload["client_tier"] = client_tier
            
            try:
                response = requests.post(f"{API_URL}/api/v1/sow/review", json=payload, timeout=300)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Store results in variables
                    score = result['compliance_score']
                    status = result['status']
                    summary = result['summary']
                    issues = result.get('issues', [])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Determine accent color based on status
                    accent_class = "accent-green" if status == "PASS" else "accent-orange" if status == "WARNING" else "accent-red"
                    icon_bg_class = "icon-bg-green" if status == "PASS" else "icon-bg-orange" if status == "WARNING" else "icon-bg-red"
                    
                    # Render Compliance Card
                    st.markdown(f"""
<div class="glass-card {accent_class} compact-card">
<div style="display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 1rem;">
<div class="card-icon {icon_bg_class}" style="margin-bottom:0;">
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
<div><div style="color: #EF4444; font-weight:700;">HIGH RISK</div><div>{summary.get('HIGH', 0)}</div></div>
<div><div style="color: #F59E0B; font-weight:700;">MEDIUM RISK</div><div>{summary.get('MEDIUM', 0)}</div></div>
<div><div style="color: #10B981; font-weight:700;">LOW RISK</div><div>{summary.get('LOW', 0)}</div></div>
</div>
</div>
""", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)

                    if issues:
                        st.subheader("Risk Analysis Details")
                        
                        high = [i for i in issues if i['severity']=='HIGH']
                        med = [i for i in issues if i['severity']=='MEDIUM']
                        low = [i for i in issues if i['severity']=='LOW']
                        
                        if high:
                            with st.expander(f"🔴 High Severity ({len(high)})", expanded=True):
                                for i in high:
                                    st.error(f"**{i['category']}**: {i['description']}")
                                    if i.get('suggestion'): st.write(f"💡 **Suggestion**: {i['suggestion']}")
                        if med:
                            with st.expander(f"🟡 Medium Severity ({len(med)})", expanded=True):
                                for i in med:
                                    st.warning(f"**{i['category']}**: {i['description']}")
                                    if i.get('suggestion'): st.write(f"💡 **Suggestion**: {i['suggestion']}")
                        if low:
                            with st.expander(f"🟢 Low Severity ({len(low)})", expanded=False):
                                for i in low:
                                    st.info(f"**{i['category']}**: {i['description']}")
                                    if i.get('suggestion'): st.write(f"💡 **Suggestion**: {i['suggestion']}")
                    else:
                        st.balloons()
                        st.success("🎉 No compliance issues found! Perfect score.")
                        
                else:
                    st.error(f"API Error: {response.text}")
                    
            except requests.exceptions.Timeout:
                 st.error("❌ Request timed out.")
            except requests.exceptions.ConnectionError:
                 st.error("❌ Could not connect to API.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
