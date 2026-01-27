"""
Macro Dashboard - Streamlit UI
Interactive frontend for economic and market indicators
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import os

# Configuration - use environment variable for deployed version
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")
if API_BASE and not API_BASE.startswith("http"):
    API_BASE = f"https://{API_BASE}"
st.set_page_config(
    page_title="Macro Dashboard",
    page_icon="📊",
    layout="wide"
)

# Design System CSS - Based on DESIGN_SYSTEM.md v2.0
# Load fonts via <link> tags (more reliable than @import in inline styles)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
    /* ============================================
       DESIGN SYSTEM v2.0 - CSS CUSTOM PROPERTIES
       Philosophy: Clean, data-first, professional
       ============================================ */
    :root {
        /* === TYPOGRAPHY === */
        --font-family: 'Urbanist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

        /* Type Scale */
        --text-display: 32px;
        --text-h1: 24px;
        --text-h2: 20px;
        --text-h3: 16px;
        --text-body: 14px;
        --text-caption: 12px;
        --text-metric-lg: 36px;
        --text-metric-sm: 24px;

        /* === COLORS - BACKGROUNDS === */
        --color-bg-primary: #0a0a0a;
        --color-bg-secondary: #141414;
        --color-bg-tertiary: #1e1e1e;
        --color-bg-overlay: rgba(0, 0, 0, 0.8);

        /* === COLORS - TEXT === */
        --color-text-primary: #ffffff;
        --color-text-secondary: #a3a3a3;
        --color-text-tertiary: #737373;
        --color-text-disabled: #525252;

        /* === COLORS - BORDERS === */
        --color-border-subtle: #262626;
        --color-border-default: #404040;
        --color-border-strong: #525252;

        /* === COLORS - ACCENT (Teal) === */
        --color-accent-primary: #14b8a6;
        --color-accent-hover: #0d9488;
        --color-accent-active: #0f766e;
        --color-accent-subtle: rgba(20, 184, 166, 0.1);
        --color-accent-border: rgba(20, 184, 166, 0.3);

        /* === COLORS - STATUS === */
        --color-success: #10b981;
        --color-success-bg: rgba(16, 185, 129, 0.1);
        --color-warning: #f59e0b;
        --color-warning-bg: rgba(245, 158, 11, 0.1);
        --color-danger: #ef4444;
        --color-danger-bg: rgba(239, 68, 68, 0.1);
        --color-info: #3b82f6;
        --color-info-bg: rgba(59, 130, 246, 0.1);

        /* === COLORS - CHARTS === */
        --color-chart-1: #14b8a6;
        --color-chart-2: #8b5cf6;
        --color-chart-3: #f59e0b;
        --color-chart-4: #ec4899;
        --color-chart-5: #06b6d4;
        --color-chart-grid: rgba(255, 255, 255, 0.05);
        --color-chart-axis: #737373;

        /* === SPACING === */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;
        --space-2xl: 48px;

        /* === BORDER RADIUS === */
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-full: 9999px;

        /* === SHADOWS === */
        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 12px 24px rgba(0, 0, 0, 0.5);
        --shadow-accent: 0 0 16px rgba(20, 184, 166, 0.3);

        /* === TRANSITIONS === */
        --transition-fast: 100ms ease-out;
        --transition-base: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 250ms ease-in-out;
    }

    /* ============================================
       FONTS & BASE
       ============================================ */
    html, body, [class*="st-"], .stMarkdown, .stText {
        font-family: var(--font-family) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Material Icons - CRITICAL: Ensure icon font renders correctly */
    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    span[translate="no"] {
        font-family: 'Material Symbols Rounded' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 20px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
        font-feature-settings: 'liga';
        font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    }

    /* ============================================
       ANIMATIONS & KEYFRAMES
       ============================================ */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    /* ============================================
       MAIN LAYOUT & BACKGROUND
       ============================================ */
    .main {
        background: var(--color-bg-primary) !important;
    }

    .main .block-container {
        padding: var(--space-lg) var(--space-xl) var(--space-2xl) var(--space-xl);
        max-width: 1400px;
        animation: fadeIn 200ms ease-out;
    }

    /* ============================================
       TYPOGRAPHY
       ============================================ */
    h1 {
        font-family: var(--font-family) !important;
        font-size: var(--text-display);
        font-weight: 700;
        color: var(--color-accent-primary);
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin-bottom: var(--space-sm);
    }

    h2 {
        font-family: var(--font-family) !important;
        font-size: var(--text-h1);
        font-weight: 600;
        color: var(--color-accent-primary);
        letter-spacing: 0;
        line-height: 1.3;
        margin-top: var(--space-2xl);
        margin-bottom: var(--space-lg);
        padding-bottom: var(--space-sm);
        border-bottom: 2px solid var(--color-accent-primary);
    }

    h3 {
        font-family: var(--font-family) !important;
        font-size: var(--text-h2);
        font-weight: 600;
        color: var(--color-accent-primary);
        letter-spacing: 0;
        line-height: 1.4;
    }

    h4, h5, h6 {
        font-family: var(--font-family) !important;
        font-size: var(--text-h3);
        font-weight: 500;
        color: var(--color-text-primary);
    }

    p, li {
        font-family: var(--font-family) !important;
        font-size: var(--text-body);
        font-weight: 400;
        color: var(--color-text-secondary);
        line-height: 1.6;
    }

    /* Markdown text in containers */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--color-text-secondary);
    }

    [data-testid="stMarkdownContainer"] strong {
        color: var(--color-text-primary);
        font-weight: 600;
    }

    /* ============================================
       SIDEBAR - Linear-inspired
       ============================================ */
    [data-testid="stSidebar"] {
        background: var(--color-bg-secondary) !important;
        border-right: 1px solid var(--color-border-subtle);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: var(--space-lg);
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-size: var(--text-caption);
        font-weight: 600;
        color: var(--color-text-tertiary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: var(--space-lg);
        margin-bottom: var(--space-sm);
        border-bottom: none;
        padding-bottom: 0;
    }

    /* Sidebar nav items (radio buttons) */
    [data-testid="stSidebar"] .stRadio > div {
        gap: var(--space-xs);
    }

    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        border-radius: var(--radius-sm);
        padding: var(--space-sm) var(--space-md);
        margin: 0;
        transition: var(--transition-base);
        cursor: pointer;
    }

    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: var(--color-accent-subtle);
    }

    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background: var(--color-accent-primary) !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label span {
        color: var(--color-text-secondary);
        font-size: var(--text-body);
        font-weight: 500;
        transition: var(--transition-base);
    }

    [data-testid="stSidebar"] .stRadio > div > label:hover span {
        color: var(--color-text-primary);
    }

    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] span {
        color: white !important;
        font-weight: 600;
    }

    /* ============================================
       METRIC CARDS - Stripe-inspired
       ============================================ */
    [data-testid="stMetric"] {
        background: var(--color-bg-secondary) !important;
        border: 1px solid var(--color-border-subtle);
        border-left: 3px solid var(--color-accent-primary);
        border-radius: var(--radius-md);
        padding: var(--space-md);
        transition: var(--transition-base);
        min-height: 120px;
    }

    [data-testid="stMetric"]:hover {
        background: var(--color-bg-tertiary) !important;
        border-color: var(--color-accent-border);
        border-left-color: var(--color-accent-hover);
    }

    [data-testid="stMetricLabel"] {
        font-family: var(--font-family) !important;
        font-size: var(--text-caption);
        font-weight: 400;
        color: var(--color-text-secondary);
        text-transform: none;
        letter-spacing: 0;
    }

    [data-testid="stMetricValue"] {
        font-family: var(--font-family) !important;
        font-size: var(--text-metric-lg);
        font-weight: 700;
        color: var(--color-text-primary);
        letter-spacing: -0.02em;
        line-height: 1.2;
    }

    [data-testid="stMetricDelta"] {
        font-size: var(--text-body);
        font-weight: 500;
    }

    [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Up"] {
        color: var(--color-success);
    }
    [data-testid="stMetricDelta"] svg[data-testid="stMetricDeltaIcon-Down"] {
        color: var(--color-danger);
    }

    [data-testid="stMetricDelta"] > div {
        color: var(--color-text-secondary);
    }

    /* Positive/Negative delta colors */
    [data-testid="stMetricDelta"][data-testid-delta="positive"] > div {
        color: var(--color-success);
    }
    [data-testid="stMetricDelta"][data-testid-delta="negative"] > div {
        color: var(--color-danger);
    }

    /* ============================================
       BUTTONS
       ============================================ */
    /* Primary Button */
    .stButton > button {
        height: 40px;
        padding: 0 var(--space-md);
        background: var(--color-accent-primary);
        color: white;
        border: none;
        border-radius: var(--radius-sm);
        font-family: var(--font-family);
        font-size: var(--text-body);
        font-weight: 500;
        transition: var(--transition-base);
        box-shadow: none;
    }

    .stButton > button:hover {
        background: var(--color-accent-hover);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .stButton > button:active {
        background: var(--color-accent-active);
        transform: translateY(0);
        box-shadow: none;
    }

    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: var(--color-accent-primary);
        color: white;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: var(--color-accent-hover);
    }

    /* Secondary/Download Button */
    .stDownloadButton > button {
        background: transparent;
        border: 1px solid var(--color-border-default);
        color: var(--color-text-primary);
        transition: var(--transition-base);
    }

    .stDownloadButton > button:hover {
        background: var(--color-bg-tertiary);
        border-color: var(--color-accent-border);
        transform: translateY(-1px);
    }

    /* ============================================
       FORM CONTROLS
       ============================================ */
    /* Labels */
    .stSelectbox > label,
    .stMultiSelect > label,
    .stTextInput > label,
    .stNumberInput > label,
    [data-testid="stWidgetLabel"] {
        font-size: var(--text-caption);
        font-weight: 500;
        color: var(--color-text-secondary) !important;
        margin-bottom: var(--space-xs);
    }

    /* Select boxes */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--color-bg-secondary) !important;
        border: 1px solid var(--color-border-default);
        border-radius: var(--radius-sm);
        transition: var(--transition-base);
    }

    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: var(--color-accent-border);
    }

    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within {
        border-color: var(--color-accent-primary);
        box-shadow: 0 0 0 2px var(--color-accent-subtle);
    }

    /* Select text color */
    .stSelectbox [data-baseweb="select"] span,
    .stMultiSelect [data-baseweb="select"] span {
        color: var(--color-text-primary) !important;
        font-size: var(--text-body);
    }

    /* Toggle */
    .stCheckbox, .stRadio {
        transition: var(--transition-base);
    }

    /* ============================================
       CHARTS - Clean, data-first
       ============================================ */
    .stPlotlyChart {
        background: var(--color-bg-secondary);
        border-radius: var(--radius-md);
        padding: var(--space-lg);
        border: none;
        transition: var(--transition-base);
    }

    .js-plotly-plot {
        border-radius: var(--radius-md);
        overflow: hidden;
    }

    /* ============================================
       EXPANDERS
       ============================================ */
    [data-testid="stExpander"] {
        border: 1px solid var(--color-border-subtle);
        border-left: 3px solid var(--color-accent-primary);
        border-radius: var(--radius-md);
        overflow: hidden;
        margin-bottom: var(--space-sm);
    }

    [data-testid="stExpander"] summary {
        background: var(--color-bg-secondary);
        padding: var(--space-md);
        transition: var(--transition-base);
    }

    [data-testid="stExpander"] summary:hover {
        background: var(--color-bg-tertiary);
        border-left-color: var(--color-accent-hover);
    }

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: var(--color-bg-secondary);
        padding: var(--space-md);
        border-top: 1px solid var(--color-border-subtle);
    }

    /* ============================================
       ALERTS & NOTIFICATIONS
       ============================================ */
    .stAlert {
        background: var(--color-bg-secondary) !important;
        border: 1px solid var(--color-border-subtle) !important;
        border-radius: var(--radius-md);
        padding: var(--space-md);
    }

    /* Warning */
    .stAlert[data-baseweb="notification"][kind="warning"] {
        border-left: 3px solid var(--color-warning) !important;
        background: var(--color-warning-bg) !important;
    }

    /* Success */
    .stAlert[data-baseweb="notification"][kind="success"] {
        border-left: 3px solid var(--color-success) !important;
        background: var(--color-success-bg) !important;
    }

    /* Error */
    .stAlert[data-baseweb="notification"][kind="error"] {
        border-left: 3px solid var(--color-danger) !important;
        background: var(--color-danger-bg) !important;
    }

    /* Info */
    .stAlert[data-baseweb="notification"][kind="info"] {
        border-left: 3px solid var(--color-info) !important;
        background: var(--color-info-bg) !important;
    }

    /* ============================================
       DATA TABLES
       ============================================ */
    .stDataFrame {
        background: var(--color-bg-secondary) !important;
        border: 1px solid var(--color-border-subtle);
        border-radius: var(--radius-md);
        overflow: hidden;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: var(--color-bg-secondary);
    }

    /* ============================================
       TABS
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: var(--space-xs);
        border-bottom: 1px solid var(--color-border-subtle);
        padding-bottom: 0;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        color: var(--color-text-secondary);
        font-weight: 500;
        padding: var(--space-sm) var(--space-md);
        transition: var(--transition-base);
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--color-text-primary);
        background: transparent;
    }

    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: var(--color-accent-primary) !important;
        border-bottom-color: var(--color-accent-primary) !important;
    }

    /* ============================================
       DIVIDERS
       ============================================ */
    hr {
        border: none !important;
        height: 1px;
        background: var(--color-border-subtle);
        margin: var(--space-lg) 0;
    }

    /* ============================================
       SCROLLBARS
       ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--color-border-default);
        border-radius: var(--radius-full);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--color-border-strong);
    }

    /* ============================================
       TOOLTIPS
       ============================================ */
    [data-baseweb="tooltip"] {
        background: var(--color-bg-tertiary) !important;
        border: 1px solid var(--color-border-default);
        border-radius: var(--radius-sm);
        color: var(--color-text-primary);
        font-size: var(--text-caption);
    }

    /* ============================================
       LIVE INDICATOR
       ============================================ */
    .live-indicator {
        display: inline-flex;
        align-items: center;
        gap: var(--space-sm);
        font-size: var(--text-caption);
        color: var(--color-success);
        font-weight: 500;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        background: var(--color-success);
        border-radius: var(--radius-full);
        animation: pulse 2s infinite;
    }

    /* ============================================
       LOADING SKELETON
       ============================================ */
    .skeleton {
        background: linear-gradient(
            90deg,
            var(--color-bg-secondary) 0%,
            var(--color-bg-tertiary) 50%,
            var(--color-bg-secondary) 100%
        );
        background-size: 200% 100%;
        animation: shimmer 1.5s ease-in-out infinite;
        border-radius: var(--radius-sm);
    }

    /* ============================================
       FOOTER
       ============================================ */
    .footer-text {
        text-align: center;
        color: var(--color-text-tertiary);
        padding: var(--space-2xl) var(--space-md);
        font-size: var(--text-caption);
        border-top: 1px solid var(--color-border-subtle);
        margin-top: var(--space-2xl);
    }

    .footer-text a {
        color: var(--color-accent-primary);
        text-decoration: none;
        transition: var(--transition-base);
    }

    .footer-text a:hover {
        color: var(--color-accent-hover);
    }

    /* ============================================
       FOCUS STATES (Accessibility)
       ============================================ */
    *:focus {
        outline: 2px solid var(--color-accent-primary);
        outline-offset: 2px;
    }

    button:focus:not(:focus-visible),
    a:focus:not(:focus-visible) {
        outline: none;
    }

    /* ============================================
       FIX: PHANTOM TEXT (Material Icons)
       The "keyb" and "keyboard_arrow_right" text appears
       when Material Symbols font fails to load
       ============================================ */
    /* Hide icon text when font renders correctly */
    [data-testid="stIconMaterial"],
    span[translate="no"][class*="st-emotion-cache"] {
        overflow: hidden;
        font-family: 'Material Symbols Rounded' !important;
    }

    /* Fallback: If font fails, hide the raw text */
    [data-testid="stExpander"] summary > span > span:first-child {
        font-family: 'Material Symbols Rounded' !important;
        font-size: 20px;
        width: 20px;
        height: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }

    /* Ensure sidebar radio items don't show phantom text */
    [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions

def live_indicator(timestamp_str=None):
    """Display a pulsing live indicator with optional timestamp."""
    if timestamp_str:
        return f'<div class="live-indicator"><span class="live-dot"></span>Live · {timestamp_str}</div>'
    return '<div class="live-indicator"><span class="live-dot"></span>Live</div>'


def render_live_indicator(timestamp_str=None):
    """Render a live indicator in the UI."""
    st.markdown(live_indicator(timestamp_str), unsafe_allow_html=True)


def auto_refresh_component(interval_seconds: int, key: str = "auto_refresh"):
    """
    Inject JavaScript to auto-refresh the page at specified intervals.
    Only active when auto-refresh is enabled.

    Args:
        interval_seconds: Time between page refreshes in seconds
        key: Unique key for the component
    """
    st.markdown(
        f"""
        <script>
            // Auto-refresh timer
            (function() {{
                const intervalMs = {interval_seconds * 1000};
                const key = '{key}';

                // Clear any existing timer
                if (window.autoRefreshTimer) {{
                    clearTimeout(window.autoRefreshTimer);
                }}

                // Set new timer
                window.autoRefreshTimer = setTimeout(function() {{
                    window.location.reload();
                }}, intervalMs);

                console.log('Auto-refresh scheduled in ' + {interval_seconds} + ' seconds');
            }})();
        </script>
        """,
        unsafe_allow_html=True
    )


def fetch_api(endpoint, silent=False):
    """Fetch data from API. Set silent=True to suppress error messages."""
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        if not silent:
            st.error(f"Error fetching data: {str(e)}")
        return None


# Common Plotly layout config - Design System v2.0
# Colors from DESIGN_SYSTEM.md
CHART_COLORS = [
    '#14b8a6',  # Teal - primary
    '#8b5cf6',  # Purple - secondary
    '#f59e0b',  # Amber - tertiary
    '#ec4899',  # Pink - quaternary
    '#06b6d4',  # Cyan - quinary
]

PLOTLY_LAYOUT_DEFAULTS = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family='Urbanist, -apple-system, BlinkMacSystemFont, sans-serif',
        color='#a3a3a3',  # --color-text-secondary
        size=12
    ),
    title_font=dict(
        size=16,
        color='#ffffff',  # --color-text-primary
        family='Urbanist, sans-serif'
    ),
    hovermode='x unified',
    hoverlabel=dict(
        bgcolor='#1e1e1e',  # --color-bg-tertiary
        bordercolor='#404040',  # --color-border-default
        font=dict(family='Urbanist, sans-serif', size=12, color='#ffffff')
    ),
    xaxis=dict(
        gridcolor='rgba(255, 255, 255, 0.05)',  # --color-chart-grid
        zerolinecolor='#404040',  # --color-border-default
        tickfont=dict(size=12, color='#737373'),  # --color-chart-axis
        linecolor='#262626',  # --color-border-subtle
        showgrid=True,
        gridwidth=1
    ),
    yaxis=dict(
        gridcolor='rgba(255, 255, 255, 0.05)',  # --color-chart-grid
        zerolinecolor='#404040',  # --color-border-default
        tickfont=dict(size=12, color='#737373'),  # --color-chart-axis
        linecolor='#262626',  # --color-border-subtle
        showgrid=True,
        gridwidth=1
    ),
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(
        font=dict(size=12, color='#a3a3a3'),
        bgcolor='rgba(0,0,0,0)',
        borderwidth=0
    )
)


def create_line_chart(data, title, y_label):
    """Create a line chart with Design System v2.0 styling"""
    df = pd.DataFrame(data['data'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['value'],
        mode='lines',
        name=data['name'],
        line=dict(color=CHART_COLORS[0], width=2),  # Teal primary
        fill='tozeroy',
        fillcolor='rgba(20, 184, 166, 0.1)'  # Teal with 10% opacity
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_label,
        height=400,
        **PLOTLY_LAYOUT_DEFAULTS
    )

    return fig


def get_indicator_delta(indicator_id, days=30):
    """Fetch historical data and calculate percentage change.
    Uses 90-day window to ensure we have data for monthly indicators."""
    try:
        end = datetime.now()
        # Use 90-day window to ensure we get data for monthly indicators
        start = end - timedelta(days=90)
        data = fetch_api(f"/api/indicators/{indicator_id}/timeseries?start={start.isoformat()}&limit=200", silent=True)
        if data and data.get('data') and len(data['data']) >= 2:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # Sort by timestamp to ensure correct order
            df = df.sort_values('timestamp')
            if len(df) >= 2:
                old_value = df.iloc[0]['value']
                new_value = df.iloc[-1]['value']
                if old_value != 0:
                    pct_change = ((new_value - old_value) / abs(old_value)) * 100
                    return round(pct_change, 2)
    except:
        pass
    return None


def create_metric_cards(indicators_data, show_delta=True):
    """Create metric cards for indicators with optional delta values"""
    cols = st.columns(len(indicators_data))

    for i, (indicator_id, info) in enumerate(indicators_data.items()):
        with cols[i]:
            value = info['latest_value']

            # Format value based on magnitude
            if abs(value) >= 1000:
                display_value = f"{value:,.0f}"
            elif abs(value) >= 10:
                display_value = f"{value:.1f}"
            else:
                display_value = f"{value:.2f}"

            # Get delta if requested
            delta = None
            delta_suffix = ""
            if show_delta:
                delta = get_indicator_delta(indicator_id)
                if delta is not None:
                    delta_suffix = f"{delta:+.1f}%"

            st.metric(
                label=info['name'],
                value=display_value,
                delta=delta_suffix if delta_suffix else None,
                help=f"Unit: {info.get('unit', 'N/A')}\nLast updated: {info['timestamp'][:10]}\n30-day change shown"
            )


def calculate_change(df, days=30):
    """Calculate percentage change over period"""
    if len(df) < 2:
        return 0
    
    recent = df.tail(days)
    if len(recent) < 2:
        return 0
    
    old_value = recent.iloc[0]['value']
    new_value = recent.iloc[-1]['value']
    
    if old_value == 0:
        return 0
    
    return ((new_value - old_value) / old_value) * 100


def check_recession_signals():
    """Check for key recession warning signals (uses silent mode to avoid error spam)"""
    warnings = []

    # Helper to safely get numeric value
    def safe_value(data, default=0):
        if data and data.get('latest_value') is not None:
            return data['latest_value']
        return default

    # Check yield curve
    yield_data = fetch_api("/api/indicators/T10Y2Y/latest", silent=True)
    if safe_value(yield_data) < 0:
        warnings.append(("Yield Curve Inverted", "The 10Y-2Y spread is negative - historically precedes recessions by 6-18 months"))

    # Check VIX (try FRED version first, then Yahoo)
    vix_data = fetch_api("/api/indicators/VIXCLS/latest", silent=True)
    if not vix_data:
        vix_data = fetch_api("/api/indicators/^VIX/latest", silent=True)
    vix_val = safe_value(vix_data)
    if vix_val > 30:
        warnings.append(("High Volatility", f"VIX is {vix_val:.1f} - elevated market fear"))

    # Check unemployment trend
    unemp_data = fetch_api("/api/indicators/UNRATE/latest", silent=True)
    unemp_val = safe_value(unemp_data)
    if unemp_val > 5:
        warnings.append(("Elevated Unemployment", f"Unemployment at {unemp_val:.1f}% - above historical average"))

    # Check high yield spread (credit stress)
    hy_data = fetch_api("/api/indicators/BAMLH0A0HYM2/latest", silent=True)
    hy_val = safe_value(hy_data)
    if hy_val > 5:
        warnings.append(("Credit Stress", f"High yield spread at {hy_val:.2f}% - elevated credit risk"))

    return warnings


def display_warning_banners():
    """Display warning banners for recession signals"""
    warnings = check_recession_signals()
    if warnings:
        st.markdown("### Warning Signals")
        for title, description in warnings:
            st.warning(f"**{title}**: {description}")
        st.divider()


# Main App
st.title("Macro Dashboard")
st.markdown("Track key economic and market indicators in real-time")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Overview", "Sector Performance", "Yield Curve", "Liquidity", "Market Regime",
     "Inflation Monitor", "Recession Watch", "Market Overview", "Credit Spreads",
     "Currency Monitor", "Commodities", "Global Markets", "Sentiment", "Custom Analysis", "FAQ"]
)

# Refresh button in sidebar
st.sidebar.divider()
st.sidebar.subheader("Data Management")

# Initialize session state for auto-refresh
if 'auto_refresh_enabled' not in st.session_state:
    st.session_state.auto_refresh_enabled = False
if 'last_fred_refresh' not in st.session_state:
    st.session_state.last_fred_refresh = None
if 'last_market_refresh' not in st.session_state:
    st.session_state.last_market_refresh = None

# Manual refresh buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("⟳ FRED", use_container_width=True, help="Refresh FRED economic data"):
        with st.spinner("Refreshing FRED..."):
            try:
                response = requests.post(f"{API_BASE}/api/refresh?source=fred", timeout=300)
                if response.status_code == 200:
                    st.session_state.last_fred_refresh = datetime.now()
                    st.sidebar.success("FRED refreshed!")
                    st.rerun()
                else:
                    st.sidebar.error("Refresh failed")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")

with col2:
    if st.button("⟳ Market", use_container_width=True, help="Refresh market price data"):
        with st.spinner("Refreshing Market..."):
            try:
                response = requests.post(f"{API_BASE}/api/refresh?source=market", timeout=300)
                if response.status_code == 200:
                    st.session_state.last_market_refresh = datetime.now()
                    st.sidebar.success("Market refreshed!")
                    st.rerun()
                else:
                    st.sidebar.error("Refresh failed")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")

# Auto-refresh settings
st.sidebar.divider()
st.sidebar.subheader("Auto-Refresh")

auto_refresh = st.sidebar.toggle("Enable Auto-Refresh", value=st.session_state.auto_refresh_enabled, key="auto_refresh_toggle")
st.session_state.auto_refresh_enabled = auto_refresh

if auto_refresh:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        fred_interval = st.selectbox(
            "FRED Interval",
            options=[15, 30, 60, 120],
            index=2,
            format_func=lambda x: f"{x} min",
            key="fred_interval",
            help="FRED data updates infrequently (daily/weekly/monthly)"
        )
    with col2:
        market_interval = st.selectbox(
            "Market Interval",
            options=[5, 10, 15, 30, 60],
            index=2,
            format_func=lambda x: f"{x} min",
            key="market_interval",
            help="Market data can update more frequently"
        )

    # Check if refresh is needed
    now = datetime.now()

    # FRED auto-refresh check
    fred_needs_refresh = False
    if st.session_state.last_fred_refresh is None:
        fred_needs_refresh = True
    else:
        fred_elapsed = (now - st.session_state.last_fred_refresh).total_seconds() / 60
        if fred_elapsed >= fred_interval:
            fred_needs_refresh = True

    # Market auto-refresh check
    market_needs_refresh = False
    if st.session_state.last_market_refresh is None:
        market_needs_refresh = True
    else:
        market_elapsed = (now - st.session_state.last_market_refresh).total_seconds() / 60
        if market_elapsed >= market_interval:
            market_needs_refresh = True

    # Perform auto-refresh if needed
    if fred_needs_refresh or market_needs_refresh:
        refresh_status = st.sidebar.empty()

        if fred_needs_refresh:
            refresh_status.info("Auto-refreshing FRED data...")
            try:
                response = requests.post(f"{API_BASE}/api/refresh?source=fred", timeout=300)
                if response.status_code == 200:
                    st.session_state.last_fred_refresh = now
            except:
                pass

        if market_needs_refresh:
            refresh_status.info("Auto-refreshing Market data...")
            try:
                response = requests.post(f"{API_BASE}/api/refresh?source=market", timeout=300)
                if response.status_code == 200:
                    st.session_state.last_market_refresh = now
            except:
                pass

        refresh_status.empty()
        if fred_needs_refresh or market_needs_refresh:
            st.rerun()

    # Display next refresh countdown
    st.sidebar.caption("**Next refresh:**")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.session_state.last_fred_refresh:
            fred_next = fred_interval - int((now - st.session_state.last_fred_refresh).total_seconds() / 60)
            fred_next = max(0, fred_next)
            st.caption(f"FRED: {fred_next} min")
        else:
            st.caption("FRED: Now")

    with col2:
        if st.session_state.last_market_refresh:
            market_next = market_interval - int((now - st.session_state.last_market_refresh).total_seconds() / 60)
            market_next = max(0, market_next)
            st.caption(f"Market: {market_next} min")
        else:
            st.caption("Market: Now")

    # Calculate the minimum refresh interval and trigger page refresh
    min_interval = min(fred_interval, market_interval)
    auto_refresh_component(min_interval * 60, key="dashboard_auto_refresh")
    st.sidebar.caption(f"_Page refreshes every {min_interval} min_")

# Live data indicator in sidebar
st.sidebar.divider()
last_update = datetime.now().strftime("%H:%M")
st.sidebar.markdown(live_indicator(last_update), unsafe_allow_html=True)

# Show last refresh times if available
if st.session_state.last_fred_refresh or st.session_state.last_market_refresh:
    refresh_info = []
    if st.session_state.last_fred_refresh:
        refresh_info.append(f"FRED: {st.session_state.last_fred_refresh.strftime('%H:%M')}")
    if st.session_state.last_market_refresh:
        refresh_info.append(f"Market: {st.session_state.last_market_refresh.strftime('%H:%M')}")
    st.sidebar.caption(f"Last refresh: {' | '.join(refresh_info)}")

# Page: Overview
if page == "Overview":
    st.header("Dashboard Overview")

    # Comprehensive introduction
    st.markdown("""
    ### Your Command Center for Macro-Economic Analysis

    This dashboard aggregates the most important economic and market indicators that professional investors, portfolio managers,
    and economists monitor to understand where the economy and markets are heading. The data comes from two primary sources:
    the **Federal Reserve Economic Data (FRED)** maintained by the St. Louis Fed (the gold standard for economic statistics),
    and **Yahoo Finance** for real-time market prices. Together, these give you a comprehensive view spanning decades of
    historical data updated to the present.

    **How to use this overview page:** This page provides a quick pulse-check across all major categories. The **Key Economic
    Indicators** section shows recession-watch metrics - if the yield spread turns negative or unemployment starts rising,
    those are warning signs. The **Key Market Indicators** show where major asset classes are trading today. The **trailing
    1-year chart** below normalizes different assets (stocks, crypto) to percentage returns so you can compare performance
    on equal footing - which asset classes are leading, which are lagging? Use the warning banners at the top as alerts:
    they'll highlight critical conditions like an inverted yield curve or elevated volatility that warrant your attention.

    **Navigating deeper:** Use the sidebar to explore specialized dashboards. **Sector Performance** shows the famous annual
    returns heatmap to understand sector rotation. **Yield Curve** visualizes interest rates across maturities - the shape
    tells you about growth expectations. **Liquidity** tracks Fed balance sheet dynamics that drive asset prices. **Market
    Regime** shows which investment styles (growth vs value, large vs small) are winning. **Inflation Monitor** breaks down
    where price pressures are coming from. **Recession Watch** consolidates leading indicators. **Market Overview** provides
    detailed charts for stocks and crypto. Each dashboard includes comprehensive explanations to help you interpret the data.
    """)

    # Warning banners at top
    display_warning_banners()

    # Health check
    health = fetch_api("/health")
    if health:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", "✅ Healthy" if health['status'] == 'healthy' else "❌ Unhealthy")
        with col2:
            st.metric("Database", health.get('database', 'N/A'))
        with col3:
            st.metric("Total Indicators", health.get('total_indicators', 0))

    st.divider()

    # Key metrics from both dashboards
    st.subheader("Key Economic Indicators")
    st.caption("**Yield Spread**: Difference between 10Y and 2Y Treasury rates (negative = inverted, recession signal). "
               "**Unemployment**: % of labor force without jobs. **Industrial Production**: Index where 100 = 2017 output levels. "
               "**Housing Starts**: New residential construction in thousands of units/year. **Consumer Sentiment**: Survey index (100 = 1966 baseline).")
    recession_data = fetch_api("/api/dashboards/recession-watch")
    if recession_data:
        create_metric_cards(recession_data['indicators'])

    st.divider()

    st.subheader("Key Market Indicators")
    st.caption("Current prices for major indices and assets. Delta shows 30-day percentage change.")
    market_data = fetch_api("/api/dashboards/market-overview")
    if market_data:
        create_metric_cards(market_data['indicators'])

    st.divider()

    # Trailing 1-Year Major Assets Comparison
    st.subheader("Major Assets - Trailing 1 Year")
    start_date = datetime.now() - timedelta(days=365)

    # Fetch multiple assets
    assets = [
        ("^GSPC", "S&P 500", "#14b8a6"),
        ("^IXIC", "Nasdaq", "#8b5cf6"),
        ("^DJI", "Dow Jones", "#F6AD55"),
        ("BTC-USD", "Bitcoin", "#B794F4")
    ]

    fig = go.Figure()
    for symbol, name, color in assets:
        data = fetch_api(f"/api/indicators/{symbol}/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if data and data.get('data') and len(data['data']) > 1:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            # Normalize to percentage change from start
            start_val = df.iloc[0]['value']
            df['pct'] = ((df['value'] - start_val) / start_val) * 100

            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['pct'],
                mode='lines',
                name=name,
                line=dict(color=color, width=2)
            ))

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Return (%)",
        template='plotly_dark',
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#2D3748'),
        yaxis=dict(gridcolor='#2D3748'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("Chart shows normalized returns (% change from 1 year ago) to compare assets on equal footing.")

# Page: Sector Performance (Novel Investor style heatmap)
elif page == "Sector Performance":
    st.header("📊 S&P 500 Sector Performance")

    # Comprehensive explanation
    st.markdown("""
    ### Understanding Sector Rotation

    The S&P 500 is divided into 11 sectors, each representing a different segment of the economy. **Sector rotation**
    is one of the most powerful concepts in investing - the observation that different sectors lead the market at
    different points in the economic cycle. During economic expansions, cyclical sectors like Technology, Consumer
    Discretionary, and Industrials tend to outperform as businesses invest and consumers spend freely. During
    contractions or uncertainty, defensive sectors like Utilities, Consumer Staples, and Health Care often hold up
    better because people still need electricity, groceries, and medical care regardless of the economy.

    **How to read the heatmap below:** Each cell shows the total annual return for that sector index in that calendar
    year. Bright green indicates strong positive returns (often 20%+), while red indicates losses. The key insight
    is the **lack of persistence** - notice how the leading sector changes almost every year. Energy dominated in
    2021-2022 during the post-COVID commodity surge, but was the worst performer in 2020 and 2015. Technology led
    during 2017-2020's digital transformation boom but suffered in 2022's rate-hike environment.

    *Data source: S&P 500 Sector Indices (back to 1993 for most sectors). Energy uses XLE ETF data (back to 1998)
    as the index data is not available. Real Estate index begins in 2001 when it was split from Financials.*
    """)

    # S&P 500 Sector Indices - using actual index data for longer history
    # Format: (symbol, display_name)
    sectors_config = [
        ("^SP500-45", "Technology"),
        ("^SP500-40", "Financials"),
        ("XLE", "Energy"),  # Use ETF - index not available on Yahoo
        ("^SP500-35", "Health Care"),
        ("^SP500-25", "Cons. Disc."),
        ("^SP500-30", "Cons. Staples"),
        ("^SP500-20", "Industrials"),
        ("^SP500-15", "Materials"),
        ("^SP500-55", "Utilities"),
        ("^SP500-60", "Real Estate"),
        ("^SP500-50", "Comm. Svcs"),
    ]

    current_year = datetime.now().year

    # Time range selector
    st.subheader("Historical Returns Heatmap")
    col1, col2 = st.columns([1, 3])
    with col1:
        time_range = st.selectbox(
            "Time Range",
            ["5 Years", "10 Years", "20 Years", "Full History"],
            index=2,
            key="sector_time_range"
        )

    # Determine years to show based on selection
    if time_range == "5 Years":
        num_years = 5
    elif time_range == "10 Years":
        num_years = 10
    elif time_range == "20 Years":
        num_years = 20
    else:  # Full History
        num_years = 35  # Back to 1990

    years = list(range(current_year - num_years, current_year + 1))
    history_start = datetime(current_year - 40, 1, 1).isoformat()

    # Build returns matrix
    returns_data = []
    for symbol, name in sectors_config:
        row = {"Sector": name}

        # Fetch data
        data = fetch_api(f"/api/indicators/{symbol}/timeseries?start={history_start}&limit=20000", silent=True)
        if data and data.get('data'):
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['year'] = df['timestamp'].dt.year
            df = df.sort_values('timestamp')

            for year in years:
                year_data = df[df['year'] == year]
                if len(year_data) >= 2:
                    start_val = year_data.iloc[0]['value']
                    end_val = year_data.iloc[-1]['value']
                    if start_val > 0:
                        pct_return = ((end_val - start_val) / start_val) * 100
                        row[str(year)] = round(pct_return, 1)
                    else:
                        row[str(year)] = None
                else:
                    row[str(year)] = None
        else:
            for year in years:
                row[str(year)] = None

        returns_data.append(row)

    returns_df = pd.DataFrame(returns_data)

    if len(returns_df) > 0:
        # Create heatmap
        year_cols = [str(y) for y in years if str(y) in returns_df.columns]
        heatmap_data = returns_df[year_cols].values.T

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=returns_df['Sector'].tolist(),
            y=year_cols,
            colorscale=[
                [0, '#ef4444'],      # Red for negative
                [0.5, '#1A1F2E'],    # Dark for zero
                [1, '#10b981']       # Green for positive
            ],
            zmid=0,
            text=[[f"{v:.1f}%" if pd.notna(v) else "" for v in row] for row in heatmap_data],
            texttemplate="%{text}",
            textfont={"size": 10, "color": "white"},
            hoverongaps=False,
            colorbar=dict(title="Return %")
        ))

        # Dynamic height based on years shown
        chart_height = max(400, min(800, len(year_cols) * 22))
        fig.update_layout(
            title=f"Annual Sector Returns (%) - {time_range}",
            xaxis_title="Sector",
            yaxis_title="Year",
            template='plotly_dark',
            height=chart_height,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Weighted Average Returns
        st.subheader("Average Annual Returns by Sector")
        st.caption(f"Simple and annualized returns over the selected {time_range.lower()} period")

        avg_data = []
        for _, row in returns_df.iterrows():
            sector_name = row['Sector']
            returns = [row[col] for col in year_cols if pd.notna(row[col])]
            if returns:
                simple_avg = np.mean(returns)
                # Calculate geometric mean (CAGR approximation)
                # Convert percentage returns to growth factors, multiply, then annualize
                growth_factors = [(1 + r/100) for r in returns]
                cumulative = np.prod(growth_factors)
                n_years = len(returns)
                cagr = (cumulative ** (1/n_years) - 1) * 100 if n_years > 0 else 0
                avg_data.append({
                    "Sector": sector_name,
                    "Simple Avg": simple_avg,
                    "CAGR": cagr,
                    "Years": n_years,
                    "Best Year": max(returns),
                    "Worst Year": min(returns)
                })

        if avg_data:
            avg_df = pd.DataFrame(avg_data).sort_values("CAGR", ascending=False)

            col1, col2 = st.columns(2)

            with col1:
                # CAGR bar chart
                colors = ['#10b981' if v >= 0 else '#ef4444' for v in avg_df['CAGR']]
                fig_cagr = go.Figure(go.Bar(
                    x=avg_df['CAGR'],
                    y=avg_df['Sector'],
                    orientation='h',
                    marker_color=colors,
                    text=[f"{v:.1f}%" for v in avg_df['CAGR']],
                    textposition='outside'
                ))
                fig_cagr.update_layout(
                    title=f"Compound Annual Growth Rate ({time_range})",
                    xaxis_title="CAGR (%)",
                    yaxis_title="",
                    template='plotly_dark',
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(gridcolor='#2D3748')
                )
                st.plotly_chart(fig_cagr, use_container_width=True)

            with col2:
                # Stats table
                st.markdown("**Return Statistics**")
                display_df = avg_df[['Sector', 'CAGR', 'Simple Avg', 'Best Year', 'Worst Year', 'Years']].copy()
                display_df.columns = ['Sector', 'CAGR %', 'Avg %', 'Best %', 'Worst %', 'Yrs']
                for col in ['CAGR %', 'Avg %', 'Best %', 'Worst %']:
                    display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}")
                st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.divider()

        # YTD performance bar chart
        st.subheader("Year-to-Date Performance")
        ytd_data = []
        start_of_year = datetime(current_year, 1, 1)
        for symbol, name in sectors_config:
            data = fetch_api(f"/api/indicators/{symbol}/timeseries?start={start_of_year.isoformat()}&limit=500", silent=True)
            if data and data.get('data') and len(data['data']) >= 2:
                df = pd.DataFrame(data['data'])
                start_val = df.iloc[0]['value']
                end_val = df.iloc[-1]['value']
                if start_val > 0:
                    ytd_return = ((end_val - start_val) / start_val) * 100
                    ytd_data.append({"Sector": name, "YTD Return": ytd_return})

        if ytd_data:
            ytd_df = pd.DataFrame(ytd_data).sort_values("YTD Return", ascending=True)
            colors = ['#10b981' if v >= 0 else '#ef4444' for v in ytd_df['YTD Return']]

            fig = go.Figure(go.Bar(
                x=ytd_df['YTD Return'],
                y=ytd_df['Sector'],
                orientation='h',
                marker_color=colors,
                text=[f"{v:.1f}%" for v in ytd_df['YTD Return']],
                textposition='outside'
            ))

            fig.update_layout(
                title=f"{current_year} YTD Sector Returns",
                xaxis_title="Return (%)",
                yaxis_title="",
                template='plotly_dark',
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='#2D3748')
            )

            st.plotly_chart(fig, use_container_width=True)

    # Sector Descriptions
    st.divider()
    st.subheader("Sector Guide")
    st.markdown("Understanding each sector's role in the economy and its major constituents.")

    col1, col2 = st.columns(2)

    with col1:
        with st.expander("**Technology (XLK)**", expanded=False):
            st.markdown("""
            **What It Covers:** Software, hardware, semiconductors, IT services, and electronic equipment companies.

            **Economic Role:** The growth engine of the modern economy. Technology drives productivity gains, digital transformation, and innovation across all other sectors. Highly sensitive to interest rates due to long-duration cash flows.

            **Cyclical Nature:** Growth-oriented and cyclical. Outperforms during economic expansions and low-rate environments. Vulnerable during rate hikes and risk-off periods.

            **Major Holdings:**
            - **Apple (AAPL)** - Consumer electronics, services ecosystem
            - **Microsoft (MSFT)** - Enterprise software, cloud (Azure)
            - **Nvidia (NVDA)** - GPUs, AI chips
            - **Broadcom (AVGO)** - Semiconductors, infrastructure software
            - **Salesforce (CRM)** - Cloud-based CRM software

            **Weight in S&P 500:** ~30% (largest sector)
            """)

        with st.expander("**Financials (XLF)**", expanded=False):
            st.markdown("""
            **What It Covers:** Banks, insurance companies, asset managers, credit card companies, and financial exchanges.

            **Economic Role:** The circulatory system of the economy. Financials facilitate capital allocation, risk transfer, and payment systems. Their health reflects credit conditions and economic confidence.

            **Cyclical Nature:** Highly cyclical and interest-rate sensitive. Banks benefit from higher rates (wider net interest margins). Vulnerable during recessions when loan defaults rise.

            **Major Holdings:**
            - **Berkshire Hathaway (BRK.B)** - Diversified conglomerate, insurance
            - **JPMorgan Chase (JPM)** - Largest U.S. bank
            - **Visa (V)** - Payment network
            - **Mastercard (MA)** - Payment network
            - **Bank of America (BAC)** - Major commercial bank

            **Weight in S&P 500:** ~13%
            """)

        with st.expander("**Health Care (XLV)**", expanded=False):
            st.markdown("""
            **What It Covers:** Pharmaceuticals, biotechnology, medical devices, health insurance, hospitals, and healthcare services.

            **Economic Role:** Essential services with relatively inelastic demand. Healthcare spending continues regardless of economic conditions, making this a defensive sector with growth characteristics from aging demographics.

            **Cyclical Nature:** Defensive with growth potential. Less volatile than the market. Subject to regulatory/political risk around drug pricing and healthcare policy.

            **Major Holdings:**
            - **UnitedHealth Group (UNH)** - Health insurance, services
            - **Eli Lilly (LLY)** - Pharmaceuticals (diabetes, obesity drugs)
            - **Johnson & Johnson (JNJ)** - Diversified pharma, devices, consumer
            - **AbbVie (ABBV)** - Biopharmaceuticals
            - **Merck (MRK)** - Pharmaceuticals

            **Weight in S&P 500:** ~12%
            """)

        with st.expander("**Consumer Discretionary (XLY)**", expanded=False):
            st.markdown("""
            **What It Covers:** Retail, automobiles, hotels, restaurants, leisure, apparel, and consumer services - things people buy when they have extra money.

            **Economic Role:** A direct read on consumer confidence and spending power. When consumers feel wealthy and secure, discretionary spending rises. When worried, it's the first to get cut.

            **Cyclical Nature:** Highly cyclical. One of the first sectors to decline entering recession and first to recover coming out. Very sensitive to employment and wage growth.

            **Major Holdings:**
            - **Amazon (AMZN)** - E-commerce, cloud (AWS)
            - **Tesla (TSLA)** - Electric vehicles
            - **Home Depot (HD)** - Home improvement retail
            - **McDonald's (MCD)** - Quick service restaurants
            - **Nike (NKE)** - Athletic apparel and footwear

            **Weight in S&P 500:** ~10%
            """)

        with st.expander("**Industrials (XLI)**", expanded=False):
            st.markdown("""
            **What It Covers:** Aerospace & defense, machinery, construction, transportation (airlines, railroads, trucking), and professional services.

            **Economic Role:** The backbone of physical economic activity. Industrials build infrastructure, move goods, and manufacture equipment. Closely tied to business investment and global trade.

            **Cyclical Nature:** Cyclical, tracking manufacturing activity and capital expenditure cycles. Benefits from infrastructure spending and reshoring trends. Vulnerable to trade wars and economic slowdowns.

            **Major Holdings:**
            - **GE Aerospace (GE)** - Aircraft engines, aerospace
            - **Caterpillar (CAT)** - Construction & mining equipment
            - **RTX Corporation (RTX)** - Aerospace, defense
            - **Union Pacific (UNP)** - Railroad transportation
            - **Honeywell (HON)** - Diversified industrial conglomerate

            **Weight in S&P 500:** ~9%
            """)

        with st.expander("**Energy (XLE)**", expanded=False):
            st.markdown("""
            **What It Covers:** Oil & gas exploration/production, refining, pipelines, and energy equipment/services.

            **Economic Role:** Provides the fuel that powers the economy. Energy prices affect transportation costs, manufacturing inputs, and consumer spending (gasoline). Geopolitically sensitive.

            **Cyclical Nature:** Highly cyclical and commodity-driven. Performance tied to oil/gas prices, which are influenced by OPEC, geopolitics, and global demand. Can move independently of broader market.

            **Major Holdings:**
            - **ExxonMobil (XOM)** - Integrated oil & gas major
            - **Chevron (CVX)** - Integrated oil & gas major
            - **ConocoPhillips (COP)** - Oil & gas exploration/production
            - **Schlumberger (SLB)** - Oilfield services
            - **EOG Resources (EOG)** - Shale oil producer

            **Weight in S&P 500:** ~4%
            """)

    with col2:
        with st.expander("**Consumer Staples (XLP)**", expanded=False):
            st.markdown("""
            **What It Covers:** Food, beverages, tobacco, household products, and personal care - everyday necessities that people buy regardless of economic conditions.

            **Economic Role:** Provides essential goods with stable demand. People need to eat, clean, and maintain hygiene in any economy. This stability makes staples a classic defensive sector.

            **Cyclical Nature:** Defensive. Outperforms during recessions and market stress as investors seek stability. Underperforms during strong bull markets when investors chase growth.

            **Major Holdings:**
            - **Procter & Gamble (PG)** - Household products
            - **Costco (COST)** - Warehouse retail
            - **Coca-Cola (KO)** - Beverages
            - **PepsiCo (PEP)** - Beverages, snacks
            - **Walmart (WMT)** - Discount retail

            **Weight in S&P 500:** ~6%
            """)

        with st.expander("**Utilities (XLU)**", expanded=False):
            st.markdown("""
            **What It Covers:** Electric utilities, gas utilities, water utilities, and independent power producers.

            **Economic Role:** Provides essential services (electricity, gas, water) with regulated, predictable revenue streams. High dividend yields make utilities bond-like investments.

            **Cyclical Nature:** Most defensive sector. Regulated monopolies with stable cash flows. Acts as a bond proxy - rises when rates fall, falls when rates rise. Minimal correlation to economic growth.

            **Major Holdings:**
            - **NextEra Energy (NEE)** - Largest U.S. utility, renewable focus
            - **Southern Company (SO)** - Electric utility
            - **Duke Energy (DUK)** - Electric utility
            - **Constellation Energy (CEG)** - Nuclear power, clean energy
            - **American Electric Power (AEP)** - Electric utility

            **Weight in S&P 500:** ~2%
            """)

        with st.expander("**Materials (XLB)**", expanded=False):
            st.markdown("""
            **What It Covers:** Chemicals, construction materials, metals & mining, paper & packaging, and containers.

            **Economic Role:** Provides raw materials for manufacturing and construction. Commodity-sensitive sector tied to global industrial activity and infrastructure investment.

            **Cyclical Nature:** Cyclical, tied to manufacturing activity and commodity prices. Benefits from infrastructure spending and emerging market growth. Vulnerable to overcapacity and trade issues.

            **Major Holdings:**
            - **Linde (LIN)** - Industrial gases
            - **Sherwin-Williams (SHW)** - Paints and coatings
            - **Freeport-McMoRan (FCX)** - Copper mining
            - **Newmont (NEM)** - Gold mining
            - **Air Products (APD)** - Industrial gases

            **Weight in S&P 500:** ~2%
            """)

        with st.expander("**Real Estate (XLRE)**", expanded=False):
            st.markdown("""
            **What It Covers:** Real Estate Investment Trusts (REITs) owning office, retail, residential, industrial, healthcare, and data center properties.

            **Economic Role:** Provides exposure to commercial real estate without direct property ownership. REITs must distribute 90% of taxable income as dividends, making them income-oriented investments.

            **Cyclical Nature:** Interest rate sensitive (like utilities). Rising rates hurt REIT valuations as their dividend yields become less attractive relative to bonds. Property-type specific risks (e.g., retail vs. industrial).

            **Major Holdings:**
            - **Prologis (PLD)** - Industrial/logistics warehouses
            - **American Tower (AMT)** - Cell towers
            - **Equinix (EQIX)** - Data centers
            - **Crown Castle (CCI)** - Cell towers
            - **Public Storage (PSA)** - Self-storage facilities

            **Weight in S&P 500:** ~2%

            *Note: Before 2015, Real Estate was part of Financials. Historical data uses VNQ (Vanguard Real Estate ETF) as proxy.*
            """)

        with st.expander("**Communication Services (XLC)**", expanded=False):
            st.markdown("""
            **What It Covers:** Telecom providers, media companies, entertainment, interactive media, and social networking platforms.

            **Economic Role:** Enables communication and content distribution. Combines stable telecom utilities with high-growth digital media. Sector was reorganized in 2018 to include internet companies previously in Technology.

            **Cyclical Nature:** Mixed - legacy telecom is defensive while digital media/advertising is cyclical. Social media and streaming are sensitive to advertising budgets and consumer discretionary spending.

            **Major Holdings:**
            - **Meta Platforms (META)** - Social media (Facebook, Instagram)
            - **Alphabet (GOOGL)** - Search, YouTube, cloud
            - **Netflix (NFLX)** - Streaming video
            - **Walt Disney (DIS)** - Entertainment, theme parks, streaming
            - **Comcast (CMCSA)** - Cable, NBCUniversal

            **Weight in S&P 500:** ~9%

            *Note: Sector was reorganized in 2018. Historical data uses IYZ (iShares Telecom ETF) as proxy, which tracked the old, narrower Telecom sector.*
            """)

# Page: Yield Curve
elif page == "Yield Curve":
    st.header("📈 Treasury Yield Curve")

    # Comprehensive explanation
    st.markdown("""
    ### What Is the Yield Curve and Why Does It Matter?

    The yield curve is a graph showing interest rates (yields) on U.S. Treasury bonds across different time horizons,
    from 1-month bills to 30-year bonds. It's one of the most closely watched indicators in finance because it reflects
    the collective expectations of millions of bond market participants about future economic growth, inflation, and
    Federal Reserve policy. In a healthy, growing economy, the curve slopes upward - investors demand higher yields to
    lock up their money for longer periods, compensating for inflation risk and opportunity cost. A 10-year bond should
    pay more than a 2-year bond, which should pay more than a 3-month bill. This "term premium" is the normal state of
    affairs and reflects optimism about future growth.

    **The dreaded inversion:** When short-term rates rise above long-term rates, the curve "inverts" - and this is
    where things get interesting. An inverted yield curve has preceded every U.S. recession since 1955, typically
    6-24 months before the downturn begins. Why does this happen? When investors expect a recession, they anticipate
    the Fed will eventually cut rates to stimulate the economy. They rush to lock in today's higher long-term rates
    before they fall, driving long-term yields down. Meanwhile, if the Fed is currently raising short-term rates to
    fight inflation (as in 2022-2023), short-term yields stay elevated. The result: short rates exceed long rates.
    The most-watched spread is the 10-year minus 2-year (10Y-2Y). When this goes negative, recession warning bells ring.
    The 10Y-3M spread is also significant - some economists consider it even more predictive.

    **How to interpret the chart below:** The current yield curve shows today's rates across all maturities. An upward
    slope (left to right) is healthy. A flat curve suggests uncertainty - the market isn't sure which way the economy
    is headed. An inverted curve (downward slope, especially in the 2Y-10Y range) is a warning sign. The historical
    10Y-2Y spread chart shows this relationship over time - when the line dips below zero (the red zone), the curve
    is inverted. Notice how inversions in 2000, 2006-2007, and 2019 preceded recessions. The 2022-2023 inversion was
    one of the deepest and longest in modern history, though the predicted recession has been slower to materialize
    than historical patterns suggested, leading to debate about whether "this time is different" or the lag is simply
    longer. The curve's shape also affects banks' profitability (they borrow short and lend long), mortgage rates,
    and corporate borrowing costs throughout the economy.
    """)

    # Yield curve maturities (in order)
    maturities = [
        ("DGS1MO", "1M", 1/12),
        ("DGS3MO", "3M", 0.25),
        ("DGS6MO", "6M", 0.5),
        ("DGS1", "1Y", 1),
        ("DGS2", "2Y", 2),
        ("DGS5", "5Y", 5),
        ("DGS7", "7Y", 7),
        ("DGS10", "10Y", 10),
        ("DGS20", "20Y", 20),
        ("DGS30", "30Y", 30)
    ]

    # Get latest yields
    current_yields = []
    for series_id, label, years in maturities:
        data = fetch_api(f"/api/indicators/{series_id}/latest", silent=True)
        if data and data.get('latest_value') is not None:
            current_yields.append({
                "label": label,
                "years": years,
                "yield": data['latest_value']
            })

    if current_yields:
        # Current yield curve
        st.subheader("Current Yield Curve")
        yield_df = pd.DataFrame(current_yields)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yield_df['label'],
            y=yield_df['yield'],
            mode='lines+markers',
            name='Current Curve',
            line=dict(color='#14b8a6', width=3),
            marker=dict(size=12),
            text=[f"{y:.2f}%" for y in yield_df['yield']],
            textposition='top center',
            textfont=dict(size=11, color='#E2E8F0')
        ))

        fig.update_layout(
            xaxis_title="Maturity",
            yaxis_title="Yield (%)",
            template='plotly_dark',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748', categoryorder='array',
                      categoryarray=['1M', '3M', '6M', '1Y', '2Y', '5Y', '7Y', '10Y', '20Y', '30Y']),
            yaxis=dict(gridcolor='#2D3748')
        )

        st.plotly_chart(fig, use_container_width=True)

        # Key spread metrics
        col1, col2, col3, col4 = st.columns(4)

        spread_10y2y = fetch_api("/api/indicators/T10Y2Y/latest", silent=True)
        if spread_10y2y and spread_10y2y.get('latest_value') is not None:
            val = spread_10y2y['latest_value']
            with col1:
                st.metric("10Y-2Y Spread", f"{val:.2f}%",
                         delta="Inverted" if val < 0 else "Normal",
                         delta_color="inverse" if val < 0 else "normal")

        # Calculate other spreads from current yields
        yields_dict = {row['label']: row['yield'] for _, row in yield_df.iterrows()}

        if '10Y' in yields_dict and '3M' in yields_dict:
            spread_10y3m = yields_dict['10Y'] - yields_dict['3M']
            with col2:
                st.metric("10Y-3M Spread", f"{spread_10y3m:.2f}%",
                         delta="Inverted" if spread_10y3m < 0 else "Normal",
                         delta_color="inverse" if spread_10y3m < 0 else "normal")

        if '30Y' in yields_dict and '5Y' in yields_dict:
            spread_30y5y = yields_dict['30Y'] - yields_dict['5Y']
            with col3:
                st.metric("30Y-5Y Spread", f"{spread_30y5y:.2f}%")

        if '2Y' in yields_dict:
            with col4:
                st.metric("2Y Yield", f"{yields_dict['2Y']:.2f}%")

    st.divider()

    # Historical 10Y-2Y spread
    st.subheader("10Y-2Y Spread History")
    time_range = st.selectbox("Time Range", ["1 Year", "5 Years", "10 Years", "Max"], index=1, key="yc_range")
    days_map = {"1 Year": 365, "5 Years": 1825, "10 Years": 3650, "Max": 20000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    spread_data = fetch_api(f"/api/indicators/T10Y2Y/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    if spread_data and spread_data.get('data'):
        df = pd.DataFrame(spread_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['value'],
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)',
            line=dict(color='#ef4444', width=2)
        ))
        fig.add_hline(y=0, line_dash="dash", line_color="#E2E8F0", annotation_text="Inversion Line")

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Spread (%)",
            template='plotly_dark',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'),
            yaxis=dict(gridcolor='#2D3748')
        )

        st.plotly_chart(fig, use_container_width=True)

# Page: Liquidity
elif page == "Liquidity":
    st.header("💧 Liquidity Dashboard")

    # Comprehensive explanation
    st.markdown("""
    ### Understanding Liquidity: The Lifeblood of Financial Markets

    Liquidity refers to the amount of money sloshing around the financial system, available to buy assets, fund loans,
    and facilitate economic activity. Many market analysts argue that liquidity conditions are the single most important
    driver of asset prices in the modern era - more important than earnings, GDP growth, or even inflation. The basic
    logic is simple: when there's abundant money seeking returns, it flows into stocks, bonds, real estate, and crypto,
    pushing prices up. When liquidity drains, asset prices fall. This explains why markets surged during 2020-2021 when
    the Fed injected trillions, and struggled in 2022 when that process reversed. Understanding these flows gives you a
    framework for anticipating major market moves.

    **The key players and metrics:** The **Federal Reserve Balance Sheet** is ground zero for liquidity analysis. When
    the Fed buys Treasury bonds and mortgage-backed securities (Quantitative Easing or QE), it creates new bank reserves
    and injects money into the system. The balance sheet grew from ~$4 trillion pre-COVID to nearly $9 trillion by 2022.
    Now the Fed is doing Quantitative Tightening (QT), letting bonds mature without replacement, slowly shrinking the
    balance sheet. **M2 Money Supply** is the broadest measure of money - cash, checking accounts, savings, and money
    market funds. M2 exploded during COVID stimulus (checks, PPP loans) and has since contracted, something that hadn't
    happened since the Great Depression. **Reverse Repo (RRP)** is where money market funds park excess cash at the Fed
    overnight. High RRP means there's so much liquidity that it's piling up with nowhere productive to go. The RRP peaked
    at $2.5 trillion in late 2022 and has since drained significantly. **Treasury General Account (TGA)** is the U.S.
    government's checking account. When Treasury builds up the TGA (collecting taxes, issuing debt), it drains liquidity
    from markets. When Treasury spends, money flows back out.

    **How to interpret these charts together:** The "net liquidity" framework many traders use is roughly:
    Fed Balance Sheet minus TGA minus RRP = Net Liquidity available for markets. When this composite rises, it's bullish
    for risk assets. When it falls, expect headwinds. Watch for inflection points: if the Fed signals it will slow or
    stop QT, or if Treasury announces spending programs that drain the TGA, these can be catalysts for market moves.
    The 2023 bank stress (SVB, etc.) forced the Fed to inject emergency liquidity via the BTFP facility, which some
    argue was "stealth QE" and helped fuel the 2023 rally despite ongoing QT. Liquidity analysis is part science, part
    art - but understanding these mechanics puts you ahead of most investors who focus only on earnings and headlines.
    """)

    # Key liquidity metrics
    col1, col2, col3, col4 = st.columns(4)

    fed_bs = fetch_api("/api/indicators/WALCL/latest", silent=True)
    if fed_bs and fed_bs.get('latest_value'):
        with col1:
            val = fed_bs['latest_value'] / 1e6  # Convert to trillions
            st.metric("Fed Balance Sheet", f"${val:.2f}T")

    m2 = fetch_api("/api/indicators/M2SL/latest", silent=True)
    if m2 and m2.get('latest_value'):
        with col2:
            val = m2['latest_value'] / 1000  # Convert to trillions
            st.metric("M2 Money Supply", f"${val:.2f}T")

    rrp = fetch_api("/api/indicators/RRPONTSYD/latest", silent=True)
    if rrp and rrp.get('latest_value'):
        with col3:
            val = rrp['latest_value'] / 1000  # Convert to trillions
            st.metric("Reverse Repo", f"${val:.2f}T")

    tga = fetch_api("/api/indicators/WTREGEN/latest", silent=True)
    if tga and tga.get('latest_value'):
        with col4:
            val = tga['latest_value'] / 1e6  # Convert to trillions
            st.metric("Treasury Account", f"${val:.2f}T")

    st.divider()

    # Fed Balance Sheet chart
    st.subheader("Fed Balance Sheet (Total Assets)")
    time_range = st.selectbox("Time Range", ["1 Year", "5 Years", "10 Years", "Max"], index=2, key="liq_range")
    days_map = {"1 Year": 365, "5 Years": 1825, "10 Years": 3650, "Max": 20000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    fed_data = fetch_api(f"/api/indicators/WALCL/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    if fed_data and fed_data.get('data'):
        df = pd.DataFrame(fed_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['value'] = df['value'] / 1e6  # Convert to trillions

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['value'],
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(20, 184, 166, 0.15)',
            line=dict(color='#14b8a6', width=2)
        ))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Total Assets ($T)",
            template='plotly_dark',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'),
            yaxis=dict(gridcolor='#2D3748')
        )

        st.plotly_chart(fig, use_container_width=True)

    # Credit conditions
    st.subheader("Credit Conditions")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**High Yield Spread (Credit Stress)**")
        hy_data = fetch_api(f"/api/indicators/BAMLH0A0HYM2/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if hy_data and hy_data.get('data'):
            df = pd.DataFrame(hy_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['value'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(246, 173, 85, 0.15)',
                line=dict(color='#F6AD55', width=2)
            ))

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Spread (%)",
                template='plotly_dark',
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='#2D3748'),
                yaxis=dict(gridcolor='#2D3748')
            )

            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**SOFR (Overnight Rate)**")
        sofr_data = fetch_api(f"/api/indicators/SOFR/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if sofr_data and sofr_data.get('data'):
            df = pd.DataFrame(sofr_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['value'],
                mode='lines',
                line=dict(color='#8b5cf6', width=2)
            ))

            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Rate (%)",
                template='plotly_dark',
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='#2D3748'),
                yaxis=dict(gridcolor='#2D3748')
            )

            st.plotly_chart(fig, use_container_width=True)

# Page: Market Regime
elif page == "Market Regime":
    st.header("🔄 Market Regime Dashboard")

    # Comprehensive explanation
    st.markdown("""
    ### Understanding Market Regimes and Style Rotation

    "Market regime" refers to the prevailing environment that determines which types of investments outperform. This is
    NOT about political leadership or who's in office - it's about the fundamental economic conditions that favor certain
    investment styles over others. Markets cycle through distinct regimes: risk-on (investors embrace volatility, speculative
    assets soar), risk-off (flight to safety, defensive assets outperform), growth-led (high P/E tech stocks dominate),
    value-led (cheap stocks with dividends shine), and various combinations. Understanding the current regime helps you
    position your portfolio appropriately and, more importantly, recognize when regimes are shifting - which is when the
    biggest opportunities (and risks) emerge.

    **The major style factors explained:** **Growth vs Value** is the most fundamental divide. Growth stocks are companies
    expected to increase earnings rapidly - think tech giants, disruptors, companies reinvesting all profits into expansion.
    They trade at high price-to-earnings ratios because investors pay up for future potential. Value stocks are mature,
    often "boring" companies trading at low multiples - banks, insurers, energy companies, industrials. They typically pay
    dividends. Growth dominated 2010-2021 during the low-interest-rate era because when rates are near zero, the present
    value of future earnings is high, favoring growth stocks. When rates rose sharply in 2022, Value surged as investors
    sought current income and shunned speculative bets. **Large Cap vs Small Cap** captures the size effect. Large caps
    (S&P 500 companies) are stable, liquid, and globally diversified. Small caps (Russell 2000) are more volatile, more
    domestically focused, and more sensitive to economic cycles. Historically, small caps outperform coming out of recessions
    as economic activity picks up, but lag during slowdowns. **US vs International** reflects geographic allocation.
    The US dominated for a decade (2011-2021) driven by tech. International stocks (Europe, Japan, Emerging Markets) are
    cheaper by valuation and offer diversification, but have lagged due to slower growth, weaker currencies, and geopolitical risks.

    **How to read these charts:** Each chart shows cumulative percentage returns, normalized so both lines start at zero.
    When the Growth line is above Value, growth stocks are winning. The spread between the lines shows the magnitude of
    outperformance. Watch for **crossovers** - when a lagging style overtakes the leader, it often signals a regime change
    that can persist for years. The 2020-2021 period showed extreme growth dominance; 2022 saw a sharp value rotation.
    For portfolio decisions, you might tilt toward the leading style (momentum) or toward the lagging style (mean reversion)
    depending on your philosophy. Many advisors recommend staying balanced across styles and rebalancing periodically,
    capturing gains from whichever regime is working while maintaining exposure to the next rotation.
    """)

    time_range = st.selectbox("Time Range", ["1 Month", "3 Months", "1 Year", "3 Years", "5 Years", "10 Years", "Max"], index=2, key="regime_range")
    days_map = {"1 Month": 30, "3 Months": 90, "1 Year": 365, "3 Years": 1095, "5 Years": 1825, "10 Years": 3650, "Max": 20000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    # Growth vs Value comparison
    st.subheader("Growth vs Value")

    growth_data = fetch_api(f"/api/indicators/IWF/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    value_data = fetch_api(f"/api/indicators/IWD/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)

    if growth_data and growth_data.get('data') and value_data and value_data.get('data'):
        growth_df = pd.DataFrame(growth_data['data'])
        growth_df['timestamp'] = pd.to_datetime(growth_df['timestamp'])
        value_df = pd.DataFrame(value_data['data'])
        value_df['timestamp'] = pd.to_datetime(value_df['timestamp'])

        # Normalize to percentage change
        growth_df = growth_df.sort_values('timestamp')
        value_df = value_df.sort_values('timestamp')
        growth_start = growth_df.iloc[0]['value']
        value_start = value_df.iloc[0]['value']
        growth_df['pct'] = ((growth_df['value'] - growth_start) / growth_start) * 100
        value_df['pct'] = ((value_df['value'] - value_start) / value_start) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=growth_df['timestamp'], y=growth_df['pct'], mode='lines',
                                 name='Growth (IWF)', line=dict(color='#14b8a6', width=2)))
        fig.add_trace(go.Scatter(x=value_df['timestamp'], y=value_df['pct'], mode='lines',
                                 name='Value (IWD)', line=dict(color='#F6AD55', width=2)))

        fig.update_layout(
            xaxis_title="Date", yaxis_title="Return (%)", template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Show which is leading
        growth_return = growth_df.iloc[-1]['pct']
        value_return = value_df.iloc[-1]['pct']
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Growth Return", f"{growth_return:.1f}%")
        with col2:
            st.metric("Value Return", f"{value_return:.1f}%")
        with col3:
            leader = "Growth" if growth_return > value_return else "Value"
            spread = abs(growth_return - value_return)
            st.metric("Current Leader", leader, f"+{spread:.1f}%")

    st.divider()

    # Large Cap vs Small Cap
    st.subheader("Large Cap vs Small Cap")

    spy_data = fetch_api(f"/api/indicators/SPY/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    iwm_data = fetch_api(f"/api/indicators/IWM/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)

    if spy_data and spy_data.get('data') and iwm_data and iwm_data.get('data'):
        spy_df = pd.DataFrame(spy_data['data'])
        spy_df['timestamp'] = pd.to_datetime(spy_df['timestamp'])
        iwm_df = pd.DataFrame(iwm_data['data'])
        iwm_df['timestamp'] = pd.to_datetime(iwm_df['timestamp'])

        spy_df = spy_df.sort_values('timestamp')
        iwm_df = iwm_df.sort_values('timestamp')
        spy_start = spy_df.iloc[0]['value']
        iwm_start = iwm_df.iloc[0]['value']
        spy_df['pct'] = ((spy_df['value'] - spy_start) / spy_start) * 100
        iwm_df['pct'] = ((iwm_df['value'] - iwm_start) / iwm_start) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=spy_df['timestamp'], y=spy_df['pct'], mode='lines',
                                 name='Large Cap (SPY)', line=dict(color='#8b5cf6', width=2)))
        fig.add_trace(go.Scatter(x=iwm_df['timestamp'], y=iwm_df['pct'], mode='lines',
                                 name='Small Cap (IWM)', line=dict(color='#B794F4', width=2)))

        fig.update_layout(
            xaxis_title="Date", yaxis_title="Return (%)", template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # US vs International
    st.subheader("US vs International")

    efa_data = fetch_api(f"/api/indicators/EFA/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    eem_data = fetch_api(f"/api/indicators/EEM/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)

    if spy_data and efa_data and efa_data.get('data') and eem_data and eem_data.get('data'):
        efa_df = pd.DataFrame(efa_data['data'])
        efa_df['timestamp'] = pd.to_datetime(efa_df['timestamp'])
        eem_df = pd.DataFrame(eem_data['data'])
        eem_df['timestamp'] = pd.to_datetime(eem_df['timestamp'])

        efa_df = efa_df.sort_values('timestamp')
        eem_df = eem_df.sort_values('timestamp')
        efa_start = efa_df.iloc[0]['value']
        eem_start = eem_df.iloc[0]['value']
        efa_df['pct'] = ((efa_df['value'] - efa_start) / efa_start) * 100
        eem_df['pct'] = ((eem_df['value'] - eem_start) / eem_start) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=spy_df['timestamp'], y=spy_df['pct'], mode='lines',
                                 name='US (SPY)', line=dict(color='#14b8a6', width=2)))
        fig.add_trace(go.Scatter(x=efa_df['timestamp'], y=efa_df['pct'], mode='lines',
                                 name='Developed (EFA)', line=dict(color='#8b5cf6', width=2)))
        fig.add_trace(go.Scatter(x=eem_df['timestamp'], y=eem_df['pct'], mode='lines',
                                 name='Emerging (EEM)', line=dict(color='#F6AD55', width=2)))

        fig.update_layout(
            xaxis_title="Date", yaxis_title="Return (%)", template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )

        st.plotly_chart(fig, use_container_width=True)

# Page: Inflation Monitor
elif page == "Inflation Monitor":
    st.header("🔥 Inflation Monitor")

    # Comprehensive explanation
    st.markdown("""
    ### Understanding Inflation: The Hidden Tax on Your Money

    Inflation measures how quickly prices rise across the economy, eroding the purchasing power of your dollars. If inflation
    runs at 3% annually, something costing $100 today will cost $103 next year - and your savings lose 3% of their real value
    unless invested at returns exceeding inflation. The Federal Reserve targets 2% annual inflation as the "Goldilocks" rate:
    high enough to encourage spending (why save if prices will be the same next year?) but low enough to maintain price
    stability. When inflation exceeds this target, the Fed raises interest rates to cool the economy, which typically hurts
    stock and bond prices. This is why investors obsess over inflation data - it directly drives Fed policy, which drives markets.

    **The key metrics decoded:** **CPI (Consumer Price Index)** is the headline inflation number you see in news reports. The
    Bureau of Labor Statistics surveys prices for ~80,000 items monthly to construct this index. **Core CPI** strips out food
    and energy because they're volatile (oil price swings, weather affecting crops) and can distort the underlying trend. Fed
    officials focus on core measures to see "sticky" inflation that persists month to month. **PCE (Personal Consumption
    Expenditures)** is actually the Fed's *preferred* measure, not CPI, because it captures a broader spending basket and
    adjusts for consumer substitution (if beef gets expensive, people buy chicken - PCE accounts for this, CPI doesn't).
    **10-Year Breakeven Inflation** is derived from bond markets: it's the difference between regular Treasury yields and
    inflation-protected TIPS yields. This tells you what bond traders expect inflation to average over the next decade -
    market expectations, not government statistics. When breakevens rise, markets are pricing in higher future inflation.

    **Understanding the component breakdown below:** Inflation doesn't hit all goods equally. **Shelter (housing/rent)** is
    the largest component (~33% of CPI) and is notoriously "lagging" - it takes 12-18 months for actual rent changes to show
    up in the data due to how it's measured. This is why CPI stayed elevated in 2023 even as real-time rent data cooled.
    **Food at home** (groceries) and **food away from home** (restaurants) are separated because they have different dynamics -
    restaurants include labor costs, which are stickier. **Gasoline** is the most volatile component, swinging wildly with
    oil prices. **Used vehicles** caused a huge inflation spike in 2021-2022 due to supply chain issues, then deflated.
    By examining which components are driving the headline number, you can better predict whether inflation will persist
    (shelter-driven = sticky) or fade (energy/goods-driven = likely transitory). The spending breakdown shows where American
    consumers actually allocate their budgets, giving context to which price changes matter most for household finances.
    """)

    # Calculate YoY inflation from index
    def get_yoy_inflation(series_id):
        # Request 2 years of data to ensure we have enough for YoY calculation (need 13+ monthly points)
        two_years_ago = (datetime.now() - timedelta(days=730)).isoformat()
        data = fetch_api(f"/api/indicators/{series_id}/timeseries?start={two_years_ago}&limit=500", silent=True)
        if data and data.get('data') and len(data['data']) > 12:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            current = df.iloc[-1]['value']
            year_ago = df.iloc[-13]['value'] if len(df) >= 13 else df.iloc[0]['value']
            return ((current - year_ago) / year_ago) * 100
        return None

    # Key inflation metrics
    st.subheader("Headline Metrics")
    col1, col2, col3, col4 = st.columns(4)

    cpi_yoy = get_yoy_inflation("CPIAUCSL")
    core_cpi_yoy = get_yoy_inflation("CPILFESL")
    pce_yoy = get_yoy_inflation("PCEPI")
    breakeven = fetch_api("/api/indicators/T10YIE/latest", silent=True)

    with col1:
        if cpi_yoy:
            color = "normal" if cpi_yoy <= 3 else "inverse"
            st.metric("CPI (YoY)", f"{cpi_yoy:.1f}%", delta="Above target" if cpi_yoy > 2 else "At target", delta_color=color)
    with col2:
        if core_cpi_yoy:
            st.metric("Core CPI (YoY)", f"{core_cpi_yoy:.1f}%")
    with col3:
        if pce_yoy:
            st.metric("PCE (YoY)", f"{pce_yoy:.1f}%")
    with col4:
        if breakeven and breakeven.get('latest_value'):
            st.metric("10Y Breakeven", f"{breakeven['latest_value']:.2f}%")

    st.divider()

    # Time range selector
    time_range = st.selectbox("Time Range", ["1 Year", "3 Years", "5 Years", "10 Years", "20 Years", "Max"], index=3, key="inf_range")
    days_map = {"1 Year": 365, "3 Years": 1095, "5 Years": 1825, "10 Years": 3650, "20 Years": 7300, "Max": 20000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    # CPI chart
    st.subheader("Consumer Price Index (YoY Change)")
    cpi_data = fetch_api(f"/api/indicators/CPIAUCSL/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    if cpi_data and cpi_data.get('data'):
        df = pd.DataFrame(cpi_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        df['yoy'] = df['value'].pct_change(periods=12) * 100

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['yoy'], mode='lines', fill='tozeroy',
                                 fillcolor='rgba(239, 68, 68, 0.15)', line=dict(color='#ef4444', width=2)))
        fig.add_hline(y=2, line_dash="dash", line_color="#10b981", annotation_text="2% Target")
        fig.update_layout(xaxis_title="Date", yaxis_title="YoY Change (%)", template='plotly_dark', height=400,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Consumer Basket Breakdown
    st.subheader("Consumer Basket Breakdown (YoY Inflation by Category)")
    st.caption("Shows which components of the CPI are driving inflation. Click 'Refresh FRED' in sidebar if data is missing.")

    # CPI component series
    cpi_components = [
        ("CUSR0000SAH1", "Shelter (Housing/Rent)", "#ef4444"),
        ("CUSR0000SAF11", "Food at Home", "#F6AD55"),
        ("CUSR0000SEFV", "Food Away from Home", "#10b981"),
        ("CUUR0000SETB01", "Gasoline", "#8b5cf6"),
        ("CUSR0000SEEB", "Electricity", "#B794F4"),
        ("CUSR0000SAM2", "Medical Care", "#14b8a6"),
        ("CUSR0000SETA02", "Used Vehicles", "#ED64A6"),
        ("CPIAPPSL", "Apparel", "#A0AEC0"),
    ]

    component_yoy = []
    for series_id, name, color in cpi_components:
        yoy = get_yoy_inflation(series_id)
        if yoy is not None:
            component_yoy.append({"Category": name, "YoY %": yoy, "color": color})

    if component_yoy:
        comp_df = pd.DataFrame(component_yoy).sort_values("YoY %", ascending=True)
        colors = ['#10b981' if v <= 2 else '#F6AD55' if v <= 5 else '#ef4444' for v in comp_df['YoY %']]

        fig = go.Figure(go.Bar(
            x=comp_df['YoY %'],
            y=comp_df['Category'],
            orientation='h',
            marker_color=colors,
            text=[f"{v:.1f}%" for v in comp_df['YoY %']],
            textposition='outside'
        ))
        fig.add_vline(x=2, line_dash="dash", line_color="#10b981", annotation_text="2% Target")
        fig.update_layout(title="Current YoY Inflation by Category", xaxis_title="YoY Change (%)", yaxis_title="",
                         template='plotly_dark', height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Consumer basket data not yet loaded. Click 'Refresh FRED' in the sidebar to fetch CPI component data.")

    st.divider()

    # ============================================================================
    # WHERE DOES YOUR MONEY GO? - Consumer Spending & Inflation Module
    # ============================================================================
    # Import canonical categories and data loaders
    from categories import (
        CANONICAL_CATEGORIES, PCE_SERIES_MAP, CPI_SERIES_MAP,
        CPI_WEIGHTS, BLS_CEX_2023, get_category_color, get_category_icon
    )

    st.subheader("💰 Where Does Your Money Go?")
    st.markdown("""
    This section answers: *Where does the average American's spending go, and how has inflation changed those buckets?*

    **Important distinction:** PCE (Personal Consumption Expenditures) includes third-party payments (employer health insurance,
    government benefits) and imputed values (homeowner equivalent rent). BLS Consumer Expenditure Survey measures what households
    actually pay out-of-pocket. PCE per household is ~$159k/year; out-of-pocket is ~$78k/year.
    """)

    # ========== PART A: Spending Breakdown ==========
    st.markdown("### Part A: Consumer Spending Breakdown")

    # Spending basis toggle
    spending_basis = st.radio(
        "Spending Measure:",
        ["PCE (National Accounts)", "Out-of-pocket (BLS CEX)"],
        horizontal=True,
        key="spending_basis",
        help="PCE includes third-party payments & imputed values. BLS CEX is actual out-of-pocket spending."
    )

    if spending_basis == "PCE (National Accounts)":
        # ===== PCE-based spending =====
        st.caption("*PCE per household includes employer-paid insurance, imputed rent for homeowners, and other non-cash items.*")

        # Controls
        ctrl_col1, ctrl_col2 = st.columns(2)
        with ctrl_col1:
            pce_view = st.radio("View:", ["Per Household", "Per Capita", "Total ($B)"], horizontal=True, key="pce_view")
        with ctrl_col2:
            show_pct = st.checkbox("Show as % of total", key="pce_pct")

        # Fetch PCE data
        total_pce_data = fetch_api("/api/indicators/PCE/latest", silent=True)
        total_pce_billions = total_pce_data.get('latest_value', 0) if total_pce_data else 0
        pce_timestamp = total_pce_data.get('timestamp', '') if total_pce_data else ''

        hh_data = fetch_api("/api/indicators/TTLHH/latest", silent=True)
        if not hh_data or not hh_data.get('latest_value'):
            hh_data = fetch_api("/api/indicators/TTLHHM156N/latest", silent=True)
        households = hh_data.get('latest_value', 0) if hh_data else 0  # thousands

        pop_data = fetch_api("/api/indicators/POPTHM/latest", silent=True)
        if not pop_data or not pop_data.get('latest_value'):
            pop_data = fetch_api("/api/indicators/POP/latest", silent=True)
        population = pop_data.get('latest_value', 0) if pop_data else 0  # thousands

        # Fetch category data using canonical mapping
        spending_data = []
        for series_id, category in PCE_SERIES_MAP.items():
            data = fetch_api(f"/api/indicators/{series_id}/latest", silent=True)
            if data and data.get('latest_value'):
                cat_info = CANONICAL_CATEGORIES.get(category, {})
                spending_data.append({
                    "category": category,
                    "value_billions": data['latest_value'],
                    "color": cat_info.get("color", "#718096"),
                    "icon": cat_info.get("icon", "📦"),
                    "description": cat_info.get("description", ""),
                })

        if spending_data and total_pce_billions > 0:
            spend_df = pd.DataFrame(spending_data)

            # Calculate "Other" as remainder
            detailed_total = spend_df['value_billions'].sum()
            other_billions = total_pce_billions - detailed_total
            if other_billions > 50:  # Only show if significant
                spend_df = pd.concat([spend_df, pd.DataFrame([{
                    "category": "Other (Education, Telecom, etc.)",
                    "value_billions": other_billions,
                    "color": "#4A5568",
                    "icon": "📦",
                    "description": "Education, communication, personal care, misc services",
                }])], ignore_index=True)

            # Calculate per-unit values
            if households > 0:
                spend_df['per_household'] = (spend_df['value_billions'] * 1e9) / (households * 1e3)
            if population > 0:
                spend_df['per_capita'] = (spend_df['value_billions'] * 1e9) / (population * 1e3)
            spend_df['pct_of_total'] = (spend_df['value_billions'] / total_pce_billions) * 100

            # Determine display column
            if pce_view == "Per Household" and households > 0:
                value_col = 'per_household'
                value_label = "Annual $ per Household"
                divisor_count = households * 1e3
            elif pce_view == "Per Capita" and population > 0:
                value_col = 'per_capita'
                value_label = "Annual $ per Person"
                divisor_count = population * 1e3
            else:
                value_col = 'value_billions'
                value_label = "Total ($B)"
                divisor_count = 1

            # Sort and prepare display
            spend_df = spend_df.sort_values(value_col, ascending=True)
            spend_df['display_label'] = spend_df.apply(lambda r: f"{r['icon']} {r['category']}", axis=1)

            # Create chart
            if show_pct:
                x_vals = spend_df['pct_of_total']
                text_vals = [f"{v:.1f}%" for v in x_vals]
                x_title = "% of Total PCE"
            elif value_col == 'value_billions':
                x_vals = spend_df[value_col]
                text_vals = [f"${v:,.0f}B" for v in x_vals]
                x_title = "Billions of Dollars"
            else:
                x_vals = spend_df[value_col]
                text_vals = [f"${v:,.0f}" for v in x_vals]
                x_title = value_label

            fig = go.Figure(go.Bar(
                x=x_vals,
                y=spend_df['display_label'],
                orientation='h',
                marker_color=spend_df['color'].tolist(),
                text=text_vals,
                textposition='outside',
                hovertemplate="<b>%{y}</b><br>" +
                              f"Value: %{{x:,.0f}}<br>" +
                              "% of Total: %{customdata:.1f}%<extra></extra>",
                customdata=spend_df['pct_of_total']
            ))
            fig.update_layout(
                title=f"PCE Spending by Category ({value_label})",
                xaxis_title=x_title,
                yaxis_title="",
                template='plotly_dark',
                height=max(450, len(spend_df) * 38),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='#2D3748'),
                margin=dict(l=10, r=80)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total PCE", f"${total_pce_billions:,.0f}B")
            with col2:
                if households > 0:
                    pce_per_hh = (total_pce_billions * 1e9) / (households * 1e3)
                    st.metric("PCE per Household", f"${pce_per_hh:,.0f}/yr")
            with col3:
                if population > 0:
                    pce_per_cap = (total_pce_billions * 1e9) / (population * 1e3)
                    st.metric("PCE per Capita", f"${pce_per_cap:,.0f}/yr")
            with col4:
                st.metric("US Households", f"{households/1e3:.1f}M")

            # Data provenance
            st.caption(f"*Data: BEA Personal Consumption Expenditures via FRED. PCE data as of {pce_timestamp[:10] if pce_timestamp else 'N/A'}.*")

        else:
            st.info("PCE spending data not yet loaded. Click 'Refresh FRED' in the sidebar.")

    else:
        # ===== BLS Consumer Expenditure Survey (Out-of-pocket) =====
        st.caption("*Out-of-pocket spending per consumer unit (≈ household). Excludes employer-paid benefits and imputed values.*")

        bls_data = BLS_CEX_2023
        total_expenditure = bls_data["total"]
        categories = bls_data["categories"]

        # Build dataframe
        bls_df = pd.DataFrame([
            {
                "category": cat,
                "value": val,
                "color": CANONICAL_CATEGORIES.get(cat, {}).get("color", "#718096"),
                "icon": CANONICAL_CATEGORIES.get(cat, {}).get("icon", "📦"),
                "pct": (val / total_expenditure) * 100
            }
            for cat, val in categories.items()
        ])
        bls_df = bls_df.sort_values('value', ascending=True)
        bls_df['display_label'] = bls_df.apply(lambda r: f"{r['icon']} {r['category']}", axis=1)

        # Controls
        show_pct_bls = st.checkbox("Show as % of total", key="bls_pct")

        if show_pct_bls:
            x_vals = bls_df['pct']
            text_vals = [f"{v:.1f}%" for v in x_vals]
            x_title = "% of Total Expenditure"
        else:
            x_vals = bls_df['value']
            text_vals = [f"${v:,.0f}" for v in x_vals]
            x_title = "Annual $ per Consumer Unit"

        fig = go.Figure(go.Bar(
            x=x_vals,
            y=bls_df['display_label'],
            orientation='h',
            marker_color=bls_df['color'].tolist(),
            text=text_vals,
            textposition='outside'
        ))
        fig.update_layout(
            title="Out-of-Pocket Spending by Category (BLS Consumer Expenditure Survey 2023)",
            xaxis_title=x_title,
            yaxis_title="",
            template='plotly_dark',
            height=max(450, len(bls_df) * 38),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'),
            margin=dict(l=10, r=80)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Annual Expenditure", f"${total_expenditure:,.0f}")
        with col2:
            st.metric("Monthly Expenditure", f"${total_expenditure/12:,.0f}")
        with col3:
            st.metric("Survey Year", "2023")

        st.caption("*Data: BLS Consumer Expenditure Survey. 'Consumer unit' ≈ household but not identical (can include single individuals).*")

    st.divider()

    # ========== PART B: Inflation Impact - Indexed Price Growth ==========
    st.markdown("### Part B: Inflation Impact Over Time")

    # Timeframe selector
    inf_col1, inf_col2 = st.columns([1, 2])
    with inf_col1:
        timeframe = st.radio(
            "Timeframe:",
            ["5 Years", "10 Years", "20 Years", "30 Years"],
            horizontal=False,
            key="inflation_impact_range"
        )
    years_map = {"5 Years": 5, "10 Years": 10, "20 Years": 20, "30 Years": 30}
    years_back = years_map[timeframe]
    start_date_impact = datetime.now() - timedelta(days=years_back * 365)
    end_date_display = datetime.now().strftime("%b %Y")
    start_date_display = start_date_impact.strftime("%b %Y")

    with inf_col2:
        # Category multiselect - default to top categories
        all_cpi_categories = list(CPI_SERIES_MAP.values())
        default_categories = ["Shelter", "Food at home", "Food away from home", "Gasoline & fuel", "Medical care", "Vehicles"]
        selected_categories = st.multiselect(
            "Categories to display:",
            options=all_cpi_categories,
            default=[c for c in default_categories if c in all_cpi_categories],
            key="inflation_categories"
        )

    if not selected_categories:
        selected_categories = default_categories

    # Fetch CPI time series for selected categories
    inflation_series = []
    for series_id, category in CPI_SERIES_MAP.items():
        if category not in selected_categories:
            continue

        data = fetch_api(
            f"/api/indicators/{series_id}/timeseries?start={start_date_impact.isoformat()}&limit=10000",
            silent=True
        )
        if data and data.get('data') and len(data['data']) > 12:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')

            base_value = df.iloc[0]['value']
            end_value = df.iloc[-1]['value']
            df['indexed'] = (df['value'] / base_value) * 100
            cumulative = ((end_value / base_value) - 1) * 100
            actual_years = (df.iloc[-1]['timestamp'] - df.iloc[0]['timestamp']).days / 365.25
            cagr = ((end_value / base_value) ** (1 / actual_years) - 1) * 100 if actual_years > 0 else 0

            inflation_series.append({
                "category": category,
                "color": get_category_color(category),
                "df": df,
                "start_date": df.iloc[0]['timestamp'],
                "end_date": df.iloc[-1]['timestamp'],
                "cumulative": cumulative,
                "cagr": cagr,
                "weight": CPI_WEIGHTS.get(category, 0)
            })

    # Also fetch headline CPI
    overall_cpi = fetch_api(
        f"/api/indicators/CPIAUCSL/timeseries?start={start_date_impact.isoformat()}&limit=10000",
        silent=True
    )
    headline_stats = None
    if overall_cpi and overall_cpi.get('data'):
        cpi_df = pd.DataFrame(overall_cpi['data'])
        cpi_df['timestamp'] = pd.to_datetime(cpi_df['timestamp'])
        cpi_df = cpi_df.sort_values('timestamp')
        cpi_start = cpi_df.iloc[0]['value']
        cpi_end = cpi_df.iloc[-1]['value']
        cpi_df['indexed'] = (cpi_df['value'] / cpi_start) * 100
        headline_cumulative = ((cpi_end / cpi_start) - 1) * 100
        actual_years = (cpi_df.iloc[-1]['timestamp'] - cpi_df.iloc[0]['timestamp']).days / 365.25
        headline_cagr = ((cpi_end / cpi_start) ** (1 / actual_years) - 1) * 100 if actual_years > 0 else 0
        headline_stats = {"cumulative": headline_cumulative, "cagr": headline_cagr, "df": cpi_df}

    if inflation_series:
        # Sort by cumulative inflation
        inflation_series = sorted(inflation_series, key=lambda x: x['cumulative'], reverse=True)

        # Create indexed line chart
        fig = go.Figure()

        # Add headline CPI first (dashed)
        if headline_stats:
            fig.add_trace(go.Scatter(
                x=headline_stats['df']['timestamp'],
                y=headline_stats['df']['indexed'],
                mode='lines',
                name=f"All Items CPI (+{headline_stats['cumulative']:.0f}%)",
                line=dict(color='#E2E8F0', width=3, dash='dash'),
            ))

        # Add category lines
        for series in inflation_series:
            fig.add_trace(go.Scatter(
                x=series['df']['timestamp'],
                y=series['df']['indexed'],
                mode='lines',
                name=f"{series['category']} (+{series['cumulative']:.0f}%)",
                line=dict(color=series['color'], width=2),
            ))

        fig.add_hline(y=100, line_dash="dot", line_color="#4A5568", annotation_text="Baseline")

        fig.update_layout(
            title=f"Cumulative Price Growth by Category ({start_date_display} - {end_date_display})",
            xaxis_title="Date",
            yaxis_title="Price Index (Start = 100)",
            template='plotly_dark',
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'),
            yaxis=dict(gridcolor='#2D3748'),
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Summary statistics table
        st.markdown("**Summary Statistics**")
        summary_data = []
        if headline_stats:
            summary_data.append({
                "Category": "📊 All Items (CPI)",
                f"Cumulative ({years_back}Y)": f"+{headline_stats['cumulative']:.1f}%",
                "CAGR": f"+{headline_stats['cagr']:.2f}%",
                "CPI Weight": "100%"
            })
        for series in inflation_series:
            summary_data.append({
                "Category": f"{get_category_icon(series['category'])} {series['category']}",
                f"Cumulative ({years_back}Y)": f"+{series['cumulative']:.1f}%",
                "CAGR": f"+{series['cagr']:.2f}%",
                "CPI Weight": f"{series['weight']:.1f}%"
            })

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

        # Key metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            if headline_stats:
                st.metric(f"Overall CPI ({years_back}Y)", f"+{headline_stats['cumulative']:.1f}%", f"CAGR: +{headline_stats['cagr']:.2f}%")
        with col2:
            highest = inflation_series[0]
            st.metric("Highest Category", highest['category'], f"+{highest['cumulative']:.0f}%")
        with col3:
            lowest = inflation_series[-1]
            st.metric("Lowest Category", lowest['category'], f"+{lowest['cumulative']:.0f}%")

        st.caption(f"*Data: BLS Consumer Price Index via FRED. Period: {start_date_display} to {end_date_display}.*")

    else:
        st.info("CPI component data not yet loaded. Click 'Refresh FRED' in the sidebar.")

    st.divider()

    # ========== PART C: Current YoY Inflation by Category ==========
    st.markdown("### Part C: Current Inflation by Category (YoY)")

    # Calculate current YoY for each CPI category
    yoy_data = []
    for series_id, category in CPI_SERIES_MAP.items():
        two_years_ago = datetime.now() - timedelta(days=730)
        data = fetch_api(
            f"/api/indicators/{series_id}/timeseries?start={two_years_ago.isoformat()}&limit=500",
            silent=True
        )
        if data and data.get('data') and len(data['data']) >= 13:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            current = df.iloc[-1]['value']
            year_ago = df.iloc[-13]['value']
            yoy = ((current - year_ago) / year_ago) * 100
            yoy_data.append({
                "category": category,
                "yoy": yoy,
                "color": get_category_color(category),
                "weight": CPI_WEIGHTS.get(category, 0)
            })

    if yoy_data:
        yoy_df = pd.DataFrame(yoy_data).sort_values('yoy', ascending=True)
        yoy_df['display_label'] = yoy_df.apply(lambda r: f"{get_category_icon(r['category'])} {r['category']}", axis=1)

        # Color bars by inflation level
        bar_colors = ['#10b981' if v <= 2 else '#F6AD55' if v <= 5 else '#ef4444' for v in yoy_df['yoy']]

        fig = go.Figure(go.Bar(
            x=yoy_df['yoy'],
            y=yoy_df['display_label'],
            orientation='h',
            marker_color=bar_colors,
            text=[f"{v:+.1f}%" for v in yoy_df['yoy']],
            textposition='outside'
        ))
        fig.add_vline(x=2, line_dash="dash", line_color="#10b981", annotation_text="2% Target")
        fig.update_layout(
            title="Current Year-over-Year Inflation by Category",
            xaxis_title="YoY Change (%)",
            yaxis_title="",
            template='plotly_dark',
            height=max(350, len(yoy_df) * 40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'),
            margin=dict(l=10, r=60)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.caption("*Data: BLS Consumer Price Index via FRED. Green = at/below 2% target, Orange = 2-5%, Red = above 5%.*")

    st.divider()

    # ========== PART D: Contribution to YoY Inflation (Stacked) ==========
    st.markdown("### Part D: Category Contributions to Headline Inflation")
    st.caption("Shows how much each category contributes to total CPI inflation, weighted by importance in consumer spending.")

    # Timeframe for contribution chart
    contrib_timeframe = st.radio(
        "Timeframe:",
        ["3 Years", "5 Years", "10 Years"],
        horizontal=True,
        key="contrib_timeframe"
    )
    contrib_years = {"3 Years": 3, "5 Years": 5, "10 Years": 10}[contrib_timeframe]
    contrib_start = datetime.now() - timedelta(days=contrib_years * 365)

    # Fetch monthly YoY data for each CPI category
    contrib_series = {}
    for series_id, category in CPI_SERIES_MAP.items():
        weight = CPI_WEIGHTS.get(category, 0)
        if weight <= 0:
            continue

        data = fetch_api(
            f"/api/indicators/{series_id}/timeseries?start={contrib_start.isoformat()}&limit=5000",
            silent=True
        )
        if data and data.get('data') and len(data['data']) >= 13:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            # Calculate YoY for each month
            df['yoy'] = df['value'].pct_change(periods=12) * 100
            df = df.dropna(subset=['yoy'])
            # Calculate weighted contribution
            df['contribution'] = df['yoy'] * (weight / 100)
            df['category'] = category
            contrib_series[category] = df[['timestamp', 'yoy', 'contribution', 'category']].copy()

    if contrib_series:
        # Combine all series
        contrib_df = pd.concat(contrib_series.values(), ignore_index=True)

        # Pivot for stacked area chart
        pivot_df = contrib_df.pivot_table(
            index='timestamp',
            columns='category',
            values='contribution',
            aggfunc='mean'
        ).reset_index()

        # Get category order by average contribution (largest first)
        category_order = contrib_df.groupby('category')['contribution'].mean().abs().sort_values(ascending=False).index.tolist()

        # Create stacked area chart
        fig = go.Figure()

        for category in reversed(category_order):  # Reverse so largest is on bottom
            if category in pivot_df.columns:
                fig.add_trace(go.Scatter(
                    x=pivot_df['timestamp'],
                    y=pivot_df[category],
                    mode='lines',
                    name=category,
                    stackgroup='one',
                    line=dict(width=0.5),
                    fillcolor=get_category_color(category),
                ))

        fig.add_hline(y=0, line_dash="solid", line_color="#4A5568")
        fig.add_hline(y=2, line_dash="dash", line_color="#10b981", annotation_text="2% Target")

        fig.update_layout(
            title=f"Contribution to Headline CPI Inflation by Category ({contrib_timeframe})",
            xaxis_title="Date",
            yaxis_title="Contribution to YoY Inflation (%)",
            template='plotly_dark',
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#2D3748'),
            yaxis=dict(gridcolor='#2D3748'),
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Show contribution breakdown table for latest month
        latest_month = contrib_df['timestamp'].max()
        latest_contrib = contrib_df[contrib_df['timestamp'] == latest_month].copy()
        latest_contrib = latest_contrib.sort_values('contribution', ascending=False)

        with st.expander("View latest month contribution breakdown"):
            table_data = []
            for _, row in latest_contrib.iterrows():
                table_data.append({
                    "Category": f"{get_category_icon(row['category'])} {row['category']}",
                    "YoY Inflation": f"{row['yoy']:+.1f}%",
                    "CPI Weight": f"{CPI_WEIGHTS.get(row['category'], 0):.1f}%",
                    "Contribution": f"{row['contribution']:+.2f}pp",
                })
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        st.caption("*Contribution = Category YoY × CPI Weight. Weights are approximate (Dec 2024 relative importance). "
                   "Categories shown cover ~75% of CPI; remainder grouped as 'Other'.*")

    else:
        st.info("Insufficient data for contribution analysis. Click 'Refresh FRED' in the sidebar.")

    st.divider()

    # Inflation expectations
    st.subheader("Market Inflation Expectations (10Y Breakeven)")
    breakeven_data = fetch_api(f"/api/indicators/T10YIE/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    if breakeven_data and breakeven_data.get('data'):
        df = pd.DataFrame(breakeven_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines', fill='tozeroy',
                                 fillcolor='rgba(139, 92, 246, 0.15)', line=dict(color='#8b5cf6', width=2)))
        fig.add_hline(y=2, line_dash="dash", line_color="#10b981", annotation_text="2% Target")
        fig.update_layout(xaxis_title="Date", yaxis_title="Breakeven Rate (%)", template='plotly_dark', height=400,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
        st.plotly_chart(fig, use_container_width=True)

# Page: Recession Watch
elif page == "Recession Watch":
    st.header("🚨 Recession Watch Dashboard")

    # Comprehensive explanation
    st.markdown("""
    ### Reading the Economic Tea Leaves: Recession Indicators

    A recession is officially defined as a "significant decline in economic activity spread across the economy, lasting more
    than a few months." The National Bureau of Economic Research (NBER) is the official arbiter, but they typically don't
    declare recessions until months after they've begun - not helpful for investors trying to position portfolios. This
    dashboard tracks the leading indicators that historically flash warning signs *before* recessions hit, giving you
    advance notice. No single indicator is perfect, but when multiple signals align, the probability of recession rises
    significantly. The key is distinguishing between brief softness (normal economic fluctuations) and genuine deterioration
    (the early stages of recession).

    **The indicator toolkit explained:** The **Yield Curve (10Y-2Y spread)** is the most famous recession predictor - an
    inverted curve (negative spread) has preceded every U.S. recession since 1955 with only one false positive. The lead
    time varies from 6-24 months, which is both useful (advance warning) and frustrating (hard to time). The **Unemployment
    Rate** is a lagging indicator - it rises *during* recessions, not before - but the **Sahm Rule** transforms it into a
    real-time signal: when the 3-month average unemployment rate rises 0.5 percentage points above its 12-month low, a
    recession has typically already begun. This rule triggered in 2020 (COVID) and flashed briefly in 2024. **Initial
    Jobless Claims** (weekly unemployment filings) is more timely than the monthly unemployment rate - rising claims signal
    that layoffs are accelerating, often the first sign of economic trouble. **Industrial Production** measures actual
    factory output, mining, and utilities - when production declines for consecutive months, it indicates weakening demand
    for goods. **Housing Starts** is a leading indicator because builders are forward-looking: they pull back on new
    construction when they anticipate falling demand, often 6-12 months before broader economic weakness. **Consumer
    Sentiment** (University of Michigan survey) captures the mood of households - pessimistic consumers spend less,
    and since consumer spending is ~70% of GDP, falling confidence can become a self-fulfilling prophecy.

    **How to interpret these charts together:** Look for *convergence* - when multiple indicators deteriorate simultaneously,
    recession risk is elevated. A single flashing indicator (like yield curve inversion) warrants attention but not panic;
    it could be a false positive or the recession could be years away. But when the yield curve inverts AND jobless claims
    start rising AND industrial production weakens AND housing starts decline - that's when defensive positioning becomes
    prudent. Use the time range selector to see historical patterns: notice how indicators behaved before the 2001, 2008,
    and 2020 recessions. The 2022-2024 period has been unusual: yield curve deeply inverted, yet employment remained strong
    and GDP kept growing, leading to the "soft landing" debate. This dashboard helps you form your own view on recession
    probability by seeing the real-time data that professional economists watch.
    """)

    recession_data = fetch_api("/api/dashboards/recession-watch")
    if recession_data:
        # Display metrics
        create_metric_cards(recession_data['indicators'])

    st.divider()

    # Time range selector
    time_range = st.selectbox("Time Range", ["5 Years", "10 Years", "20 Years", "30 Years", "Max"], index=2, key="recession_range")
    days_map = {"5 Years": 1825, "10 Years": 3650, "20 Years": 7300, "30 Years": 10950, "Max": 20000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    col1, col2 = st.columns(2)

    with col1:
        # Yield Curve
        st.subheader("📉 Yield Curve (10Y-2Y Spread)")
        yield_data = fetch_api(f"/api/indicators/T10Y2Y/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if yield_data and yield_data.get('data'):
            df = pd.DataFrame(yield_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['value'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(255, 99, 99, 0.2)',
                line=dict(color='#ef4444', width=2),
                name='Yield Spread'
            ))

            fig.add_hline(y=0, line_dash="dash", line_color="#E2E8F0", annotation_text="Inversion Line")

            fig.update_layout(
                xaxis_title="Date", yaxis_title="Spread (%)", hovermode='x unified',
                template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748')
            )

            st.plotly_chart(fig, use_container_width=True)

            current_value = df.iloc[-1]['value']
            if current_value < 0:
                st.warning("⚠️ Yield curve is inverted - recession risk elevated")
            else:
                st.success("✅ Yield curve is normal")

        # Housing Starts
        st.subheader("🏠 Housing Starts")
        housing_data = fetch_api(f"/api/indicators/HOUST/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if housing_data and housing_data.get('data'):
            df = pd.DataFrame(housing_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                     fill='tozeroy', fillcolor='rgba(20, 184, 166, 0.1)', line=dict(color='#14b8a6', width=2)))
            fig.update_layout(xaxis_title="Date", yaxis_title="Thousands of Units", template='plotly_dark', height=350,
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Unemployment Rate
        st.subheader("👷 Unemployment Rate")
        unemp_data = fetch_api(f"/api/indicators/UNRATE/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if unemp_data and unemp_data.get('data'):
            df = pd.DataFrame(unemp_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                     fill='tozeroy', fillcolor='rgba(246, 173, 85, 0.15)', line=dict(color='#F6AD55', width=2)))
            fig.update_layout(xaxis_title="Date", yaxis_title="Percent", template='plotly_dark', height=350,
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
            st.plotly_chart(fig, use_container_width=True)

        # Consumer Sentiment
        st.subheader("😊 Consumer Sentiment")
        sentiment_data = fetch_api(f"/api/indicators/UMCSENT/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
        if sentiment_data and sentiment_data.get('data'):
            df = pd.DataFrame(sentiment_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                     fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.15)', line=dict(color='#8b5cf6', width=2)))
            fig.update_layout(xaxis_title="Date", yaxis_title="Index", template='plotly_dark', height=350,
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
            st.plotly_chart(fig, use_container_width=True)

    # Industrial Production
    st.subheader("🏭 Industrial Production")
    indpro_data = fetch_api(f"/api/indicators/INDPRO/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
    if indpro_data and indpro_data.get('data'):
        df = pd.DataFrame(indpro_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                 fill='tozeroy', fillcolor='rgba(183, 148, 244, 0.15)', line=dict(color='#B794F4', width=2)))
        fig.update_layout(xaxis_title="Date", yaxis_title="Index (2017=100)", template='plotly_dark', height=350,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
        st.plotly_chart(fig, use_container_width=True)

# Page: Market Overview
elif page == "Market Overview":
    st.header("📈 Comprehensive Market Overview")

    st.markdown("""
    This page provides a thorough analysis of market conditions across multiple dimensions: breadth, style factors,
    international exposure, fixed income, volatility, valuations, positioning, commodities, correlations, and technicals.
    Use the time range selector below to adjust all charts simultaneously.
    """)

    # Global time range selector
    st.divider()
    time_range = st.selectbox(
        "Time Range (applies to all charts)",
        ["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years", "10 Years", "Max"],
        index=3,
        key="mkt_time_range"
    )
    days_map = {"1 Month": 30, "3 Months": 90, "6 Months": 180, "1 Year": 365,
                "2 Years": 730, "5 Years": 1825, "10 Years": 3650, "Max": 15000}
    mkt_start_date = datetime.now() - timedelta(days=days_map[time_range])

    # Helper function to get return
    def get_return(series_id, days=None):
        """Calculate return for a series over specified days or full period."""
        data = fetch_api(f"/api/indicators/{series_id}/timeseries?start={mkt_start_date.isoformat()}&limit=10000", silent=True)
        if data and data.get('data') and len(data['data']) > 1:
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            if days and len(df) > days:
                start_val = df.iloc[-days-1]['value']
            else:
                start_val = df.iloc[0]['value']
            end_val = df.iloc[-1]['value']
            return ((end_val - start_val) / start_val) * 100, df
        return None, None

    # ============================================================================
    # SECTION 1: MARKET BREADTH & INTERNALS
    # ============================================================================
    st.divider()
    st.subheader("1. Market Breadth & Internals")

    st.markdown("""
    **Market breadth measures whether gains are widespread or concentrated in a few large stocks.** When the S&P 500
    rises but most stocks within it are actually falling, that's a warning sign - the rally is narrow and potentially
    fragile. The most telling breadth indicator is the comparison between the cap-weighted S&P 500 (SPY) and the
    equal-weighted version (RSP). In a cap-weighted index, Apple and Microsoft might represent 12% of the index;
    in equal-weight, they're just 0.4% combined like every other stock.

    **When SPY outperforms RSP**, mega-caps are leading - this characterized 2023's "Magnificent Seven" rally where
    seven tech giants drove most of the gains while the average stock lagged. **When RSP outperforms SPY**, breadth
    is broadening and more stocks are participating - historically a healthier, more sustainable rally. The ratio
    of RSP/SPY, charted over time, reveals these regime shifts. Other breadth metrics include the percentage of
    S&P 500 stocks above their 200-day moving average (healthy >60%, concerning <40%) and the advance/decline line.

    **Why this matters for your portfolio:** Narrow markets tend to be vulnerable to rotation - when the handful
    of leaders stumble, there's nothing to catch the index. Broad markets are more resilient. If you're overweight
    mega-cap tech, a narrow market flatters your returns but also concentrates your risk.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**S&P 500 vs Equal-Weight (SPY vs RSP)**")
        spy_ret, spy_df = get_return("SPY")
        rsp_ret, rsp_df = get_return("RSP")

        if spy_df is not None and rsp_df is not None:
            # Normalize both to 100
            spy_df['normalized'] = (spy_df['value'] / spy_df.iloc[0]['value']) * 100
            rsp_df['normalized'] = (rsp_df['value'] / rsp_df.iloc[0]['value']) * 100

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=spy_df['timestamp'], y=spy_df['normalized'],
                                     name=f"SPY (Cap-Weighted) {spy_ret:+.1f}%", line=dict(color='#14b8a6', width=2)))
            fig.add_trace(go.Scatter(x=rsp_df['timestamp'], y=rsp_df['normalized'],
                                     name=f"RSP (Equal-Weight) {rsp_ret:+.1f}%", line=dict(color='#8b5cf6', width=2)))
            fig.update_layout(title="Cap-Weighted vs Equal-Weight S&P 500", xaxis_title="", yaxis_title="Indexed (Start=100)",
                             template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

            # Breadth indicator
            if spy_ret and rsp_ret:
                spread = rsp_ret - spy_ret
                if spread > 2:
                    st.success(f"Breadth expanding: Equal-weight outperforming by {spread:.1f}pp")
                elif spread < -2:
                    st.warning(f"Narrow leadership: Cap-weight outperforming by {-spread:.1f}pp")
                else:
                    st.info(f"Breadth neutral: Spread of {spread:+.1f}pp")
        else:
            st.info("Breadth data not available. Click 'Refresh Market' to load RSP data.")

    with col2:
        st.markdown("**Large Cap vs Small Cap (SPY vs IWM)**")
        iwm_ret, iwm_df = get_return("IWM")

        if spy_df is not None and iwm_df is not None:
            iwm_df['normalized'] = (iwm_df['value'] / iwm_df.iloc[0]['value']) * 100

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=spy_df['timestamp'], y=spy_df['normalized'],
                                     name=f"SPY (Large Cap) {spy_ret:+.1f}%", line=dict(color='#14b8a6', width=2)))
            fig.add_trace(go.Scatter(x=iwm_df['timestamp'], y=iwm_df['normalized'],
                                     name=f"IWM (Small Cap) {iwm_ret:+.1f}%", line=dict(color='#F6AD55', width=2)))
            fig.update_layout(title="Large Cap vs Small Cap", xaxis_title="", yaxis_title="Indexed (Start=100)",
                             template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Size comparison data not available.")

    # ============================================================================
    # SECTION 2: STYLE & FACTOR PERFORMANCE
    # ============================================================================
    st.divider()
    st.subheader("2. Style & Factor Performance")

    st.markdown("""
    **Investment "factors" are characteristics that explain stock returns beyond just market exposure.** Academic
    research (Fama-French, AQR) has identified several persistent factors that have historically delivered excess
    returns: Value (cheap stocks), Growth (high earnings growth), Momentum (recent winners), Quality (profitable,
    stable companies), and Low Volatility (boring stocks that zig when others zag).

    **Style rotation** - the shift between Growth and Value - is one of the most important market regimes to monitor.
    Growth stocks (high P/E, reinvesting all earnings) dominated from 2010-2021, delivering spectacular returns as
    interest rates fell. Value stocks (low P/E, dividends, "boring" businesses) tend to outperform when rates rise,
    inflation persists, or growth scares hit. In 2022, Value crushed Growth as rates spiked. Understanding which
    style is leading helps with sector allocation: Growth leadership favors tech; Value leadership favors financials,
    energy, and industrials.

    **Factor timing is notoriously difficult**, but understanding factor exposures helps diagnose your portfolio.
    If you own mostly tech growth stocks and Growth is underperforming, you'll lag the market even if stock-picking
    is good. Diversifying across factors (not just sectors) can smooth returns. The Momentum factor captures
    "trend following" - stocks that went up tend to keep going up, until they don't. Quality captures flight-to-safety.
    """)

    # Factor performance comparison
    factors = [
        ("VUG", "Growth", "#14b8a6"),
        ("VTV", "Value", "#8b5cf6"),
        ("MTUM", "Momentum", "#F6AD55"),
        ("QUAL", "Quality", "#B794F4"),
        ("USMV", "Low Vol", "#ef4444"),
        ("IWM", "Small Cap", "#10b981"),
    ]

    factor_returns = []
    for ticker, name, color in factors:
        ret, _ = get_return(ticker)
        if ret is not None:
            factor_returns.append({"Factor": name, "Return": ret, "color": color, "ticker": ticker})

    if factor_returns:
        factor_df = pd.DataFrame(factor_returns).sort_values("Return", ascending=True)

        fig = go.Figure(go.Bar(
            x=factor_df['Return'],
            y=factor_df['Factor'],
            orientation='h',
            marker_color=factor_df['color'].tolist(),
            text=[f"{r:+.1f}%" for r in factor_df['Return']],
            textposition='outside'
        ))
        fig.update_layout(title=f"Factor Performance ({time_range})", xaxis_title="Return (%)", yaxis_title="",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'))
        st.plotly_chart(fig, use_container_width=True)

        # Growth vs Value spread
        growth_ret = next((f['Return'] for f in factor_returns if f['Factor'] == 'Growth'), None)
        value_ret = next((f['Return'] for f in factor_returns if f['Factor'] == 'Value'), None)
        if growth_ret and value_ret:
            gv_spread = growth_ret - value_ret
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Growth vs Value Spread", f"{gv_spread:+.1f}pp",
                         "Growth winning" if gv_spread > 0 else "Value winning")
            with col2:
                best = factor_df.iloc[-1]
                st.metric("Best Factor", best['Factor'], f"{best['Return']:+.1f}%")
            with col3:
                worst = factor_df.iloc[0]
                st.metric("Worst Factor", worst['Factor'], f"{worst['Return']:+.1f}%")
    else:
        st.info("Factor data not available. Click 'Refresh Market' to load factor ETFs.")

    # ============================================================================
    # SECTION 3: INTERNATIONAL MARKETS
    # ============================================================================
    st.divider()
    st.subheader("3. International Markets")

    st.markdown("""
    **International diversification remains one of the few "free lunches" in investing**, though it hasn't felt that
    way for US investors over the past decade. Since 2010, the US has dramatically outperformed international
    developed and emerging markets. This outperformance has been driven by: (1) tech sector dominance (US has more
    mega-cap tech), (2) stronger dollar (hurts international returns for US investors), and (3) better corporate
    governance and earnings growth.

    **However, valuations now heavily favor international stocks.** US stocks trade at ~20x forward earnings while
    European stocks trade at ~13x and Emerging Markets at ~11x. These valuation gaps are historically extreme.
    International outperformance tends to come in multi-year cycles - the 2000s saw Emerging Markets dramatically
    outperform the US. Mean reversion may eventually favor international again. The key catalysts to watch:
    dollar weakness (helps international), China reopening/stimulus, European energy crisis resolution, and
    relative interest rate differentials.

    **Emerging Markets (EEM, VWO)** offer higher growth potential but with higher volatility and political risk.
    China (FXI, MCHI) is the largest EM component but faces structural challenges. India (INDA) has emerged as
    a growth darling. **Developed International (EFA, VGK, EWJ)** offers more stability: Europe has value-oriented
    sectors (financials, industrials), Japan has finally escaped deflation and is seeing corporate governance reforms.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Developed Markets Comparison**")
        developed = [("SPY", "US", "#14b8a6"), ("VGK", "Europe", "#8b5cf6"), ("EWJ", "Japan", "#F6AD55"), ("EWU", "UK", "#B794F4")]
        fig = go.Figure()
        for ticker, name, color in developed:
            ret, df = get_return(ticker)
            if df is not None:
                df['normalized'] = (df['value'] / df.iloc[0]['value']) * 100
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['normalized'],
                                        name=f"{name} {ret:+.1f}%" if ret else name,
                                        line=dict(color=color, width=2)))
        fig.update_layout(title="US vs Developed International", xaxis_title="", yaxis_title="Indexed (Start=100)",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Emerging Markets Comparison**")
        emerging = [("EEM", "EM Broad", "#14b8a6"), ("FXI", "China", "#ef4444"), ("INDA", "India", "#10b981"), ("EWZ", "Brazil", "#F6AD55")]
        fig = go.Figure()
        for ticker, name, color in emerging:
            ret, df = get_return(ticker)
            if df is not None:
                df['normalized'] = (df['value'] / df.iloc[0]['value']) * 100
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['normalized'],
                                        name=f"{name} {ret:+.1f}%" if ret else name,
                                        line=dict(color=color, width=2)))
        fig.update_layout(title="Emerging Markets", xaxis_title="", yaxis_title="Indexed (Start=100)",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    # ============================================================================
    # SECTION 4: FIXED INCOME & CREDIT
    # ============================================================================
    st.divider()
    st.subheader("4. Fixed Income & Credit Markets")

    st.markdown("""
    **Fixed income is far more than "boring bonds."** The credit markets are often smarter than equity markets at
    sniffing out trouble. Credit spreads - the extra yield investors demand to hold corporate bonds over risk-free
    Treasuries - are one of the best recession indicators. When spreads widen sharply (investors demanding more
    compensation for default risk), it often precedes equity market selloffs and economic weakness.

    **The Treasury market** sets the "risk-free rate" that anchors all other asset valuations. Rising Treasury
    yields hurt stock valuations (future earnings discounted at higher rates) and crush existing bond prices
    (2022 was the worst year for bonds in modern history). **TLT (20+ Year Treasury ETF)** moves inversely to
    long-term rates - when rates rise, TLT falls, and vice versa. **TIP (TIPS ETF)** tracks inflation-protected
    bonds, useful for gauging real (inflation-adjusted) yields.

    **Credit quality spectrum:** Investment Grade corporates (LQD) are high-quality companies like Apple and
    Microsoft issuing debt. High Yield or "junk" bonds (HYG, JNK) are riskier issuers offering higher yields.
    The spread between HYG yield and Treasury yield indicates risk appetite. Tight spreads = complacency,
    wide spreads = fear. **Emerging Market bonds (EMB)** offer higher yields but carry currency and political
    risk. The 60/40 portfolio (60% stocks, 40% bonds) relies on bonds zigging when stocks zag - but this
    correlation broke down in 2022 when both fell together, a rare and painful scenario.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Treasury ETFs (Duration Exposure)**")
        treasuries = [("SHY", "1-3Y Treasury", "#10b981"), ("IEF", "7-10Y Treasury", "#8b5cf6"), ("TLT", "20+Y Treasury", "#ef4444")]
        fig = go.Figure()
        for ticker, name, color in treasuries:
            ret, df = get_return(ticker)
            if df is not None:
                df['normalized'] = (df['value'] / df.iloc[0]['value']) * 100
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['normalized'],
                                        name=f"{name} {ret:+.1f}%" if ret else name,
                                        line=dict(color=color, width=2)))
        fig.update_layout(title="Treasury ETFs by Duration", xaxis_title="", yaxis_title="Indexed (Start=100)",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Credit Markets (Risk Appetite)**")
        credit = [("LQD", "Investment Grade", "#14b8a6"), ("HYG", "High Yield", "#F6AD55"), ("EMB", "EM Bonds", "#B794F4")]
        fig = go.Figure()
        for ticker, name, color in credit:
            ret, df = get_return(ticker)
            if df is not None:
                df['normalized'] = (df['value'] / df.iloc[0]['value']) * 100
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['normalized'],
                                        name=f"{name} {ret:+.1f}%" if ret else name,
                                        line=dict(color=color, width=2)))
        fig.update_layout(title="Corporate & EM Bonds", xaxis_title="", yaxis_title="Indexed (Start=100)",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    # Credit spread from FRED
    hy_spread = fetch_api("/api/indicators/BAMLH0A0HYM2EY/latest", silent=True)
    ig_spread = fetch_api("/api/indicators/BAMLC0A0CM/latest", silent=True)
    if hy_spread or ig_spread:
        col1, col2, col3 = st.columns(3)
        with col1:
            if hy_spread and hy_spread.get('latest_value'):
                val = hy_spread['latest_value']
                st.metric("High Yield Spread", f"{val:.2f}%", "Elevated" if val > 5 else "Normal")
        with col2:
            if ig_spread and ig_spread.get('latest_value'):
                val = ig_spread['latest_value']
                st.metric("Investment Grade Spread", f"{val:.2f}%")
        with col3:
            real_rate = fetch_api("/api/indicators/DFII10/latest", silent=True)
            if real_rate and real_rate.get('latest_value'):
                st.metric("10Y Real Rate", f"{real_rate['latest_value']:.2f}%")

    # ============================================================================
    # SECTION 5: VOLATILITY & RISK SENTIMENT
    # ============================================================================
    st.divider()
    st.subheader("5. Volatility & Risk Sentiment")

    st.markdown("""
    **The VIX is the market's "fear gauge"**, derived from S&P 500 options prices. It represents expected annualized
    volatility over the next 30 days. A VIX of 20 implies the market expects the S&P 500 to move about 1.25% per day
    (20% / sqrt(252 trading days)). Below 15 indicates complacency; above 30 indicates fear; above 40 is panic.
    The VIX spiked to 82 during March 2020 (COVID crash) and 80 during October 2008 (financial crisis).

    **VIX term structure** is even more informative than the level. Normally, longer-dated VIX futures trade higher
    than short-dated ones (contango) - uncertainty increases with time. When short-term VIX exceeds long-term VIX
    (backwardation), it signals acute fear NOW. Persistent backwardation is rare and typically coincides with major
    market stress. Comparing VIX to VIX3M (3-month VIX) reveals this term structure.

    **Mean reversion** is the VIX's defining characteristic. Extremely high VIX readings often precede market bounces
    (fear is maximum at bottoms). Extremely low VIX readings can signal complacency before corrections (everyone's
    bullish, no one's hedging). The VIX doesn't predict direction, but it does indicate the market's current emotional
    state and the cost of portfolio protection. When VIX is high, puts are expensive (bad time to hedge); when VIX
    is low, puts are cheap (good time to add protection).
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**VIX (Fear Gauge)**")
        vix_data = fetch_api(f"/api/indicators/^VIX/timeseries?start={mkt_start_date.isoformat()}&limit=10000", silent=True)
        if not vix_data or not vix_data.get('data'):
            vix_data = fetch_api(f"/api/indicators/VIXCLS/timeseries?start={mkt_start_date.isoformat()}&limit=10000", silent=True)
        if vix_data and vix_data.get('data'):
            df = pd.DataFrame(vix_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                    fill='tozeroy', fillcolor='rgba(246, 173, 85, 0.15)',
                                    line=dict(color='#F6AD55', width=2), name='VIX'))
            fig.add_hline(y=20, line_dash="dash", line_color="#10b981", annotation_text="Normal (20)")
            fig.add_hline(y=30, line_dash="dash", line_color="#ef4444", annotation_text="Elevated (30)")
            fig.update_layout(title="VIX Volatility Index", xaxis_title="", yaxis_title="VIX Level",
                             template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
            st.plotly_chart(fig, use_container_width=True)

            current_vix = df.iloc[-1]['value']
            avg_vix = df['value'].mean()
            col1a, col2a = st.columns(2)
            with col1a:
                color = "normal" if current_vix < 25 else "inverse"
                st.metric("Current VIX", f"{current_vix:.1f}", f"Avg: {avg_vix:.1f}", delta_color=color)
            with col2a:
                if current_vix > 30:
                    st.error("Fear elevated - potential buying opportunity")
                elif current_vix < 15:
                    st.warning("Complacency - consider hedges")
                else:
                    st.success("Normal volatility regime")

    with col2:
        st.markdown("**Financial Conditions Index (NFCI)**")
        nfci_data = fetch_api(f"/api/indicators/NFCI/timeseries?start={mkt_start_date.isoformat()}&limit=10000", silent=True)
        if nfci_data and nfci_data.get('data'):
            df = pd.DataFrame(nfci_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                    fill='tozeroy', fillcolor='rgba(183, 148, 244, 0.15)',
                                    line=dict(color='#B794F4', width=2)))
            fig.add_hline(y=0, line_dash="dash", line_color="#E2E8F0", annotation_text="Neutral (0)")
            fig.update_layout(title="Chicago Fed Financial Conditions Index", xaxis_title="", yaxis_title="Index (0 = avg)",
                             template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
            st.plotly_chart(fig, use_container_width=True)

            current_nfci = df.iloc[-1]['value']
            if current_nfci > 0.5:
                st.error("Financial conditions tightening significantly")
            elif current_nfci > 0:
                st.warning("Financial conditions slightly tight")
            else:
                st.success("Financial conditions loose (supportive of risk)")
        else:
            st.info("Financial conditions data not available. Click 'Refresh FRED' to load.")

    # ============================================================================
    # SECTION 6: VALUATIONS
    # ============================================================================
    st.divider()
    st.subheader("6. Market Valuations")

    st.markdown("""
    **Valuations don't time the market, but they predict long-term returns.** High valuations (high P/E ratios)
    historically lead to lower 10-year returns, while low valuations lead to higher 10-year returns. The
    correlation is remarkably strong over long horizons but nearly useless over short horizons - expensive
    markets can get more expensive for years before reverting.

    **The Buffett Indicator** (total market cap / GDP) is Warren Buffett's favorite valuation metric. It compares
    the value of all publicly traded stocks to the size of the economy. Historically, readings above 150% have
    preceded poor returns, while readings below 80% have preceded strong returns. The indicator hit all-time
    highs in 2021 and remains elevated. Critics note that (1) more companies are public now, (2) US companies
    have significant foreign revenues, and (3) interest rates affect fair value.

    **The CAPE (Cyclically Adjusted P/E)**, or Shiller P/E, divides the S&P 500 price by average inflation-adjusted
    earnings over the past 10 years. This smooths out cyclical earnings fluctuations. Average CAPE is ~16-17;
    readings above 25 have historically signaled expensive markets. Current CAPE is ~32, among the highest
    in history outside of 2000's tech bubble. However, low interest rates justify higher P/E ratios (higher
    present value of future earnings), complicating the picture.
    """)

    # Buffett Indicator components
    col1, col2 = st.columns(2)

    with col1:
        # Use SPY as a proxy for total market (Wilshire 5000 was discontinued on FRED June 2024)
        spy_data = fetch_api(f"/api/indicators/SPY/timeseries?start={mkt_start_date.isoformat()}&limit=10000", silent=True)
        if spy_data and spy_data.get('data'):
            df = pd.DataFrame(spy_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                    fill='tozeroy', fillcolor='rgba(20, 184, 166, 0.15)',
                                    line=dict(color='#14b8a6', width=2)))
            fig.update_layout(title="S&P 500 (SPY) - Total Market Proxy", xaxis_title="", yaxis_title="Price ($)",
                             template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Market data not available. Click 'Refresh Market' to load.")

    with col2:
        gdp_data = fetch_api("/api/indicators/GDP/latest", silent=True)
        market_cap_data = fetch_api("/api/indicators/NCBEILQ027S/latest", silent=True)

        if gdp_data and gdp_data.get('latest_value') and market_cap_data and market_cap_data.get('latest_value'):
            gdp = gdp_data['latest_value']
            market_cap = market_cap_data['latest_value']
            buffett = (market_cap / gdp) * 100

            # Gauge-style display
            st.markdown("**Buffett Indicator (Market Cap / GDP)**")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=buffett,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Market Cap / GDP (%)"},
                gauge={
                    'axis': {'range': [None, 250]},
                    'bar': {'color': "#14b8a6"},
                    'steps': [
                        {'range': [0, 80], 'color': "#1A365D"},
                        {'range': [80, 120], 'color': "#2A4365"},
                        {'range': [120, 180], 'color': "#744210"},
                        {'range': [180, 250], 'color': "#742A2A"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 2},
                        'thickness': 0.75,
                        'value': 100
                    }
                }
            ))
            fig.update_layout(template='plotly_dark', height=300, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

            if buffett > 180:
                st.error(f"Buffett Indicator at {buffett:.0f}% - historically very expensive")
            elif buffett > 120:
                st.warning(f"Buffett Indicator at {buffett:.0f}% - above historical average")
            else:
                st.success(f"Buffett Indicator at {buffett:.0f}% - reasonable valuation")
        else:
            st.info("Buffett Indicator components not available.")

    # ============================================================================
    # SECTION 7: FLOWS & POSITIONING
    # ============================================================================
    st.divider()
    st.subheader("7. Flows & Market Positioning")

    st.markdown("""
    **"Don't fight the flows"** - tracking where money is moving provides insights into investor sentiment and
    potential market direction. Fund flows show whether investors are adding to or withdrawing from various
    asset classes. Heavy inflows into equity funds often coincide with late-stage bull markets (retail chasing
    performance), while heavy outflows can signal capitulation (potential bottoms).

    **Margin debt** is a powerful contrarian indicator. When investors borrow heavily against their portfolios
    to buy more stocks (high margin debt), it signals bullish excess - and creates forced-selling risk when
    markets decline (margin calls). Margin debt peaked before the 2000 and 2008 crashes. Rising margin debt
    in an uptrend confirms conviction; falling margin debt can be an early warning sign.

    **Positioning surveys** (AAII sentiment, fund manager surveys) capture what investors think rather than
    what they're doing. Extreme bullish readings are contrarian bearish (everyone who wants to buy has bought),
    while extreme bearish readings are contrarian bullish (maximum pessimism = potential bottom). The challenge
    is that sentiment can stay extreme longer than expected - it's better used as a risk indicator than a
    timing tool.
    """)

    margin_data = fetch_api(f"/api/indicators/BOGZ1FL663067003Q/timeseries?start={mkt_start_date.isoformat()}&limit=1000", silent=True)
    if margin_data and margin_data.get('data'):
        df = pd.DataFrame(margin_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value']/1000, mode='lines',
                                fill='tozeroy', fillcolor='rgba(139, 92, 246, 0.15)',
                                line=dict(color='#8b5cf6', width=2)))
        fig.update_layout(title="Margin Debt at Broker-Dealers ($Billions)", xaxis_title="", yaxis_title="$ Billions",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'))
        st.plotly_chart(fig, use_container_width=True)

        current = df.iloc[-1]['value']/1000
        peak = df['value'].max()/1000
        st.metric("Current Margin Debt", f"${current:.0f}B", f"Peak: ${peak:.0f}B")
    else:
        st.info("Margin debt data not available. Click 'Refresh FRED' to load BOGZ1FL663067003Q.")

    # ============================================================================
    # SECTION 8: COMMODITIES & ALTERNATIVES
    # ============================================================================
    st.divider()
    st.subheader("8. Commodities & Alternative Assets")

    st.markdown("""
    **Commodities provide diversification and inflation protection**, as they often move independently of stocks
    and bonds. Gold is the classic "safe haven" - it tends to rise during crises, currency debasement fears,
    and geopolitical uncertainty. It doesn't produce earnings or dividends, so it's valued based on sentiment,
    real interest rates (gold competes with bonds), and currency moves (priced in dollars, so gold rises when
    the dollar falls).

    **Oil prices** impact the economy directly through gas prices, transportation costs, and inflation. High
    oil prices act as a "tax" on consumers and hurt corporate margins. Oil spikes have preceded several
    recessions. However, for energy investors (XLE), high oil prices are bullish. The US shale revolution has
    made the US a net energy exporter, changing the economic impact of oil price moves.

    **Copper ("Dr. Copper")** is called that because its price is thought to have a "PhD in economics" - it's
    so widely used in construction and manufacturing that copper demand signals economic activity. Rising
    copper prices suggest economic expansion; falling copper prices suggest contraction. The copper/gold
    ratio is a risk-on/risk-off indicator: when copper outperforms gold, risk appetite is high.

    **Cryptocurrencies** have emerged as a distinct asset class with characteristics of both "digital gold"
    (store of value, inflation hedge) and high-growth tech investments (extreme volatility, narrative-driven).
    Bitcoin and Ethereum now have spot ETFs, bringing institutional legitimacy. Crypto tends to be highly
    correlated with risk appetite - it rallies when investors are bullish on growth and falls during risk-off.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Precious Metals & Commodities**")
        commodities = [("GLD", "Gold", "#FFD700"), ("SLV", "Silver", "#C0C0C0"), ("USO", "Oil", "#8b5cf6"), ("DBC", "Commodities", "#F6AD55")]
        fig = go.Figure()
        for ticker, name, color in commodities:
            ret, df = get_return(ticker)
            if df is not None:
                df['normalized'] = (df['value'] / df.iloc[0]['value']) * 100
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['normalized'],
                                        name=f"{name} {ret:+.1f}%" if ret else name,
                                        line=dict(color=color, width=2)))
        fig.update_layout(title="Commodities Performance", xaxis_title="", yaxis_title="Indexed (Start=100)",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Crypto & Real Estate**")
        alts = [("BTC-USD", "Bitcoin", "#F7931A"), ("ETH-USD", "Ethereum", "#627EEA"), ("VNQ", "REITs", "#14b8a6")]
        fig = go.Figure()
        for ticker, name, color in alts:
            ret, df = get_return(ticker)
            if df is not None:
                df['normalized'] = (df['value'] / df.iloc[0]['value']) * 100
                fig.add_trace(go.Scatter(x=df['timestamp'], y=df['normalized'],
                                        name=f"{name} {ret:+.1f}%" if ret else name,
                                        line=dict(color=color, width=2)))
        fig.update_layout(title="Crypto & Real Assets", xaxis_title="", yaxis_title="Indexed (Start=100)",
                         template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

    # ============================================================================
    # SECTION 9: CROSS-ASSET CORRELATIONS
    # ============================================================================
    st.divider()
    st.subheader("9. Cross-Asset Correlations")

    st.markdown("""
    **Correlations between asset classes determine portfolio diversification benefits.** The classic 60/40
    portfolio (60% stocks, 40% bonds) relies on stocks and bonds being negatively correlated - when stocks
    fall, bonds rise, cushioning losses. This relationship held for decades but broke down in 2022 when both
    stocks AND bonds fell sharply together, delivering the worst 60/40 performance since the 1970s.

    **The stock-bond correlation** is regime-dependent. In low-inflation environments (1990s-2020), the
    correlation was negative - bonds acted as portfolio insurance. In high-inflation environments (1970s,
    2022+), the correlation can turn positive - rising inflation hurts both stocks (higher discount rates)
    and bonds (higher yields = lower prices). Understanding the current correlation regime is critical for
    portfolio construction.

    **Dollar correlations** matter for international investors. When the dollar strengthens, international
    investments lose value for US investors even if local prices are flat. Risk assets (stocks, high-yield
    bonds, commodities) often have negative correlations with the dollar - a weaker dollar is generally
    bullish for risk assets. Gold has a historically negative correlation with real interest rates - when
    real rates fall, gold tends to rise.
    """)

    # Calculate rolling correlations
    spy_ret, spy_df = get_return("SPY")
    tlt_ret, tlt_df = get_return("TLT")

    if spy_df is not None and tlt_df is not None:
        # Merge on date and calculate correlation
        spy_df['date'] = spy_df['timestamp'].dt.date
        tlt_df['date'] = tlt_df['timestamp'].dt.date
        merged = pd.merge(spy_df[['date', 'value']], tlt_df[['date', 'value']], on='date', suffixes=('_spy', '_tlt'))
        merged['spy_ret'] = merged['value_spy'].pct_change()
        merged['tlt_ret'] = merged['value_tlt'].pct_change()

        # Rolling 60-day correlation
        merged['correlation'] = merged['spy_ret'].rolling(60).corr(merged['tlt_ret'])
        merged = merged.dropna()

        if len(merged) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pd.to_datetime(merged['date']), y=merged['correlation'],
                                    mode='lines', fill='tozeroy',
                                    fillcolor='rgba(183, 148, 244, 0.15)',
                                    line=dict(color='#B794F4', width=2)))
            fig.add_hline(y=0, line_dash="dash", line_color="#E2E8F0", annotation_text="Uncorrelated")
            fig.update_layout(title="Stock-Bond Correlation (SPY vs TLT, 60-day rolling)",
                             xaxis_title="", yaxis_title="Correlation",
                             template='plotly_dark', height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748', range=[-1, 1]))
            st.plotly_chart(fig, use_container_width=True)

            current_corr = merged['correlation'].iloc[-1]
            avg_corr = merged['correlation'].mean()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Current Stock-Bond Correlation", f"{current_corr:.2f}",
                         "Positive (diversification reduced)" if current_corr > 0.2 else "Negative (diversification working)")
            with col2:
                if current_corr > 0.3:
                    st.warning("Bonds not providing diversification - consider alternatives")
                elif current_corr < -0.3:
                    st.success("Strong negative correlation - 60/40 portfolio benefits")
                else:
                    st.info("Neutral correlation regime")

    # ============================================================================
    # SECTION 10: TECHNICAL INDICATORS
    # ============================================================================
    st.divider()
    st.subheader("10. Technical Indicators")

    st.markdown("""
    **Technical analysis** studies price and volume patterns to forecast future price movements. While
    fundamentalists scoff at "reading tea leaves," technicals provide useful information about supply/demand
    dynamics and investor behavior. The most widely-watched technical levels become self-fulfilling as
    millions of traders watch and act on them.

    **Moving averages** smooth price data to identify trends. The 200-day moving average is the most important
    long-term trend indicator. When price is above the 200-day MA, the trend is considered bullish; below it,
    bearish. The "golden cross" (50-day MA crossing above 200-day MA) is a bullish signal; the "death cross"
    (50-day crossing below) is bearish. These signals lag but have historically filtered out noise.

    **Support and resistance** levels form where prices have historically reversed. Prior highs become
    resistance (sellers remember they should have sold there); prior lows become support (buyers remember
    it was a good entry). Round numbers (e.g., S&P 500 at 5,000) act as psychological support/resistance.
    Breakouts above resistance or breakdowns below support often lead to continuation moves as stops are
    triggered and momentum traders pile in.
    """)

    # S&P 500 with moving averages
    spy_long = fetch_api(f"/api/indicators/SPY/timeseries?start={(datetime.now() - timedelta(days=500)).isoformat()}&limit=10000", silent=True)
    if spy_long and spy_long.get('data') and len(spy_long['data']) > 200:
        df = pd.DataFrame(spy_long['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        df['MA50'] = df['value'].rolling(50).mean()
        df['MA200'] = df['value'].rolling(200).mean()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['value'], mode='lines',
                                name='SPY', line=dict(color='#14b8a6', width=2)))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['MA50'], mode='lines',
                                name='50-Day MA', line=dict(color='#F6AD55', width=1.5, dash='dash')))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['MA200'], mode='lines',
                                name='200-Day MA', line=dict(color='#ef4444', width=1.5, dash='dash')))
        fig.update_layout(title="S&P 500 (SPY) with Moving Averages", xaxis_title="", yaxis_title="Price ($)",
                         template='plotly_dark', height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(gridcolor='#2D3748'), yaxis=dict(gridcolor='#2D3748'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        # Technical signals
        current_price = df.iloc[-1]['value']
        ma50 = df.iloc[-1]['MA50']
        ma200 = df.iloc[-1]['MA200']

        col1, col2, col3 = st.columns(3)
        with col1:
            pct_above_200 = ((current_price - ma200) / ma200) * 100
            st.metric("Price vs 200-Day MA", f"{pct_above_200:+.1f}%",
                     "Above (Bullish)" if pct_above_200 > 0 else "Below (Bearish)")
        with col2:
            if ma50 > ma200:
                st.success("Golden Cross (50 > 200) - Bullish")
            else:
                st.error("Death Cross (50 < 200) - Bearish")
        with col3:
            # RSI calculation
            delta = df['value'].diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            current_rsi = rsi.iloc[-1]
            st.metric("14-Day RSI", f"{current_rsi:.0f}",
                     "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral")
    else:
        st.info("Insufficient historical data for technical analysis.")

# Page: Credit Spreads
elif page == "Credit Spreads":
    st.header("💳 Credit Spreads & Bond Market Stress")

    st.markdown("""
    ### Understanding Credit Spreads

    Credit spreads measure the difference in yield between corporate bonds and "risk-free" Treasury bonds of similar
    maturity. When investors demand higher yields to hold corporate debt relative to Treasuries, spreads widen - this
    signals increased concern about default risk and economic stress. Credit markets often lead equity markets in
    signaling trouble because bond investors tend to be more risk-aware and have priority claims in bankruptcy.

    **High Yield (Junk) Spreads** are particularly important because these bonds are issued by companies with weaker
    balance sheets. When spreads blow out (widen dramatically), it often indicates financial stress is spreading
    through the economy. The 2008 crisis saw high yield spreads exceed 20%; COVID briefly pushed them above 10%.

    **Investment Grade Spreads** track higher-quality corporate debt. These widen less dramatically but still provide
    important signals about corporate borrowing conditions and overall financial market stress.

    *The spread data below uses ICE BofA indices, the industry standard for tracking credit market conditions.*
    """)

    # Key credit spread indicators
    # ICE BofA US High Yield Index Option-Adjusted Spread
    # ICE BofA US Corporate Index Option-Adjusted Spread
    # BAA-AAA spread for corporate quality

    col1, col2, col3, col4 = st.columns(4)

    # High Yield Spread
    hy_spread = fetch_api("/api/indicators/BAMLH0A0HYM2/latest", silent=True)
    if hy_spread and hy_spread.get('latest_value') is not None:
        val = hy_spread['latest_value']
        with col1:
            delta_str = "Elevated" if val > 5 else "Normal" if val < 4 else "Moderate"
            st.metric("High Yield Spread", f"{val:.2f}%", delta=delta_str,
                     delta_color="inverse" if val > 5 else "normal")

    # Investment Grade Spread
    ig_spread = fetch_api("/api/indicators/BAMLC0A0CM/latest", silent=True)
    if ig_spread and ig_spread.get('latest_value') is not None:
        val = ig_spread['latest_value']
        with col2:
            st.metric("Investment Grade Spread", f"{val:.2f}%")

    # BAA Corporate Bond Yield
    baa_yield = fetch_api("/api/indicators/DBAA/latest", silent=True)
    if baa_yield and baa_yield.get('latest_value') is not None:
        with col3:
            st.metric("BAA Corporate Yield", f"{baa_yield['latest_value']:.2f}%")

    # AAA Corporate Bond Yield
    aaa_yield = fetch_api("/api/indicators/DAAA/latest", silent=True)
    if aaa_yield and aaa_yield.get('latest_value') is not None:
        with col4:
            st.metric("AAA Corporate Yield", f"{aaa_yield['latest_value']:.2f}%")

    st.divider()

    # Historical High Yield Spread
    st.subheader("High Yield Spread History")
    time_range = st.selectbox("Time Range", ["1 Year", "5 Years", "10 Years", "20 Years", "Max"], index=2, key="credit_range")
    days_map = {"1 Year": 365, "5 Years": 1825, "10 Years": 3650, "20 Years": 7300, "Max": 15000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    hy_data = fetch_api(f"/api/indicators/BAMLH0A0HYM2/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
    ig_data = fetch_api(f"/api/indicators/BAMLC0A0CM/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)

    if hy_data and hy_data.get('data'):
        fig = go.Figure()

        # High Yield spread
        hy_df = pd.DataFrame(hy_data['data'])
        hy_df['timestamp'] = pd.to_datetime(hy_df['timestamp'])
        fig.add_trace(go.Scatter(
            x=hy_df['timestamp'], y=hy_df['value'],
            name='High Yield Spread', line=dict(color='#ef4444', width=2),
            fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.1)'
        ))

        # Investment Grade spread
        if ig_data and ig_data.get('data'):
            ig_df = pd.DataFrame(ig_data['data'])
            ig_df['timestamp'] = pd.to_datetime(ig_df['timestamp'])
            fig.add_trace(go.Scatter(
                x=ig_df['timestamp'], y=ig_df['value'],
                name='Investment Grade Spread', line=dict(color='#14b8a6', width=2)
            ))

        # Add stress threshold lines
        fig.add_hline(y=5, line_dash="dash", line_color="yellow",
                     annotation_text="Stress Level (5%)", annotation_position="right")
        fig.add_hline(y=8, line_dash="dash", line_color="red",
                     annotation_text="Crisis Level (8%)", annotation_position="right")

        fig.update_layout(
            title="Credit Spreads Over Time",
            yaxis_title="Spread (%)",
            height=500,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig, use_container_width=True)

    # BAA-AAA Spread (credit quality indicator)
    st.subheader("BAA-AAA Spread (Credit Quality Indicator)")
    st.markdown("""
    The spread between BAA (lowest investment grade) and AAA (highest quality) corporate bonds measures
    how much extra yield investors demand for taking on additional credit risk within investment grade.
    Widening suggests flight to quality even within the corporate bond market.
    """)

    baa_data = fetch_api(f"/api/indicators/DBAA/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
    aaa_data = fetch_api(f"/api/indicators/DAAA/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)

    if baa_data and baa_data.get('data') and aaa_data and aaa_data.get('data'):
        baa_df = pd.DataFrame(baa_data['data'])
        aaa_df = pd.DataFrame(aaa_data['data'])
        baa_df['timestamp'] = pd.to_datetime(baa_df['timestamp'])
        aaa_df['timestamp'] = pd.to_datetime(aaa_df['timestamp'])

        # Merge and calculate spread
        merged = pd.merge(baa_df, aaa_df, on='timestamp', suffixes=('_baa', '_aaa'))
        merged['spread'] = merged['value_baa'] - merged['value_aaa']

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=merged['timestamp'], y=merged['spread'],
            name='BAA-AAA Spread', line=dict(color='#9F7AEA', width=2),
            fill='tozeroy', fillcolor='rgba(159, 122, 234, 0.1)'
        ))
        fig2.update_layout(
            title="BAA-AAA Corporate Bond Spread",
            yaxis_title="Spread (%)",
            height=400,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig2, use_container_width=True)

# Page: Currency Monitor
elif page == "Currency Monitor":
    st.header("💱 Currency & Dollar Monitor")

    st.markdown("""
    ### The Dollar's Role in Global Markets

    The U.S. Dollar is the world's reserve currency, and its strength or weakness ripples through every asset class.
    A strong dollar makes U.S. exports more expensive (hurting multinationals), reduces the dollar value of overseas
    earnings, puts pressure on emerging markets with dollar-denominated debt, and typically correlates with lower
    commodity prices (since most commodities are priced in dollars).

    **DXY (Dollar Index)** measures the dollar against a basket of six major currencies (EUR, JPY, GBP, CAD, SEK, CHF),
    with the Euro comprising about 57% of the weight. It's the most widely watched measure of overall dollar strength.

    **Key relationships to watch:**
    - Dollar strength often coincides with risk-off environments (flight to safety)
    - The Yen traditionally strengthens during market stress (safe haven currency)
    - Emerging market currencies weaken when the dollar strengthens, potentially causing EM debt stress
    """)

    # Currency pairs using Yahoo Finance symbols
    currencies = [
        ("DX-Y.NYB", "DXY Index", "Dollar Index"),
        ("EURUSD=X", "EUR/USD", "Euro"),
        ("JPY=X", "USD/JPY", "Japanese Yen"),
        ("GBPUSD=X", "GBP/USD", "British Pound"),
        ("CNY=X", "USD/CNY", "Chinese Yuan"),
        ("AUDUSD=X", "AUD/USD", "Australian Dollar"),
    ]

    # Display current values
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3]

    for i, (symbol, label, name) in enumerate(currencies):
        data = fetch_api(f"/api/indicators/{symbol}/latest", silent=True)
        if data and data.get('latest_value') is not None:
            with cols[i]:
                st.metric(label, f"{data['latest_value']:.4f}" if 'USD' in label else f"{data['latest_value']:.2f}")

    st.divider()

    # DXY Historical Chart
    st.subheader("Dollar Index (DXY) History")
    time_range = st.selectbox("Time Range", ["1 Year", "5 Years", "10 Years", "Max"], index=1, key="fx_range")
    days_map = {"1 Year": 365, "5 Years": 1825, "10 Years": 3650, "Max": 10000}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    dxy_data = fetch_api(f"/api/indicators/DX-Y.NYB/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)

    if dxy_data and dxy_data.get('data'):
        df = pd.DataFrame(dxy_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['value'],
            name='DXY', line=dict(color='#14b8a6', width=2),
            fill='tozeroy', fillcolor='rgba(20, 184, 166, 0.1)'
        ))

        # Add reference lines
        fig.add_hline(y=100, line_dash="dash", line_color="gray",
                     annotation_text="100 (Baseline)", annotation_position="right")

        fig.update_layout(
            title="U.S. Dollar Index (DXY)",
            yaxis_title="Index Value",
            height=450,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig, use_container_width=True)

    # Multi-currency comparison
    st.subheader("Major Currency Pairs")

    fig2 = go.Figure()
    colors = ['#14b8a6', '#8b5cf6', '#ef4444', '#F6AD55', '#9F7AEA']

    for i, (symbol, label, name) in enumerate(currencies[1:]):  # Skip DXY
        data = fetch_api(f"/api/indicators/{symbol}/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
        if data and data.get('data'):
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            # Normalize to percentage change from start
            df['normalized'] = (df['value'] / df['value'].iloc[0] - 1) * 100
            fig2.add_trace(go.Scatter(
                x=df['timestamp'], y=df['normalized'],
                name=label, line=dict(color=colors[i % len(colors)], width=2)
            ))

    fig2.add_hline(y=0, line_dash="dash", line_color="gray")
    fig2.update_layout(
        title="Currency Performance (% Change from Start)",
        yaxis_title="% Change",
        height=450,
        **PLOTLY_LAYOUT_DEFAULTS
    )
    st.plotly_chart(fig2, use_container_width=True)

# Page: Commodities
elif page == "Commodities":
    st.header("🛢️ Commodities Dashboard")

    st.markdown("""
    ### Commodities as Economic Indicators

    Commodity prices provide real-time signals about global economic activity, inflation expectations, and supply/demand
    dynamics. Unlike financial assets, commodities are physical goods consumed in production and daily life, making
    their prices directly reflect real economic conditions.

    **Key Commodities:**
    - **Crude Oil (WTI/Brent):** The lifeblood of the global economy. Oil prices affect transportation costs, manufacturing
      inputs, and consumer spending through gasoline prices. High oil prices act as a tax on consumers.
    - **Gold:** The ultimate safe haven and inflation hedge. Gold typically rises during uncertainty, real rate declines,
      and dollar weakness. The gold/silver ratio can signal risk sentiment.
    - **Copper ("Dr. Copper"):** Called the metal with a PhD in economics because its price closely tracks industrial
      activity. Copper is used in construction, electronics, and manufacturing - rising prices signal growth.
    - **Natural Gas:** Critical for heating and electricity generation. Highly seasonal and weather-dependent.

    **Copper/Gold Ratio:** A rising ratio suggests economic optimism (cyclical copper outperforming defensive gold);
    a falling ratio suggests risk aversion and growth concerns.
    """)

    # Commodity symbols
    commodities = [
        ("CL=F", "Crude Oil (WTI)", "$/barrel"),
        ("GC=F", "Gold", "$/oz"),
        ("SI=F", "Silver", "$/oz"),
        ("HG=F", "Copper", "$/lb"),
        ("NG=F", "Natural Gas", "$/MMBtu"),
        ("ZC=F", "Corn", "cents/bu"),
    ]

    # Display current prices
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3]

    commodity_values = {}
    for i, (symbol, name, unit) in enumerate(commodities):
        data = fetch_api(f"/api/indicators/{symbol}/latest", silent=True)
        if data and data.get('latest_value') is not None:
            commodity_values[symbol] = data['latest_value']
            with cols[i]:
                st.metric(name, f"${data['latest_value']:,.2f}", help=unit)

    st.divider()

    # Time range selector
    st.subheader("Commodity Price History")
    time_range = st.selectbox("Time Range", ["1 Year", "3 Years", "5 Years", "10 Years"], index=1, key="commodity_range")
    days_map = {"1 Year": 365, "3 Years": 1095, "5 Years": 1825, "10 Years": 3650}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    # Oil chart
    oil_data = fetch_api(f"/api/indicators/CL=F/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
    if oil_data and oil_data.get('data'):
        df = pd.DataFrame(oil_data['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['value'],
            name='WTI Crude', line=dict(color='#F6AD55', width=2),
            fill='tozeroy', fillcolor='rgba(246, 173, 85, 0.1)'
        ))
        fig.update_layout(
            title="Crude Oil (WTI)",
            yaxis_title="$/barrel",
            height=400,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig, use_container_width=True)

    # Gold and Copper comparison
    col1, col2 = st.columns(2)

    with col1:
        gold_data = fetch_api(f"/api/indicators/GC=F/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
        if gold_data and gold_data.get('data'):
            df = pd.DataFrame(gold_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df['value'],
                name='Gold', line=dict(color='#FFD700', width=2),
                fill='tozeroy', fillcolor='rgba(255, 215, 0, 0.1)'
            ))
            fig.update_layout(title="Gold", yaxis_title="$/oz", height=350, **PLOTLY_LAYOUT_DEFAULTS)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        copper_data = fetch_api(f"/api/indicators/HG=F/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
        if copper_data and copper_data.get('data'):
            df = pd.DataFrame(copper_data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df['value'],
                name='Copper', line=dict(color='#B87333', width=2),
                fill='tozeroy', fillcolor='rgba(184, 115, 51, 0.1)'
            ))
            fig.update_layout(title="Copper", yaxis_title="$/lb", height=350, **PLOTLY_LAYOUT_DEFAULTS)
            st.plotly_chart(fig, use_container_width=True)

    # Copper/Gold Ratio
    st.subheader("Copper/Gold Ratio (Economic Sentiment)")
    if gold_data and gold_data.get('data') and copper_data and copper_data.get('data'):
        gold_df = pd.DataFrame(gold_data['data'])
        copper_df = pd.DataFrame(copper_data['data'])
        gold_df['timestamp'] = pd.to_datetime(gold_df['timestamp'])
        copper_df['timestamp'] = pd.to_datetime(copper_df['timestamp'])

        merged = pd.merge(copper_df, gold_df, on='timestamp', suffixes=('_copper', '_gold'))
        # Ratio: copper price * 1000 / gold price (scale for readability)
        merged['ratio'] = (merged['value_copper'] * 1000) / merged['value_gold']

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=merged['timestamp'], y=merged['ratio'],
            name='Copper/Gold Ratio', line=dict(color='#14b8a6', width=2),
            fill='tozeroy', fillcolor='rgba(20, 184, 166, 0.1)'
        ))
        fig.update_layout(
            title="Copper/Gold Ratio (Higher = More Optimistic)",
            yaxis_title="Ratio",
            height=400,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig, use_container_width=True)

# Page: Global Markets
elif page == "Global Markets":
    st.header("🌍 Global Markets Comparison")

    st.markdown("""
    ### Diversification Beyond U.S. Borders

    While U.S. markets have dominated returns over the past decade, global diversification remains important for
    risk management and capturing opportunities in different economic cycles. International markets can outperform
    for extended periods - European and emerging markets led in the 2000s while the U.S. lagged.

    **Key Comparisons:**
    - **US vs. International Developed (EFA):** Europe, Japan, Australia - mature economies with different sector exposures
    - **US vs. Emerging Markets (EEM):** China, India, Brazil, etc. - higher growth potential but more volatility
    - **Developed vs. Emerging:** Relative performance indicates global risk appetite

    **Why EM Matters:** Emerging markets are sensitive to dollar strength, commodity prices, and global growth.
    When the dollar weakens and growth is strong, EM often outperforms significantly.
    """)

    # Global market ETFs
    markets = [
        ("SPY", "S&P 500 (US)", "#14b8a6"),
        ("EFA", "Developed Int'l (EAFE)", "#8b5cf6"),
        ("EEM", "Emerging Markets", "#ef4444"),
        ("VGK", "Europe (VGK)", "#F6AD55"),
        ("EWJ", "Japan (EWJ)", "#9F7AEA"),
        ("FXI", "China (FXI)", "#ED64A6"),
    ]

    # Current values
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3, col1, col2, col3]

    for i, (symbol, name, color) in enumerate(markets):
        data = fetch_api(f"/api/indicators/{symbol}/latest", silent=True)
        if data and data.get('latest_value') is not None:
            with cols[i]:
                st.metric(name, f"${data['latest_value']:.2f}")

    st.divider()

    # Time range selector
    st.subheader("Relative Performance")
    time_range = st.selectbox("Time Range", ["YTD", "1 Year", "3 Years", "5 Years", "10 Years"], index=2, key="global_range")

    if time_range == "YTD":
        start_date = datetime(datetime.now().year, 1, 1)
    else:
        days_map = {"1 Year": 365, "3 Years": 1095, "5 Years": 1825, "10 Years": 3650}
        start_date = datetime.now() - timedelta(days=days_map[time_range])

    # Normalized performance chart
    fig = go.Figure()

    for symbol, name, color in markets:
        data = fetch_api(f"/api/indicators/{symbol}/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
        if data and data.get('data'):
            df = pd.DataFrame(data['data'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            # Normalize to percentage change from start
            df['normalized'] = (df['value'] / df['value'].iloc[0] - 1) * 100
            fig.add_trace(go.Scatter(
                x=df['timestamp'], y=df['normalized'],
                name=name, line=dict(color=color, width=2)
            ))

    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(
        title=f"Global Market Performance ({time_range})",
        yaxis_title="% Return",
        height=500,
        **PLOTLY_LAYOUT_DEFAULTS
    )
    st.plotly_chart(fig, use_container_width=True)

    # US vs International ratio
    st.subheader("US vs. International Relative Strength")

    spy_data = fetch_api(f"/api/indicators/SPY/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
    efa_data = fetch_api(f"/api/indicators/EFA/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)
    eem_data = fetch_api(f"/api/indicators/EEM/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)

    if spy_data and efa_data and spy_data.get('data') and efa_data.get('data'):
        spy_df = pd.DataFrame(spy_data['data'])
        efa_df = pd.DataFrame(efa_data['data'])
        spy_df['timestamp'] = pd.to_datetime(spy_df['timestamp'])
        efa_df['timestamp'] = pd.to_datetime(efa_df['timestamp'])

        merged = pd.merge(spy_df, efa_df, on='timestamp', suffixes=('_spy', '_efa'))
        merged['us_vs_intl'] = merged['value_spy'] / merged['value_efa']
        # Normalize
        merged['us_vs_intl_norm'] = (merged['us_vs_intl'] / merged['us_vs_intl'].iloc[0] - 1) * 100

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=merged['timestamp'], y=merged['us_vs_intl_norm'],
            name='US vs Developed Int\'l', line=dict(color='#14b8a6', width=2),
            fill='tozeroy', fillcolor='rgba(20, 184, 166, 0.1)'
        ))

        if eem_data and eem_data.get('data'):
            eem_df = pd.DataFrame(eem_data['data'])
            eem_df['timestamp'] = pd.to_datetime(eem_df['timestamp'])
            merged2 = pd.merge(spy_df, eem_df, on='timestamp', suffixes=('_spy', '_eem'))
            merged2['us_vs_em'] = merged2['value_spy'] / merged2['value_eem']
            merged2['us_vs_em_norm'] = (merged2['us_vs_em'] / merged2['us_vs_em'].iloc[0] - 1) * 100
            fig2.add_trace(go.Scatter(
                x=merged2['timestamp'], y=merged2['us_vs_em_norm'],
                name='US vs Emerging', line=dict(color='#ef4444', width=2)
            ))

        fig2.add_hline(y=0, line_dash="dash", line_color="gray")
        fig2.update_layout(
            title="US Outperformance vs International (Rising = US Winning)",
            yaxis_title="Relative Performance (%)",
            height=400,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig2, use_container_width=True)

# Page: Sentiment
elif page == "Sentiment":
    st.header("📊 Sentiment & Positioning")

    st.markdown("""
    ### Measuring Market Psychology

    Sentiment indicators gauge investor psychology and can serve as contrarian signals. When everyone is bullish,
    there may be no one left to buy. When everyone is bearish, the market may be oversold. These indicators are
    most useful at extremes - moderate readings are less actionable.

    **Key Indicators:**
    - **VIX (Fear Index):** Measures expected S&P 500 volatility. Spikes during fear, low during complacency.
      Readings above 30 often mark market bottoms; below 15 can signal complacency.
    - **VIX Term Structure:** When near-term VIX exceeds longer-term (backwardation), it signals acute fear.
      Normal markets show contango (upward slope).
    - **Put/Call Ratio:** High readings (>1.0) indicate bearishness and potential contrarian buy signal.
      Low readings (<0.7) indicate complacency.

    *Remember: Sentiment indicators work best as contrarian signals at extremes. Markets can stay irrational
    longer than you can stay solvent - don't use these alone.*
    """)

    # Key sentiment indicators
    col1, col2, col3, col4 = st.columns(4)

    # VIX
    vix_data = fetch_api("/api/indicators/^VIX/latest", silent=True)
    if vix_data and vix_data.get('latest_value') is not None:
        vix_val = vix_data['latest_value']
        with col1:
            if vix_val > 30:
                sentiment = "Fear"
                color = "inverse"
            elif vix_val < 15:
                sentiment = "Complacent"
                color = "off"
            else:
                sentiment = "Normal"
                color = "normal"
            st.metric("VIX", f"{vix_val:.2f}", delta=sentiment, delta_color=color)

    # VIX3M (3-month VIX)
    vix3m_data = fetch_api("/api/indicators/^VIX3M/latest", silent=True)
    if vix3m_data and vix3m_data.get('latest_value') is not None:
        with col2:
            st.metric("VIX 3-Month", f"{vix3m_data['latest_value']:.2f}")

    # Term structure
    if vix_data and vix3m_data and vix_data.get('latest_value') and vix3m_data.get('latest_value'):
        term_spread = vix3m_data['latest_value'] - vix_data['latest_value']
        with col3:
            structure = "Contango" if term_spread > 0 else "Backwardation"
            st.metric("VIX Term Spread", f"{term_spread:.2f}", delta=structure,
                     delta_color="normal" if term_spread > 0 else "inverse")

    # Put/Call ratio (CBOE equity)
    pcr_data = fetch_api("/api/indicators/PCEQUITY/latest", silent=True)
    if pcr_data and pcr_data.get('latest_value') is not None:
        pcr_val = pcr_data['latest_value']
        with col4:
            if pcr_val > 1.0:
                pcr_signal = "Bearish"
            elif pcr_val < 0.7:
                pcr_signal = "Bullish"
            else:
                pcr_signal = "Neutral"
            st.metric("Put/Call Ratio", f"{pcr_val:.2f}", delta=pcr_signal)

    st.divider()

    # VIX Historical
    st.subheader("VIX History")
    time_range = st.selectbox("Time Range", ["1 Year", "3 Years", "5 Years", "10 Years"], index=1, key="sentiment_range")
    days_map = {"1 Year": 365, "3 Years": 1095, "5 Years": 1825, "10 Years": 3650}
    start_date = datetime.now() - timedelta(days=days_map[time_range])

    vix_history = fetch_api(f"/api/indicators/^VIX/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)

    if vix_history and vix_history.get('data'):
        df = pd.DataFrame(vix_history['data'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['timestamp'], y=df['value'],
            name='VIX', line=dict(color='#ef4444', width=2),
            fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.1)'
        ))

        # Add threshold lines
        fig.add_hline(y=30, line_dash="dash", line_color="red",
                     annotation_text="Fear (30)", annotation_position="right")
        fig.add_hline(y=20, line_dash="dash", line_color="yellow",
                     annotation_text="Elevated (20)", annotation_position="right")
        fig.add_hline(y=15, line_dash="dash", line_color="green",
                     annotation_text="Complacent (15)", annotation_position="right")

        fig.update_layout(
            title="VIX - Volatility Index",
            yaxis_title="VIX Level",
            height=450,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig, use_container_width=True)

    # VIX Term Structure Chart
    st.subheader("VIX Term Structure Over Time")

    vix3m_history = fetch_api(f"/api/indicators/^VIX3M/timeseries?start={start_date.isoformat()}&limit=10000", silent=True)

    if vix_history and vix3m_history and vix_history.get('data') and vix3m_history.get('data'):
        vix_df = pd.DataFrame(vix_history['data'])
        vix3m_df = pd.DataFrame(vix3m_history['data'])
        vix_df['timestamp'] = pd.to_datetime(vix_df['timestamp'])
        vix3m_df['timestamp'] = pd.to_datetime(vix3m_df['timestamp'])

        merged = pd.merge(vix_df, vix3m_df, on='timestamp', suffixes=('_vix', '_vix3m'))
        merged['term_spread'] = merged['value_vix3m'] - merged['value_vix']

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=merged['timestamp'], y=merged['term_spread'],
            name='VIX Term Spread (3M - Spot)', line=dict(color='#9F7AEA', width=2),
            fill='tozeroy', fillcolor='rgba(159, 122, 234, 0.1)'
        ))
        fig2.add_hline(y=0, line_dash="dash", line_color="red",
                      annotation_text="Backwardation Below", annotation_position="right")

        fig2.update_layout(
            title="VIX Term Structure (Positive = Contango, Negative = Backwardation)",
            yaxis_title="Spread",
            height=400,
            **PLOTLY_LAYOUT_DEFAULTS
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Fear & Greed conceptual section
    st.subheader("Interpreting Sentiment Extremes")
    st.markdown("""
    | Indicator | Extreme Fear | Neutral | Extreme Greed |
    |-----------|--------------|---------|---------------|
    | VIX | > 30 | 15-25 | < 15 |
    | Put/Call Ratio | > 1.0 | 0.7-1.0 | < 0.7 |
    | VIX Term Structure | Backwardation | Flat | Steep Contango |

    **Contrarian Signals:**
    - Extreme fear often marks buying opportunities (but can persist)
    - Extreme greed suggests caution (but markets can stay complacent)
    - Best used in combination with price action and fundamentals
    """)

# Page: Custom Analysis
elif page == "Custom Analysis":
    st.header("🔍 Custom Analysis")
    st.markdown("Analyze and compare multiple indicators")

    # Get all indicators
    all_indicators = fetch_api("/api/indicators")

    if all_indicators:
        # Create mappings
        indicator_options = {
            f"{ind['name']} ({ind['indicator_id']})": ind['indicator_id']
            for ind in all_indicators
        }
        indicator_metadata = {ind['indicator_id']: ind for ind in all_indicators}

        # Multi-select for indicators
        selected_names = st.multiselect(
            "Select Indicators (up to 5)",
            options=list(indicator_options.keys()),
            default=[list(indicator_options.keys())[0]],
            max_selections=5
        )

        if not selected_names:
            st.warning("Please select at least one indicator")
        else:
            selected_ids = [indicator_options[name] for name in selected_names]

            # Options row
            col1, col2, col3 = st.columns(3)
            with col1:
                years_back = st.slider("Years of History", 1, 30, 5)
            with col2:
                normalize = st.checkbox("Normalize (% change from start)", value=len(selected_ids) > 1)
            with col3:
                y_axis_zero = st.checkbox("Y-axis starts at 0", value=False)

            start_date = datetime.now() - timedelta(days=365 * years_back)

            # Fetch data for all selected indicators (with high limit for long history)
            datasets = {}
            for sel_id in selected_ids:
                data = fetch_api(f"/api/indicators/{sel_id}/timeseries?start={start_date.isoformat()}&limit=20000", silent=True)
                if data and data.get('data'):
                    df = pd.DataFrame(data['data'])
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df.sort_values('timestamp')
                    datasets[sel_id] = {
                        'data': df,
                        'name': data['name'],
                        'metadata': indicator_metadata.get(sel_id, {})
                    }

            if datasets:
                # Create comparison chart
                fig = go.Figure()
                # Vibrant colors for dark theme
                colors = ['#14b8a6', '#8b5cf6', '#F6AD55', '#ef4444', '#B794F4']

                for i, (sel_id, dataset) in enumerate(datasets.items()):
                    df = dataset['data']
                    name = dataset['name']

                    if normalize and len(df) > 0:
                        # Normalize to percentage change from first value
                        first_val = df.iloc[0]['value']
                        if first_val != 0:
                            y_values = ((df['value'] - first_val) / abs(first_val)) * 100
                            y_label = "% Change from Start"
                        else:
                            y_values = df['value']
                            y_label = "Value"
                    else:
                        y_values = df['value']
                        y_label = "Value"

                    fig.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=y_values,
                        mode='lines',
                        name=name,
                        line=dict(color=colors[i % len(colors)], width=2)
                    ))

                # Update layout with dark theme
                layout_opts = {
                    'xaxis_title': "Date",
                    'yaxis_title': "% Change" if normalize else "Value",
                    'hovermode': 'x unified',
                    'template': 'plotly_dark',
                    'height': 500,
                    'legend': dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    'paper_bgcolor': 'rgba(0,0,0,0)',
                    'plot_bgcolor': 'rgba(0,0,0,0)',
                    'xaxis': dict(gridcolor='#2D3748', zerolinecolor='#2D3748'),
                    'yaxis': dict(gridcolor='#2D3748', zerolinecolor='#2D3748')
                }

                if y_axis_zero and not normalize:
                    layout_opts['yaxis'] = dict(rangemode='tozero', gridcolor='#2D3748', zerolinecolor='#2D3748')

                fig.update_layout(**layout_opts)
                st.plotly_chart(fig, use_container_width=True)

                # Statistics for each indicator
                st.subheader("📊 Statistics")

                for sel_id, dataset in datasets.items():
                    df = dataset['data']
                    meta = dataset['metadata']
                    unit = meta.get('unit', 'N/A')

                    st.markdown(f"**{dataset['name']}** (Unit: {unit})")
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Current", f"{df.iloc[-1]['value']:,.2f}")
                    with col2:
                        st.metric("Average", f"{df['value'].mean():,.2f}")
                    with col3:
                        st.metric("Min", f"{df['value'].min():,.2f}")
                    with col4:
                        st.metric("Max", f"{df['value'].max():,.2f}")

                    # Trends
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("30-Day", f"{calculate_change(df, 30):+.2f}%")
                    with col2:
                        st.metric("90-Day", f"{calculate_change(df, 90):+.2f}%")
                    with col3:
                        st.metric("1-Year", f"{calculate_change(df, 365):+.2f}%")

                    st.divider()

                # Download combined data
                if len(datasets) > 0:
                    # Merge all dataframes
                    combined_df = None
                    for sel_id, dataset in datasets.items():
                        df = dataset['data'][['timestamp', 'value']].copy()
                        df = df.rename(columns={'value': sel_id})
                        if combined_df is None:
                            combined_df = df
                        else:
                            combined_df = pd.merge(combined_df, df, on='timestamp', how='outer')

                    if combined_df is not None:
                        combined_df = combined_df.sort_values('timestamp')
                        csv = combined_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Combined Data as CSV",
                            data=csv,
                            file_name=f"comparison_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
            else:
                st.error("No data available for selected indicators")

# Page: FAQ
elif page == "FAQ":
    st.header("FAQ: Understanding the Metrics")
    st.markdown("Comprehensive explanations of the key indicators and metrics used throughout this dashboard.")

    # Create expandable sections for each metric category
    with st.expander("**10-Year/2-Year Treasury Spread (Yield Curve Inversion)**", expanded=False):
        st.markdown("""
        ### The 10Y-2Y Treasury Spread: The Most Reliable Recession Predictor

        **What It Is:**
        The 10-Year/2-Year Treasury Spread measures the difference between the yield (interest rate) on 10-year U.S. Treasury bonds and 2-year Treasury notes. When you subtract the 2-year yield from the 10-year yield, you get "the spread." A positive spread means long-term rates are higher than short-term rates (normal). A negative spread means short-term rates exceed long-term rates (inverted).

        **Why It Matters:**
        This single indicator has predicted every U.S. recession since 1955 with remarkable accuracy, typically 6-24 months before the downturn begins. There has been only one false positive in nearly 70 years (a brief inversion in 1966 that didn't lead to recession). No other economic indicator comes close to this track record, which is why it receives so much attention from investors, economists, and the Federal Reserve itself.

        **The Economic Logic:**
        In a healthy economy, lenders demand higher interest rates for longer-term loans because they're taking on more risk - inflation could erode purchasing power, the borrower might default, or better opportunities might arise. This creates an upward-sloping yield curve. When the curve inverts, it signals that bond market participants collectively expect economic trouble ahead. Here's the mechanism:

        1. **Expectations of Fed Rate Cuts:** When investors anticipate a recession, they expect the Federal Reserve will eventually cut short-term rates to stimulate the economy. They rush to lock in today's long-term rates before they fall, driving down long-term yields.

        2. **Flight to Safety:** During uncertainty, investors flee risky assets (stocks, corporate bonds) for the safety of Treasury bonds. This surge in demand for long-term Treasuries pushes their prices up and yields down.

        3. **Fed Tightening:** Often, inversions occur when the Fed is actively raising short-term rates to combat inflation. The 2-year yield (sensitive to Fed policy) rises, while the 10-year yield (driven by growth expectations) stagnates or falls.

        **Historical Context:**
        - **2006-2007:** The curve inverted in late 2006, about 18 months before the Great Recession officially began in December 2007. Investors who heeded this warning had time to reduce risk exposure before the 2008 crash.
        - **2019:** A brief inversion occurred in August 2019, and the COVID recession hit in February 2020 (though this was obviously caused by an external shock, not economic fundamentals).
        - **2022-2024:** The yield curve inverted in July 2022 and remained inverted for an unusually long period - over two years. This prolonged inversion sparked intense "recession watch" debates, yet the economy proved more resilient than historical patterns suggested, leading to discussions about whether structural changes (massive fiscal stimulus, strong labor market) might be altering the indicator's reliability.

        **How to Use This Metric:**
        - **Negative spread (below zero):** Recession warning. Historically, this signals elevated recession probability within 6-24 months. Consider reducing exposure to cyclical stocks, increasing cash or defensive positions, and stress-testing your portfolio.
        - **Positive but flattening:** The curve is normalizing, which can happen before economic recovery or during periods of uncertainty. Watch the trend direction.
        - **Positive and steepening:** Generally bullish for economic growth. Long-term rates rising faster than short-term rates suggests investors expect stronger future growth and inflation.

        **Limitations:**
        The yield curve is not a timing tool - it tells you recession is likely but not exactly when. The lag between inversion and recession has varied from 6 to 24 months historically. Additionally, unprecedented monetary policy (quantitative easing, yield curve control discussions) may have distorted traditional relationships. The 2022-2024 experience suggests the indicator may need recalibration for the post-COVID economic environment.

        **Related Metrics:** The 10Y-3M spread (10-year minus 3-month) is also closely watched and some economists consider it even more predictive than the 10Y-2Y spread.
        """)

    with st.expander("**Federal Reserve Balance Sheet & Liquidity Metrics**", expanded=False):
        st.markdown("""
        ### Fed Balance Sheet, M2, Reverse Repo, and Treasury General Account: The Liquidity Framework

        **What These Metrics Are:**
        These four indicators together paint a picture of how much money is flowing through the financial system - what traders call "liquidity." Many professional investors argue that liquidity conditions are the primary driver of asset prices in the modern era, often more important than corporate earnings or economic growth.

        ---

        **Federal Reserve Balance Sheet (WALCL)**

        The Fed's balance sheet represents the total assets held by the Federal Reserve, primarily U.S. Treasury securities and mortgage-backed securities (MBS). When the Fed "prints money," it doesn't literally print cash - it creates digital bank reserves by purchasing these securities from banks and financial institutions.

        *Historical Context:*
        - **Pre-2008:** The balance sheet was around $900 billion, mostly Treasury bills needed for normal monetary operations.
        - **2008-2014 (QE1-QE3):** Expanded to $4.5 trillion through three rounds of quantitative easing to combat the financial crisis and support the recovery.
        - **2020-2022 (COVID QE):** Exploded from $4.2T to nearly $9T as the Fed purchased $120 billion/month in securities to support markets during the pandemic.
        - **2022-Present (QT):** The Fed began "quantitative tightening," allowing securities to mature without replacement, slowly shrinking the balance sheet.

        *Why It Matters:*
        When the Fed expands its balance sheet, it injects reserves into the banking system. Banks can lend more, financial institutions have more cash to deploy, and this money flows into stocks, bonds, real estate, and other assets. The correlation between Fed balance sheet expansion and stock market gains from 2009-2021 was striking. Conversely, balance sheet reduction (QT) withdraws liquidity and can create headwinds for asset prices.

        ---

        **M2 Money Supply**

        M2 is the broadest commonly-reported measure of money in the economy. It includes:
        - Physical currency in circulation
        - Checking account deposits
        - Savings accounts
        - Money market funds
        - Small time deposits (CDs under $100,000)

        *Historical Context:*
        M2 typically grows 5-7% annually, reflecting economic growth and modest inflation. During COVID, M2 exploded by over 25% in 2020-2021 as stimulus checks, PPP loans, and Fed asset purchases flooded the system with cash. In 2022-2023, M2 actually contracted year-over-year - the first sustained decline since the Great Depression. This monetary contraction contributed to the "soft landing" scenario by reducing inflationary pressure without requiring a severe recession.

        *Why It Matters:*
        M2 represents the actual money available for spending and investing. Rapid M2 growth often precedes inflation (more money chasing the same goods). M2 contraction can slow economic activity and asset price appreciation. The quantity theory of money (MV=PQ) suggests that money supply growth, all else equal, leads to either higher prices (inflation) or higher output (real growth).

        ---

        **Reverse Repo Facility (RRP)**

        The Reverse Repo facility is where money market funds and certain financial institutions can park excess cash overnight at the Federal Reserve, earning a guaranteed interest rate. Think of it as a giant savings account at the Fed for institutional money.

        *Historical Context:*
        The RRP was barely used before 2021, typically holding less than $200 billion. It surged to over $2.5 trillion by late 2022 as:
        - Massive liquidity from COVID stimulus had nowhere productive to go
        - Short-term Treasury supply was limited
        - The Fed's RRP rate became attractive relative to alternatives

        Since then, RRP has drained significantly as Treasury bill issuance increased (giving money funds alternative investments) and as overall liquidity declined.

        *Why It Matters:*
        High RRP usage indicates excess liquidity "trapped" at the Fed rather than flowing into markets. When RRP drains, that money re-enters the financial system, potentially supporting asset prices. Some analysts use RRP as a gauge of how much "dry powder" exists that could flow into risk assets.

        ---

        **Treasury General Account (TGA)**

        The TGA is essentially the U.S. government's checking account at the Federal Reserve. When the Treasury collects taxes or issues debt, the money flows into the TGA. When the government spends (pays contractors, issues refunds, funds programs), money flows out of the TGA.

        *Historical Context:*
        The TGA historically held $200-400 billion. During COVID, it swelled to over $1.8 trillion as the Treasury pre-funded pandemic response programs. It then drained rapidly as those funds were spent. The TGA experiences predictable seasonal patterns (building up before tax deadlines, draining after) and irregular swings around debt ceiling negotiations.

        *Why It Matters:*
        TGA changes directly impact market liquidity:
        - **TGA rising (Treasury raising cash):** Drains liquidity from markets as money flows from the private sector to the government's account.
        - **TGA falling (Treasury spending):** Injects liquidity as government payments flow to businesses and individuals who deposit or invest the funds.

        ---

        **The Net Liquidity Framework:**
        Many traders calculate "net liquidity" as: **Fed Balance Sheet - TGA - RRP = Net Liquidity**

        This formula attempts to capture the actual money available to support asset prices after accounting for funds trapped at the Fed (RRP) and held by Treasury (TGA). Rising net liquidity tends to correlate with rising stock prices; falling net liquidity creates headwinds. While not a perfect predictor, this framework helps explain many major market moves since 2020.
        """)

    with st.expander("**Inflation Metrics: CPI, Core CPI, PCE, and Breakeven Inflation**", expanded=False):
        st.markdown("""
        ### Understanding Inflation: The Metrics That Drive Fed Policy

        Inflation - the rate at which prices rise across the economy - is arguably the most important economic variable for investors. It directly drives Federal Reserve policy, which in turn moves interest rates, bond prices, stock valuations, and virtually every other financial asset. Understanding the nuances between different inflation measures helps you anticipate Fed actions and position your portfolio accordingly.

        ---

        **Consumer Price Index (CPI)**

        *What It Is:*
        CPI is the most widely reported inflation measure, produced monthly by the Bureau of Labor Statistics (BLS). It tracks price changes for a "basket" of approximately 80,000 goods and services that represent typical urban consumer spending, including housing, food, transportation, medical care, apparel, and entertainment.

        *How It's Calculated:*
        BLS employees literally visit stores, call service providers, and survey landlords to collect prices. The basket is weighted by spending patterns from consumer surveys. Housing (shelter) is the largest component at roughly 33% of the index.

        *Historical Context:*
        - **1970s-1980s:** CPI peaked at 14.8% in 1980 during the stagflation era, prompting Fed Chair Volcker's aggressive rate hikes.
        - **1990s-2010s:** CPI averaged 2-3%, the "Great Moderation" era of stable prices.
        - **2021-2022:** CPI surged to 9.1% (June 2022), the highest in 40 years, driven by pandemic supply chain disruptions, massive fiscal/monetary stimulus, and the Ukraine war's impact on energy prices.
        - **2023-Present:** CPI has declined but remains "sticky" above the Fed's 2% target.

        *Limitations:*
        CPI uses a fixed basket that may not reflect your personal spending. If beef prices rise and you switch to chicken, CPI still measures beef. The housing component (Owner's Equivalent Rent) lags actual market rents by 12-18 months due to methodology, which is why CPI remained elevated in 2023 even as real-time rent data showed cooling.

        ---

        **Core CPI (CPI Less Food and Energy)**

        *What It Is:*
        Core CPI removes food and energy prices from the calculation, focusing on the remaining ~75% of the basket.

        *Why It Exists:*
        Food and energy prices are notoriously volatile - a hurricane disrupts refinery output, a drought affects crop yields, OPEC changes production quotas. These swings can cause headline CPI to spike or plunge in ways that don't reflect underlying inflation trends. Core CPI attempts to show "sticky" inflation that persists month after month.

        *Why It Matters:*
        Fed officials often focus on core measures because they're more indicative of where inflation is heading. A spike in gasoline prices will reverse when supply normalizes; a spike in service prices (wages, rents) tends to persist. When making policy decisions, the Fed wants to avoid overreacting to temporary commodity swings.

        ---

        **Personal Consumption Expenditures (PCE) Price Index**

        *What It Is:*
        PCE is actually the Federal Reserve's *preferred* inflation measure, even though it gets less media attention than CPI. It's produced by the Bureau of Economic Analysis (BEA) as part of GDP calculations.

        *How It Differs from CPI:*
        1. **Broader Coverage:** PCE includes spending on behalf of consumers (employer-paid health insurance, Medicare/Medicaid payments), not just out-of-pocket expenses.
        2. **Substitution Effect:** PCE adjusts for consumer behavior - when beef prices rise, it assumes consumers buy more chicken. CPI uses a fixed basket.
        3. **Different Weights:** PCE weights housing lower (~15% vs 33% in CPI) and healthcare higher.

        *Why the Fed Prefers PCE:*
        PCE tends to run 0.3-0.5 percentage points lower than CPI due to the substitution adjustment. The Fed believes this better reflects actual inflation experienced by consumers. The Fed's official 2% inflation target is expressed in terms of PCE, not CPI.

        ---

        **10-Year Breakeven Inflation Rate**

        *What It Is:*
        The breakeven rate is derived from bond markets by comparing yields on regular Treasury bonds to Treasury Inflation-Protected Securities (TIPS). The difference represents what bond investors expect inflation to average over the next 10 years.

        *How It's Calculated:*
        10-Year Treasury Yield - 10-Year TIPS Yield = Breakeven Inflation

        If 10-year Treasuries yield 4.5% and 10-year TIPS yield 2.0%, the breakeven is 2.5% - meaning investors expect inflation to average 2.5% annually over the next decade.

        *Why It Matters:*
        Unlike CPI and PCE (which measure past inflation), breakeven rates are forward-looking. They tell you what millions of bond market participants - professional investors betting real money - expect inflation to be. Rising breakevens often precede Fed hawkishness (rate hikes); falling breakevens suggest inflation concerns are easing.

        *Historical Context:*
        Breakevens typically hover around 2-2.5%, consistent with the Fed's target. They crashed below 1% during the COVID panic (March 2020) and surged above 3% during the 2022 inflation scare. As of 2024-2025, they've normalized around 2.3-2.5%, suggesting markets believe the Fed will ultimately succeed in controlling inflation.

        ---

        **Interpreting the Inflation Dashboard:**
        - **CPI > 3% and rising:** Fed likely to remain hawkish; expect rate hikes or "higher for longer" rhetoric
        - **Core CPI sticky while headline CPI falls:** The "hard part" of fighting inflation - embedded price pressures
        - **PCE at or below 2%:** Fed may consider rate cuts; bullish for stocks and bonds
        - **Breakevens rising sharply:** Markets losing confidence in Fed's inflation control; negative for fixed income
        """)

    with st.expander("**VIX (Volatility Index) - The Fear Gauge**", expanded=False):
        st.markdown("""
        ### The VIX: Wall Street's Fear Gauge

        **What It Is:**
        The VIX (CBOE Volatility Index) measures expected stock market volatility over the next 30 days. It's calculated from prices of S&P 500 index options and is expressed in percentage points representing the annualized expected move in the S&P 500.

        *Technical Definition:*
        A VIX reading of 20 implies that the market expects the S&P 500 to move (up or down) roughly 20% over the next year, or about 5.8% over the next month (20% / sqrt(12)). However, most investors interpret VIX simply as a fear/complacency gauge rather than calculating precise expected moves.

        **Why It Matters:**
        The VIX is inversely correlated with stock prices about 80% of the time - when stocks fall sharply, VIX spikes, and vice versa. This makes it a real-time sentiment indicator. More importantly, the VIX has predictive value: extreme readings often signal market turning points.

        ---

        **Interpreting VIX Levels:**

        **Below 12 - Extreme Complacency:**
        Markets are calm, investors are confident, and options are cheap. While this can persist during strong bull markets, historically low VIX often precedes corrections. Investors aren't pricing in any risk, which means even minor negative surprises can cause outsized reactions.

        **12-17 - Low Volatility:**
        Generally favorable conditions. Markets are trending without major concerns. Common during economic expansions and bull markets. The VIX spent much of 2017 and 2024 in this range.

        **17-25 - Normal/Elevated:**
        This is the historical average range. Some uncertainty exists, but nothing alarming. Markets can trend up or down from here. The VIX typically oscillates in this range during mixed economic conditions.

        **25-35 - High Volatility:**
        Significant fear in the market. Usually coincides with corrections (10%+ declines) or specific shock events. Investors are paying up for portfolio protection. This level often represents opportunity for long-term investors willing to buy fear.

        **Above 35 - Extreme Fear:**
        Crisis conditions. Markets are in freefall or anticipating severe negative outcomes. Options become extremely expensive as investors panic-buy protection.

        **Historic Spikes:**
        - **October 2008 (Financial Crisis):** VIX hit 80, the highest ever recorded at the time
        - **August 2011 (U.S. Debt Downgrade):** VIX spiked to 48
        - **August 2015 (China Devaluation):** VIX briefly touched 53
        - **February 2018 (Volmageddon):** VIX jumped from 13 to 37 in one day
        - **March 2020 (COVID Crash):** VIX hit 82.69, surpassing the 2008 peak

        ---

        **How to Use the VIX:**

        **Contrarian Indicator:**
        VIX extremes often mark market turning points. When VIX spikes above 35-40 during selloffs, it frequently indicates capitulation - the point of maximum fear when weak hands have sold and buying opportunities emerge. Conversely, very low VIX (below 12) often precedes corrections, as complacent markets are vulnerable to surprise.

        **Mean Reversion:**
        Unlike stocks, the VIX doesn't trend indefinitely. It's fundamentally mean-reverting because volatility spikes are unsustainable - markets can't crash 5% daily forever. This mean-reversion tendency makes VIX spikes potential buying signals for stocks (and selling signals for VIX-related products).

        **Portfolio Protection Gauge:**
        High VIX means options are expensive - paying for downside protection costs more. Low VIX means options are cheap - an ideal time to buy portfolio insurance if you're concerned about future risks.

        **Risk Management:**
        Many systematic strategies use VIX to adjust position sizes: reducing exposure when VIX is high (markets are dangerous) and increasing exposure when VIX is low (markets are calm). However, this can lead to buying high and selling low if implemented naively.

        ---

        **Limitations:**
        The VIX measures *expected* volatility, not *realized* volatility. Markets can remain calm when VIX is elevated, or surprise investors when VIX is low. VIX is also influenced by options market supply/demand dynamics, not just fear. Systematic selling of volatility by pension funds and structured products can suppress VIX even when underlying risks exist.
        """)

    with st.expander("**Growth vs. Value Investing (IWF/IWD)**", expanded=False):
        st.markdown("""
        ### Growth vs. Value: The Fundamental Style Rotation

        **What These ETFs Represent:**
        - **IWF (iShares Russell 1000 Growth ETF):** Tracks large-cap U.S. stocks classified as "growth" companies
        - **IWD (iShares Russell 1000 Value ETF):** Tracks large-cap U.S. stocks classified as "value" companies

        The Russell 1000 contains the 1,000 largest U.S. companies. It's divided into Growth and Value using metrics like price-to-book ratio, forecasted earnings growth, and historical sales growth.

        ---

        **Defining Growth and Value:**

        **Growth Stocks:**
        Companies expected to grow earnings faster than the market average. Characteristics include:
        - High price-to-earnings (P/E) ratios - investors pay premium for future growth
        - High price-to-book (P/B) ratios
        - Low or no dividends - profits reinvested for expansion
        - Revenue growing 15-30%+ annually
        - Often in technology, consumer discretionary, healthcare innovation

        *Examples:* Apple, Microsoft, Nvidia, Amazon, Tesla, Meta

        **Value Stocks:**
        Companies trading at low prices relative to their fundamentals. Characteristics include:
        - Low P/E ratios - "cheap" relative to current earnings
        - Low P/B ratios - trading near or below book value
        - Higher dividend yields - returning cash to shareholders
        - Mature businesses with slower growth
        - Often in financials, energy, utilities, industrials

        *Examples:* JPMorgan, ExxonMobil, Johnson & Johnson, Procter & Gamble, Berkshire Hathaway

        ---

        **The Historical Cycle:**

        **Academic Evidence:**
        The "value premium" - the tendency for value stocks to outperform growth over long periods - was documented by professors Fama and French in the 1990s. From 1926-2006, value outperformed growth by roughly 3% annually on average.

        **Growth Dominance (2010-2021):**
        The decade following the financial crisis was historically anomalous. Growth massively outperformed value, driven by:
        - Near-zero interest rates (low discount rates favor distant future cash flows)
        - Technology's increasing dominance of the economy
        - Network effects and winner-take-all dynamics in digital businesses
        - Underperformance of financials, energy, and other value sectors

        The FAANG stocks (Facebook/Meta, Apple, Amazon, Netflix, Google) became so dominant that growth vs. value became largely a tech vs. everything-else bet.

        **Value Revival (2022):**
        When the Fed began raising rates aggressively, growth stocks got crushed. Higher discount rates reduce the present value of future earnings, hitting high-P/E growth stocks hardest. Value surged as:
        - Banks benefited from higher interest rates (wider lending margins)
        - Energy soared with oil prices
        - Investors sought current income (dividends) over speculative growth

        **2023-2024 Mixed Regime:**
        The environment has become more nuanced, with AI excitement fueling select growth stocks while traditional value sectors have struggled to maintain momentum.

        ---

        **Why The Rotation Matters:**

        **Portfolio Construction:**
        Your style allocation significantly impacts returns. A portfolio tilted heavily toward growth would have outperformed 2010-2021 but underperformed 2022. Understanding the current regime helps with tactical allocation.

        **Economic Linkage:**
        - **Growth favored:** Low interest rates, technological disruption, risk-on sentiment
        - **Value favored:** Rising rates, inflation, economic recovery from recession, risk-off sentiment

        **Interest Rate Sensitivity:**
        Growth stocks are essentially long-duration assets - most of their value comes from earnings years or decades in the future. When rates rise, those future earnings are discounted more heavily, crushing valuations. Value stocks generate more current cash flow and are less interest-rate sensitive.

        ---

        **How to Interpret the Dashboard Chart:**

        The chart normalizes both IWF and IWD to show percentage returns from the start of your selected period. If Growth is above Value, growth stocks have outperformed during that timeframe. The spread between the lines shows the magnitude of outperformance.

        **Watch for crossovers:** When the lagging style crosses above the leader, it often signals a regime shift that can persist for months or years. The 2022 crossover (value overtaking growth) was significant after a decade of growth dominance.

        **Tactical Considerations:**
        - Momentum followers tilt toward the leading style
        - Mean-reversion believers tilt toward the lagging style
        - Most advisors recommend maintaining exposure to both, rebalancing periodically to capture relative performance
        """)

    with st.expander("**Large Cap vs. Small Cap (SPY/IWM)**", expanded=False):
        st.markdown("""
        ### Large Cap vs. Small Cap: The Size Factor

        **What These ETFs Represent:**
        - **SPY (SPDR S&P 500 ETF):** Tracks the 500 largest U.S. companies by market capitalization
        - **IWM (iShares Russell 2000 ETF):** Tracks 2,000 smaller U.S. companies (roughly ranks 1,001-3,000 by size)

        The "size factor" is one of the most studied phenomena in finance, alongside value and momentum.

        ---

        **Characteristics of Each:**

        **Large Caps (SPY):**
        - Massive companies: average market cap $50B+, giants like Apple exceed $3 trillion
        - Global operations with diversified revenue streams
        - Generally stable earnings, lower volatility
        - High liquidity - easy to trade with minimal market impact
        - More analyst coverage, more efficiently priced
        - Currently dominated by technology mega-caps

        **Small Caps (IWM):**
        - Companies with market caps typically $300M - $2B
        - Often more domestically focused
        - Higher growth potential but also higher failure risk
        - More volatile - can move 2-3% on days when SPY moves 1%
        - Less analyst coverage - potential for mispricing
        - More sensitive to domestic economic conditions
        - Higher debt loads relative to size, more interest rate sensitive

        ---

        **The Small Cap Premium:**

        **Academic Theory:**
        Research shows that small caps have historically outperformed large caps over very long periods (5-10%+ annually in some studies). Theories for why:
        - Greater risk requires greater return (compensation for volatility, illiquidity, bankruptcy risk)
        - Less analyst coverage creates exploitable inefficiencies
        - Small companies have more room to grow

        **Reality Check:**
        The small cap premium has been inconsistent. From 2010-2023, large caps actually outperformed, driven by:
        - The rise of mega-cap tech (unprecedented concentration of returns)
        - Globalization favoring multinationals
        - Low rates favoring growth (large caps are more growth-weighted)
        - Index investing flows disproportionately benefiting large caps

        ---

        **Cyclical Patterns:**

        **Small Caps Lead Economic Recovery:**
        Historically, small caps outperform coming out of recessions:
        - They're more domestically exposed and benefit from U.S. recovery
        - They often fell harder during the recession, so they have more to recover
        - Risk appetite returns, favoring higher-beta assets
        - They're more sensitive to credit conditions, which ease during recovery

        **Large Caps Lead During Uncertainty:**
        When economic conditions are uncertain or deteriorating:
        - Investors seek quality and stability
        - Large caps have stronger balance sheets to weather storms
        - Global diversification provides hedging
        - Liquidity premium increases (investors pay up for ability to exit easily)

        **Interest Rate Sensitivity:**
        Small caps are more interest rate sensitive because:
        - Higher debt levels relative to market cap
        - More reliance on variable-rate bank loans vs. fixed-rate bonds
        - Many are unprofitable and dependent on access to capital markets

        The 2022-2023 rate hikes hit small caps harder than large caps partly for these reasons.

        ---

        **Interpreting the Dashboard:**

        The chart shows normalized returns allowing direct comparison. When SPY is above IWM, large caps are outperforming. The spread indicates magnitude.

        **Signals to Watch:**
        - **Small caps surging after recession:** Classic risk-on signal, economic recovery underway
        - **Small caps diverging negative while large caps flat:** Warning sign of credit stress or domestic weakness
        - **Persistent large cap dominance:** May indicate market narrowness (gains concentrated in few stocks), which can be fragile

        **The Breadth Consideration:**
        When large caps dramatically outperform small caps, it often means returns are concentrated in a handful of mega-cap names. This "narrow" market can be vulnerable - if those few leaders stumble, the index has limited support. Healthy bull markets typically feature broad participation across market caps.
        """)

    with st.expander("**Unemployment Rate & The Sahm Rule**", expanded=False):
        st.markdown("""
        ### Unemployment Rate: The Lagging Indicator That Matters Most

        **What It Is:**
        The unemployment rate represents the percentage of the labor force (people working or actively seeking work) who don't have jobs. It's calculated monthly by the Bureau of Labor Statistics from surveys of approximately 60,000 households.

        *The Formula:*
        Unemployment Rate = (Unemployed / Labor Force) x 100

        *Important Nuance:*
        You must be actively looking for work to count as "unemployed." People who've given up searching (discouraged workers) or who are underemployed (working part-time but wanting full-time) aren't captured in the headline rate. Alternative measures (U-6) capture these broader definitions.

        ---

        **Why It's a Lagging Indicator:**

        Unlike leading indicators (yield curve, housing starts), unemployment is "lagging" - it rises *during* recessions, not before them. Companies don't lay off workers in anticipation of recession; they wait until revenues actually decline and layoffs become unavoidable.

        *Typical Sequence:*
        1. Economic conditions deteriorate
        2. Corporate profits decline
        3. Hiring freezes implemented
        4. Layoffs begin
        5. Unemployment rate rises
        6. NBER officially declares recession (often months after it began)

        **Why It Still Matters:**
        Despite being lagging, unemployment is crucial because:
        - It determines Fed policy (the Fed has a "dual mandate" of price stability AND maximum employment)
        - Consumer spending drives ~70% of GDP - unemployed people spend less
        - It's self-reinforcing: layoffs reduce spending, which causes more layoffs
        - It's a key input for recession dating

        ---

        **The Sahm Rule: Turning Lagging Into Real-Time**

        Economist Claudia Sahm developed a rule that transforms the lagging unemployment rate into a real-time recession indicator:

        **The Rule:**
        A recession has begun when the 3-month average unemployment rate rises by 0.5 percentage points or more relative to its low over the prior 12 months.

        **Why It Works:**
        The labor market has strong momentum. Once unemployment starts rising meaningfully, it tends to keep rising. The 0.5 percentage point threshold captures the "escape velocity" point where normal fluctuations have clearly turned into genuine deterioration.

        **Historical Performance:**
        The Sahm Rule has correctly identified every recession since 1970 in real-time, with no false positives. It triggered:
        - March 2020 (COVID recession) - immediate confirmation
        - December 2007 (Great Recession) - identified recession at its start
        - March 2001 (Dot-com recession) - correctly flagged

        **2024 Experience:**
        The Sahm Rule briefly triggered in mid-2024, sparking recession fears. However, the context was unusual - unemployment rose partly due to labor force growth (immigration, workers returning) rather than purely from layoffs. This highlighted that even reliable rules require interpretation.

        ---

        **Key Thresholds:**

        - **Below 4%:** Historically tight labor market, workers have bargaining power, wage pressures may build
        - **4-5%:** Generally considered "full employment" - the natural rate consistent with stable inflation
        - **5-6%:** Elevated but not crisis-level; may indicate economic softening
        - **Above 6%:** Typically associated with recessions or their aftermath
        - **Above 10%:** Severe recession (reached 10% in 2009, 14.7% briefly in April 2020)

        ---

        **How to Use This Metric:**

        **Watch the Trend, Not the Level:**
        A steady 4.2% unemployment is very different from 4.2% that was 3.5% six months ago. The direction and velocity of change matter more than the absolute level.

        **Compare to Fed Projections:**
        The Fed publishes quarterly projections for unemployment. If actual unemployment rises faster than projected, expect more dovish policy (rate cuts). If unemployment stays lower than projected, the Fed can maintain restrictive policy longer.

        **Consider Labor Force Participation:**
        Unemployment can fall for "bad" reasons (people giving up and leaving the labor force) or "good" reasons (job creation). Check the labor force participation rate alongside unemployment for the full picture.

        **Initial Jobless Claims as Leading Component:**
        Weekly initial claims (new unemployment filings) provide more timely data than the monthly unemployment rate. Rising claims often precede unemployment rate increases by 1-2 months.
        """)

    with st.expander("**Housing Starts: The Economy's Crystal Ball**", expanded=False):
        st.markdown("""
        ### Housing Starts: Why Home Construction Predicts Recessions

        **What It Is:**
        Housing starts measure the number of new residential construction projects that began during a given month. A "start" is counted when excavation begins for the foundation. The data is reported monthly by the Census Bureau and expressed as a seasonally adjusted annual rate (SAAR) - meaning the monthly figure is multiplied by 12 to represent what annual starts would be if that month's pace continued all year.

        ---

        **Why It's a Leading Indicator:**

        Housing starts are uniquely forward-looking because builders must make decisions based on expected future demand:

        1. **Long Planning Horizons:** From land acquisition to completed home takes 6-12+ months. Builders start projects based on where they expect demand to be next year, not today.

        2. **Financing Sensitivity:** New construction is highly sensitive to mortgage rates and credit availability. When rates rise, builders pull back before buyers stop shopping.

        3. **Economic Multiplier:** Each housing start triggers a cascade of economic activity - lumber, appliances, labor, furniture, landscaping. This makes housing a reliable early signal of broader economic momentum.

        4. **Builder Confidence:** Builders are essentially betting their capital on future conditions. When they reduce starts, they're signaling pessimism about the economic outlook.

        ---

        **Historical Context:**

        **Normal Range:** 1.0-1.5 million starts annually during healthy economic periods

        **Key Historical Episodes:**
        - **2005-2006:** Housing starts peaked at 2.3 million annually, a level that in retrospect signaled massive overbuilding during the housing bubble
        - **2008-2009:** Collapsed to under 500,000 - the lowest since records began in 1959. The housing crash both triggered and deepened the Great Recession.
        - **2010-2019:** Slow recovery to ~1.2 million, constrained by post-crisis lending standards and labor shortages
        - **2020-2021:** Surged to 1.7 million as pandemic-driven demand for suburban homes and low rates spurred construction
        - **2022-2023:** Pulled back toward 1.4 million as mortgage rates doubled

        ---

        **The Recession Connection:**

        Housing starts have declined before every recession since 1960, typically 12-18 months before the official start date:

        - **Pre-2001 recession:** Starts peaked in early 1999, well before the March 2001 recession
        - **Pre-2008 recession:** Starts peaked in January 2006, nearly two years before the December 2007 recession start
        - **Pre-COVID:** Starts actually held up well, confirming that COVID was an external shock rather than an endogenous economic cycle

        **The Mechanism:**
        When housing starts decline significantly:
        1. Construction jobs are lost (construction is ~5% of employment)
        2. Building material demand falls (lumber, concrete, appliances)
        3. Home sales slow, reducing realtor/mortgage broker incomes
        4. Consumer wealth effect weakens (less home equity appreciation)
        5. Local tax revenues decline (fewer permits, lower property values)

        ---

        **Interpreting the Data:**

        **Healthy Levels:** 1.2-1.6 million starts typically indicates sustainable demand
        **Overheating:** Above 1.8 million may signal unsustainable boom (watch for speculative building)
        **Recession Warning:** Sharp decline (20%+ from peak) especially with falling permits suggests economic trouble ahead
        **Recovery Signal:** Sustained increases from depressed levels often mark economic recovery

        **Related Metrics:**
        - **Building Permits:** Even more forward-looking than starts (permits must be obtained before starting)
        - **Home Sales:** Existing and new home sales show actual transaction activity
        - **Homebuilder Sentiment (NAHB Index):** Survey of builder confidence
        - **Case-Shiller Index:** Home price appreciation

        ---

        **Current Interpretation:**

        Housing starts should be interpreted alongside mortgage rates. During 2022-2023, starts held up better than many expected despite 7%+ mortgage rates because:
        - Existing homeowners with low-rate mortgages weren't selling, constraining inventory
        - Strong demographics (Millennials entering prime homebuying years)
        - Builders offered rate buydowns and incentives

        The "lock-in effect" - homeowners unwilling to trade their 3% mortgage for a 7% one - has created unusual dynamics where new construction remained relatively resilient while existing home sales plummeted.
        """)

    with st.expander("**Consumer Sentiment: Measuring Economic Mood**", expanded=False):
        st.markdown("""
        ### Consumer Sentiment: The Psychology of Spending

        **What It Is:**
        The University of Michigan Consumer Sentiment Index is a monthly survey measuring how optimistic or pessimistic consumers feel about their personal finances and the broader economy. Approximately 500 households are surveyed by telephone each month, answering questions about:

        1. Current financial situation compared to a year ago
        2. Expected financial situation a year from now
        3. Economic outlook for the next 12 months
        4. Economic outlook for the next 5 years
        5. Current buying conditions for major household items

        The index is normalized so that 1966 = 100 (the base year when the survey methodology was standardized).

        ---

        **Why It Matters:**

        Consumer spending drives approximately 70% of U.S. GDP. Unlike business investment or government spending, consumer behavior is heavily influenced by psychology and confidence:

        **The Self-Fulfilling Prophecy:**
        - When consumers feel confident, they spend more, boosting the economy, which validates their confidence
        - When consumers feel pessimistic, they cut spending, slowing the economy, which validates their pessimism

        **Predictive Value:**
        Consumer sentiment often changes direction before actual spending does. A collapse in sentiment can foreshadow reduced consumption even before economic data shows weakness.

        **Fed Attention:**
        The Federal Reserve monitors sentiment closely because:
        - It influences inflation expectations (confident consumers may spend despite higher prices)
        - It affects the transmission of monetary policy (pessimistic consumers may not respond to rate cuts)
        - Extreme readings may require policy response

        ---

        **Historical Context:**

        **Key Reference Points:**
        - **Above 100:** Historically optimistic (reached 112 in January 2000)
        - **80-100:** Normal range during economic expansions
        - **60-80:** Below average, often during slowdowns or uncertainty
        - **Below 60:** Pessimistic, typically during recessions
        - **Record Low:** 50.0 in June 2022 (surpassed even the 2008 financial crisis trough)

        **Notable Episodes:**
        - **1990-1991 Recession:** Sentiment dropped to 63
        - **2008-2009 Financial Crisis:** Bottomed at 55.3 in November 2008
        - **2020 COVID Crash:** Dropped to 71.8 in April 2020 (relatively mild given circumstances)
        - **2022 Inflation Shock:** Collapsed to 50.0 - the lowest ever recorded, driven by inflation concerns despite a strong labor market

        ---

        **The 2022 Anomaly:**

        The June 2022 reading of 50.0 was historically unprecedented and highlighted important nuances:

        **Why So Low:**
        - 40-year high inflation eroding purchasing power
        - Gasoline prices above $5/gallon nationally
        - Stock market decline reducing wealth
        - Housing affordability collapse
        - Political polarization (sentiment has become more partisan)

        **The Puzzle:**
        Sentiment hit all-time lows while:
        - Unemployment was near 50-year lows (3.6%)
        - Job openings were at record highs
        - Wage growth was strong
        - Consumer spending remained resilient

        This disconnect - people saying they feel terrible while continuing to spend - raised questions about the indicator's predictive value in the post-COVID environment.

        ---

        **Interpreting the Indicator:**

        **Watch the Trend:**
        Month-to-month changes of 5+ points are significant. Sustained moves over 3+ months are more meaningful than single-month spikes.

        **Context Matters:**
        Compare sentiment to actual economic conditions:
        - Low sentiment + strong economy = potential for improvement as pessimism lifts
        - High sentiment + weakening data = potential vulnerability

        **Political Overlay:**
        Since 2016, sentiment has become more politically polarized. Supporters of the incumbent party consistently report higher sentiment than opponents. This reduces the signal quality somewhat.

        **Components Matter:**
        The index has two sub-components:
        - **Current Conditions:** How people feel about the present
        - **Expectations:** How people feel about the future

        Divergence between these can be informative. If current conditions are good but expectations are poor, consumers may pull back spending in anticipation of trouble.

        ---

        **Related Metrics:**
        - **Conference Board Consumer Confidence:** Alternative measure with slightly different methodology; the two indices usually move together but can diverge
        - **Retail Sales:** Actual spending data to compare against sentiment
        - **Consumer Credit:** Borrowing behavior shows confidence in action
        - **Savings Rate:** High savings can reflect precautionary behavior (low confidence)
        """)

    with st.expander("**Industrial Production: Measuring Real Economic Output**", expanded=False):
        st.markdown("""
        ### Industrial Production: The Heartbeat of the Physical Economy

        **What It Is:**
        The Industrial Production Index (IPI) measures real output from three sectors:
        1. **Manufacturing** (~75% of the index) - factories producing goods
        2. **Mining** (~15%) - extraction of oil, gas, coal, metals
        3. **Utilities** (~10%) - electricity and gas production

        Published monthly by the Federal Reserve, the index is normalized so that 2017 = 100. Unlike GDP (which measures value), industrial production measures physical volume - actual widgets produced, barrels extracted, megawatts generated.

        ---

        **Why It Matters:**

        **Real Economy Signal:**
        Industrial production cuts through financial market noise to show what's actually happening in the physical economy. You can't fake factory output - either the widgets rolled off the assembly line or they didn't.

        **Recession Confirmation:**
        The National Bureau of Economic Research (NBER) uses industrial production as one of four key indicators for dating recessions. Significant sustained declines in industrial production are virtually synonymous with recession.

        **Global Supply Chain Indicator:**
        U.S. industrial production reflects demand from both domestic consumers and international supply chains. Weakness can indicate softening in global trade and manufacturing.

        ---

        **Historical Context:**

        **Long-Term Trend:**
        Industrial production has grown roughly 3% annually over the very long term, though this includes significant cyclical swings.

        **Recession Patterns:**
        - **2008-2009:** Industrial production fell 17% peak-to-trough, the largest decline since WWII
        - **2020 COVID:** Dropped 16% in just two months (March-April 2020), then recovered rapidly
        - **2001 Recession:** Declined about 6% - relatively mild for a recession

        **Post-COVID Reality:**
        As of 2024-2025, industrial production has not returned to its pre-pandemic trend. This reflects:
        - Supply chain restructuring (reshoring, "China plus one" strategies)
        - Labor constraints in manufacturing
        - Shift toward services in the overall economy

        ---

        **Interpreting the Data:**

        **Month-over-Month Changes:**
        - **+0.3% or higher:** Strong growth
        - **+0.1% to +0.2%:** Modest positive
        - **-0.1% to +0.1%:** Essentially flat
        - **-0.3% or worse:** Concerning weakness
        - **Two consecutive negative months:** Potential recession warning

        **Year-over-Year Comparison:**
        More useful for seeing trends through monthly noise. Sustained YoY declines are recession warning signs.

        **Capacity Utilization:**
        The Fed also publishes capacity utilization - what percentage of industrial capacity is being used:
        - **80%+:** Economy running hot, potential inflation pressure
        - **75-80%:** Normal healthy range
        - **Below 70%:** Significant slack, deflationary pressure
        - **Below 65%:** Recession territory (hit 63.4% in 2009, 64.2% in April 2020)

        ---

        **Manufacturing vs. Overall Economy:**

        **Important Caveat:**
        Manufacturing represents only about 11% of U.S. GDP (down from 28% in 1953). The U.S. economy is predominantly services - healthcare, finance, technology, education. This means:

        - Industrial production can decline without causing recession if services are strong
        - Manufacturing "recessions" (sustained IP declines) occurred in 2015-2016 and 2019 without full economic recessions
        - The indicator is most useful in conjunction with employment and consumption data

        **Still Valuable Because:**
        Manufacturing is more cyclical than services and often turns first. It's also more interest-rate sensitive (capital-intensive businesses) and more globally exposed. Think of industrial production as an early warning system for the goods-producing economy.

        ---

        **Related Metrics:**
        - **ISM Manufacturing PMI:** Survey-based forward-looking indicator of manufacturing activity
        - **Durable Goods Orders:** Orders for long-lasting manufactured items
        - **Factory Orders:** Broader measure including non-durable goods
        - **Capacity Utilization:** How much of industrial capacity is being used
        """)

    st.divider()
    st.markdown("""
    ### Additional Resources

    **Data Sources:**
    - **FRED (Federal Reserve Economic Data):** [fred.stlouisfed.org](https://fred.stlouisfed.org) - The primary source for economic indicators
    - **Yahoo Finance:** Real-time market prices and historical data
    - **Bureau of Labor Statistics (BLS):** Employment, inflation, and productivity data
    - **Bureau of Economic Analysis (BEA):** GDP, PCE, and national accounts data

    **Further Reading:**
    - Understanding the Federal Reserve's dual mandate (employment and price stability)
    - Business cycle theory and NBER recession dating
    - Modern Portfolio Theory and factor investing
    - Quantitative Easing and monetary policy transmission mechanisms
    """)

# Footer
st.divider()
st.markdown("""
<div class='footer-text'>
    <p>Macro Dashboard v2.0 | Data from FRED & Yahoo Finance</p>
    <p>Built with Streamlit | API Documentation: <a href='http://localhost:8000/docs'>localhost:8000/docs</a></p>
</div>
""", unsafe_allow_html=True)
