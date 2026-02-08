"""
Shared Streamlit UI styles and components.
Centralized CSS for the "Warm Dark Mode" Cuscal Brand Theme.
"""

import streamlit as st

def apply_custom_css():
    """
    Applies the global custom CSS for the Warm Dark Mode Cuscal brand theme.
    This ensures all pages have a consistent look and feel.
    """
    st.markdown(
        """
        <style>
        /* GLOBAL: Force the "Void" background */
        .stApp {
            background-color: #0a0a0a;
        }
        
        /* AMBIENT GLOWS: Golden Amber (Top-Left) + Brand Red (Bottom-Right) */
        .stApp::before {
            content: "";
            position: fixed;
            top: -20%;
            left: -10%;
            width: 500px;
            height: 500px;
            background: rgba(245, 158, 11, 0.4);
            border-radius: 50%;
            filter: blur(120px);
            pointer-events: none;
            z-index: 0;
        }
        
        .stApp::after {
            content: "";
            position: fixed;
            bottom: -20%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: rgba(217, 45, 32, 0.4);
            border-radius: 50%;
            filter: blur(120px);
            pointer-events: none;
            z-index: 0;
        }
        
        /* GLOBAL: Kill all underlines */
        a {
            text-decoration: none !important;
        }
        
        /* HEADER: Kill the massive white space at the top */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }
        
        /* SIDEBAR: Aggressive top spacing removal */
        section[data-testid="stSidebar"] > div {
            padding-top: 1rem !important;
        }
        
        /* SIDEBAR: Target Streamlit's emotion cache class */
        section[data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
            margin-top: -20px;
        }
        
        /* SIDEBAR: Professional Dark Glassmorphism */
        [data-testid="stSidebar"] {
            background-color: rgba(10, 10, 10, 0.5) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(24px);
            width: 16rem !important;
            min-width: 16rem !important;
            max-width: 16rem !important;
        }
        
        /* Hide default Streamlit header */
        [data-testid="stHeader"] {
            display: none;
        }
        
        /* NAV LINKS: Professional hover states */
        [data-testid="stSidebarNav"] {
            padding-top: 1rem;
        }
        
        /* Sidebar Navigation Links */
        [data-testid="stSidebarNav"] a {
            color: #a3a3a3 !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            padding: 0.75rem 1rem !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            position: relative !important;
        }
        
        /* Hover State */
        [data-testid="stSidebarNav"] a:hover {
            color: #ffffff !important;
            background: rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Active State - Brand Red with Glow Indicator */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            color: #D92D20 !important;
            background: linear-gradient(to right, rgba(217, 45, 32, 0.1), transparent) !important;
        }
        
        /* Active Indicator - Vertical Glowing Line */
        [data-testid="stSidebarNav"] a[aria-current="page"]::before {
            content: "";
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 24px;
            background: #D92D20;
            border-radius: 0 4px 4px 0;
            box-shadow: 0 0 10px #D92D20;
        }
        
        /* Main menu section styling */
        [data-testid="stSidebarNav"] > ul {
            padding: 0;
        }
        
        /* Individual nav items */
        [data-testid="stSidebarNav"] li {
            margin-bottom: 0.25rem;
        }
        
        /* STATUS FOOTER: Engineering Telemetry */
        .status-footer {
            margin-top: auto;
            padding-top: 2rem;
        }
        
        .status-dot {
            height: 6px;
            width: 6px;
            background-color: #10B981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 6px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .status-text {
            color: #737373;
            font-size: 12px;
            letter-spacing: 0.15em;
            text-transform: uppercase;
        }
        
        .status-value {
            color: #ffffff;
            font-size: 14px;
            font-weight: 700;
        }
        
        /* Typography */
        h1, h2, h3 { 
            color: #ffffff !important; 
            font-weight: 600; 
        }
        p, .stMarkdown { 
            color: #a3a3a3 !important; 
        }
        
        /* Header Styling */
        .main-header {
            text-align: center;
            padding: 1.5rem 0 0 0;
            margin-bottom: 1.5rem;
            position: relative;
            z-index: 1;
            flex-shrink: 0;
        }
        .main-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.25rem;
            letter-spacing: -0.03em;
            color: #ffffff !important;
        }
        .main-header p {
            color: #9ca3af;
            font-size: 0.95rem;
            margin-top: 0.5rem;
        }
        
        /* Streamlit Columns - Equal Height */
        [data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 1.5rem;
        }
        
        [data-testid="column"] > div {
            flex: 1;
            display: flex;
        }
        
        /* FORM INPUTS: Glassmorphic Style */
        input[type="text"], 
        textarea, 
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            padding: 0.75rem !important;
            transition: all 0.2s ease !important;
        }
        
        /* SELECTBOX: Complete override to fix invisible text */
        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
        }
        
        /* Target ALL text elements inside selectbox */
        .stSelectbox,
        .stSelectbox *,
        .stSelectbox div,
        .stSelectbox span,
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] *,
        .stSelectbox [data-baseweb="select"] div,
        .stSelectbox [data-baseweb="select"] span {
            color: #ffffff !important;
        }
        
        /* Force selectbox container to show overflow */
        .stSelectbox [data-baseweb="select"],
        .stSelectbox [data-baseweb="select"] > div {
            overflow: visible !important;
        }
        
        /* Input placeholder text */
        input::placeholder,
        textarea::placeholder {
            color: #737373 !important;
            opacity: 0.7 !important;
        }
        
        /* Input Focus State - Brand Red Glow */
        input[type="text"]:focus,
        textarea:focus,
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #D92D20 !important;
            box-shadow: 0 0 0 1px #D92D20, 0 0 20px rgba(217, 45, 32, 0.3) !important;
            outline: none !important;
        }
        
        /* PRIMARY BUTTON: Brand Red */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #D92D20 0%, #B71C1C 100%) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 0.75rem 2rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(217, 45, 32, 0.4) !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #EF4444 0%, #D92D20 100%) !important;
            box-shadow: 0 6px 20px rgba(217, 45, 32, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        
        /* SECONDARY BUTTON */
        .stButton > button {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        
        .stButton > button:hover {
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        /* DOCUMENT CONTAINER: Legal Paper Style */
        .document-container {
            background: rgba(20, 20, 20, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 2.5rem;
            margin: 2rem 0;
            position: relative;
            z-index: 1;
        }
        
        /* Serif typography for document content */
        .document-container h1,
        .document-container h2,
        .document-container h3 {
            font-family: 'Georgia', 'Times New Roman', serif !important;
            color: #ffffff !important;
            margin-top: 1.5rem;
        }
        
        .document-container p {
            font-family: 'Georgia', 'Times New Roman', serif !important;
            line-height: 1.8;
            color: #d1d1d1 !important;
        }
        
        /* Glass Card Styles - updated for better contrast */
        .glass-card {
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        
        .glass-card:hover {
            background: rgba(0, 0, 0, 0.7);
            border-color: rgba(255, 255, 255, 0.15);
        }
        
        /* Accent colors for cards */
        .accent-purple { border-top: 3px solid #8B5CF6; }
        .accent-orange { border-top: 3px solid #F97316; }
        .accent-red { border-top: 3px solid #EF4444; }
        .accent-green { border-top: 3px solid #10B981; }
        
        /* Icon backgrounds */
        .card-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        }
        
        .icon-bg-purple { background: rgba(139, 92, 246, 0.15); color: #A78BFA; }
        .icon-bg-orange { background: rgba(249, 115, 22, 0.15); color: #FB923C; }
        .icon-bg-red { background: rgba(239, 68, 68, 0.15); color: #FCA5A5; }
        .icon-bg-green { background: rgba(16, 185, 129, 0.15); color: #6EE7B7; }
        
        /* Compact card variant */
        .compact-card {
            padding: 1.25rem !important;
        }
        
        /* Metric styling */
        .dashboard-metric {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
        }
        
        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .metric-row:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        
        .metric-value {
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
        }
        
        .metric-label {
            font-size: 0.75rem;
            color: #737373;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 1rem 0;
            color: #525252;
            font-size: 0.8rem;
            position: relative;
            z-index: 1;
            flex-shrink: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main_header(title: str, subtitle: str):
    """
    Renders the consistent main header.
    """
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
