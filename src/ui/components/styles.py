"""
Shared Streamlit UI styles and components.
Centralized CSS for the "Cuscal" Enterprise Dark Theme.
"""

import streamlit as st

def apply_custom_css():
    """
    Applies the global custom CSS for the Cuscal brand theme.
    """
    st.markdown(
        """
        <style>
        /* IMPORT FONTS */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        /* GLOBAL RESET & VARIABLES */
        :root {
            --bg-color: #050505;
            --card-bg: #111111;
            --card-border: #222222;
            --text-primary: #FFFFFF;
            --text-secondary: #888888;
            --accent-red: #D92D20;
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        html, body, [class*="css"] {
            font-family: var(--font-family) !important;
            color: var(--text-primary);
        }

        /* APP BACKGROUND */
        .stApp {
            background-color: var(--bg-color);
        }
        
        /* HIDE DEFAULT STREAMLIT ELEMENTS */
        [data-testid="stHeader"] { display: none; }
        footer { display: none !important; }
        
        /* CONTAINER SPACING */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }

        /* CUSTOM HEADER */
        .cuscal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem 0;
            margin-bottom: 1.5rem;
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        .logo-square {
            width: 12px;
            height: 12px;
            background-color: var(--accent-red);
            display: inline-block;
        }

        .login-link {
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .login-link:hover {
            color: var(--text-primary);
        }

        /* HERO SECTION */
        .hero-section {
            text-align: center;
            margin-bottom: 4rem;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            margin-bottom: 1rem;
        }
        
        .hero-subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto;
        }

        /* AGENT CARD STYLES */
        .agent-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 24px;
            height: 320px;
            display: flex;
            flex-direction: column;
            text-decoration: none !important;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .agent-card:hover {
            border-color: #444;
            transform: translateY(-2px);
        }
        
        .card-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #1A1A1A;
            color: var(--accent-red); /* Default accent */
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            font-size: 1.2rem;
        }
        
        /* Icon Colors specific variants if needed, but keeping it uniform for consistency */
        .icon-sow { color: #D92D20; background: rgba(217, 45, 32, 0.1); }
        .icon-audit { color: #D92D20; background: rgba(217, 45, 32, 0.1); }
        .icon-intel { color: #F59E0B; background: rgba(245, 158, 11, 0.1); }
        .icon-kb { color: #F59E0B; background: rgba(245, 158, 11, 0.1); }

        .card-title {
            color: var(--text-primary);
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        
        .card-description {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.5;
            flex-grow: 1;
        }
        
        .card-action {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: auto;
            color: var(--text-primary);
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        .card-arrow {
            transition: transform 0.2s ease;
        }
        
        .agent-card:hover .card-arrow {
            transform: translateX(4px);
        }

        /* FORM ELEMENTS OVERRIDES (For other pages) */
        .stTextInput > div > div > input, .stSelectbox > div > div {
            background-color: var(--card-bg) !important;
            border-color: var(--card-border) !important;
            color: white !important;
        }
        
        .stButton > button[kind="primary"] {
            background-color: var(--accent-red) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
        }

        /* PUSH FOOTER TO BOTTOM */
        /* Enable flex column on the sidebar content wrapper */
        section[data-testid="stSidebar"] > div:nth-of-type(1) {
             height: auto; /* Allow height to adjust dynamically */
             min-height: 100vh; /* Ensure it takes at least the full viewport height */
             display: flex;
             flex-direction: column;
        }
        
        /* The main scrollable content area */
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
            display: flex;
            flex-direction: column;
            flex-grow: 1; /* Allow content to grow and push footer down */
            padding-bottom: 0rem !important; /* Remove excessive padding */
            overflow: hidden !important; /* Hide scrollbar if content fits */
        }
        
        /* REFINED SIDEBAR FOOTER */
        /* The container wrapping our footer */
        section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] > div:has(.sidebar-footer) {
             margin-top: auto;
             padding-bottom: 0 !important;
        }

        .sidebar-footer {
            background-color: #0A0A0A;
            border: 1px solid #222;
            border-radius: 12px;
            padding: 1rem;
            margin: 0 0.5rem 1rem 0.5rem;
            width: auto;
            margin-top: auto;
        }

        /* Status Section */
        .status-section {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .status-row {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: #10B981; /* Emerald 500 */
            border-radius: 50%;
            box-shadow: 0 0 8px rgba(16, 185, 129, 0.4);
            animation: pulse 2s infinite;
        }

        .status-text {
            color: #34D399; /* Emerald 400 */
            font-size: 0.85rem;
            font-weight: 500;
            letter-spacing: 0.02em;
        }

        .engine-info {
            color: #525252; /* Neutral 600/700 equivalent */
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            font-weight: 600;
            margin-top: 4px;
        }

        /* PREMIUM SAAS CARD SYSTEM (Glassmorphism) */
        .saas-card {
            background: rgba(20, 20, 20, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .section-tag {
            font-size: 0.6rem;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 0.75rem;
            display: block;
        }

        .metric-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 1.5rem;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .metric-label {
            font-size: 0.85rem;
            color: #888;
        }

        .metric-value {
            font-size: 0.85rem;
            color: #fff;
            font-weight: 500;
            font-family: 'Courier New', monospace;
        }

        .tip-group {
            display: flex;
            flex-direction: column;
            gap: 12px;
            padding-top: 1.25rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        .tip-item {
            display: flex;
            gap: 12px;
        }

        .tip-icon {
            flex-shrink: 0;
            margin-top: 2px;
        }

        .tip-content {
            font-size: 0.85rem;
            line-height: 1.5;
        }

        .tip-title {
            color: #ddd;
            font-weight: 600;
            margin-bottom: 2px;
            display: block;
        }

        .tip-desc {
            color: #777;
        }

        /* DOCUMENT PREVIEW & TOOLBAR */
        .document-toolbar {
            background: #111;
            border: 1px solid #222;
            border-bottom: none;
            border-radius: 12px 12px 0 0;
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .telemetry-tag {
            font-family: 'Courier New', monospace;
            font-size: 0.7rem;
            color: #10B981;
            background: rgba(16, 185, 129, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .document-canvas {
            background: #0f0f0f;
            border: 1px solid #222;
            border-radius: 0 0 12px 12px;
            padding: 3rem 4rem;
            font-family: 'Inter', -apple-system, sans-serif;
            color: #ccc;
            line-height: 1.7;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
        }

        .document-canvas h1, .document-canvas h2, .document-canvas h3 {
            color: #fff;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        .document-canvas strong {
            color: #eee;
        }

        .document-canvas p {
            margin-bottom: 1.25rem;
        }

        @keyframes pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(0.95); }
            100% { opacity: 1; transform: scale(1); }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

def main_header(title: str, subtitle: str):
    """
    Renders the consistent main header.
    DEPRECATED for Homepage, used for sub-pages.
    """
    st.markdown(
        f"""
        <div class="main-header" style="text-align: center; margin-bottom: 2rem;">
            <h1>{title}</h1>
            <p style="color: #888;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
