"""
Anmol AI Ops Incident Investigator
Streamlit Main Dashboard Application
Built by Anmol
"""

import streamlit as st
import json
from incidents import INCIDENTS
from analyzer import analyze_incident

# ---------------------------------------------------------
# Page Configuration & Modern SRE Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anmol AI Ops Incident Investigator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Executive / SRE Dashboard Styling
st.markdown("""
<style>
    /* Hide Streamlit Chrome, Header, Footer, Status Widgets, and Docstring Tooltips */
    #MainMenu {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stStatusWidget {display: none !important;}
    [data-testid="stTooltipContent"] {display: none !important;}
    [data-baseweb="tooltip"] {display: none !important;}
    div[class*="stDocstring"] {display: none !important;}


    /* Dark Palette Theme Overrides */
    .stApp {
        background-color: #0B1120;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Custom Header Container */
    .header-box {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 5px solid #0078D4;
        padding: 24px;
        border-radius: 10px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        color: #F8FAFC;
        font-size: 32px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: #38BDF8;
        font-size: 16px;
        font-weight: 600;
        margin-top: 4px;
    }
    
    .skills-badge {
        display: inline-block;
        background-color: rgba(0, 120, 212, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(96, 165, 250, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    .header-desc {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 12px;
        line-height: 1.5;
    }
    
    .notice-box {
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px dashed #475569;
        color: #CBD5E1;
        padding: 10px 16px;
        border-radius: 6px;
        font-size: 12px;
        margin-top: 14px;
    }

    /* Metric Cards */
    .metric-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .metric-label {
        color: #94A3B8;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 700;
        margin-top: 4px;
    }
    
    /* Result Header & Cards */
    .result-section {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }
    
    .section-header {
        color: #38BDF8;
        font-size: 20px;
        font-weight: 700;
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
        margin-bottom: 16px;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    .sidebar-section {
        background: #1E293B;
        border: 1px solid #334155;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .sidebar-title {
        color: #38BDF8;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
        text-transform: uppercase;
    }
    
    /* Terminal Block */
    .terminal-box {
        background-color: #020617;
        color: #E2E8F0;
        font-family: "Courier New", Courier, monospace;
        padding: 14px;
        border-radius: 6px;
        border: 1px solid #1E293B;
        font-size: 13px;
        line-height: 1.4;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    /* Button overrides */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #0078D4 0%, #005A9E 100%);
        color: white;
        font-weight: 700;
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 120, 212, 0.4);
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1084DE 0%, #00457E 100%);
        box-shadow: 0 6px 16px rgba(0, 120, 212, 0.6);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">ABOUT THIS PROJECT</div>
        <p style="color: #94A3B8; font-size: 13px; margin: 0;">
            This portfolio project demonstrates automated Kubernetes incident investigation and SRE diagnostic workflows.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">TECH STACK</div>
        <ul style="color: #CBD5E1; font-size: 13px; margin: 0; padding-left: 18px;">
            <li>Python 3.11+</li>
            <li>Streamlit UI</li>
            <li>Azure AKS Concepts</li>
            <li>Kubernetes Signals</li>
            <li>SRE Diagnostics</li>
            <li>AIOps Automation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <div class="sidebar-title">ROADMAP</div>
        <div style="font-size: 12px; color: #CBD5E1;">
            <p style="margin: 4px 0;"><strong>V1:</strong> Deterministic incident analysis (Active)</p>
            <p style="margin: 4px 0; color: #64748B;"><strong>V2:</strong> LLM-assisted reasoning</p>
            <p style="margin: 4px 0; color: #64748B;"><strong>V3:</strong> Read-only AKS integration</p>
            <p style="margin: 4px 0; color: #64748B;"><strong>V4:</strong> Azure Monitor + Log Analytics + RAG</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section" style="border-left: 3px solid #F59E0B;">
        <div class="sidebar-title" style="color: #F59E0B;">ENGINEERING SAFETY</div>
        <p style="color: #CBD5E1; font-size: 12px; margin: 0;">
            Recommendations are advisory. Engineers should validate evidence and commands before executing remediation in a production environment.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Application Header
# ---------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div class="header-title">AI Ops Incident Investigator</div>
    <div class="header-subtitle">Built by Anmol</div>
    <div class="skills-badge">Azure • AKS • Kubernetes • SRE • Python • AI</div>
    <div class="header-desc">
        An AI-ready Kubernetes incident investigation platform that analyzes operational signals, 
        identifies probable root causes, and recommends diagnostic and remediation actions.
    </div>
    <div class="notice-box">
        🔒 <strong>Portfolio Demonstration:</strong> Uses simulated Kubernetes operational telemetry. No production systems or confidential data are accessed.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Main Dashboard Metrics
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Incidents Analyzed</div>
        <div class="metric-value" style="color: #38BDF8;">5</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Platform</div>
        <div class="metric-value" style="color: #60A5FA;">AKS</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Analysis Engine</div>
        <div class="metric-value" style="color: #34D399;">Python</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Mode</div>
        <div class="metric-value" style="color: #FBBF24;">Simulation</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Incident Selection & Details
# ---------------------------------------------------------
incident_options = {
    "1. CrashLoopBackOff": "CrashLoopBackOff",
    "2. OOMKilled": "OOMKilled",
    "3. ImagePullBackOff": "ImagePullBackOff",
    "4. Readiness Probe Failure": "Readiness Probe Failure",
    "5. PVC Pending": "PVC Pending"
}

selected_option = st.selectbox(
    "Select Kubernetes Incident",
    options=list(incident_options.keys()),
    index=0,
    help="Select a simulated incident scenario to view telemetry and execute diagnostic analysis."
)

incident_key = incident_options[selected_option]
current_incident = INCIDENTS[incident_key]

st.markdown("<br>", unsafe_allow_html=True)

# Incident Overview & Details Cards
with st.container():
    st.markdown(f"### Incident Telemetry: {current_incident['title']}")
    
    # Metadata pills
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.info(f"**Pod Name:** `{current_incident['pod_name']}`")
    with m_col2:
        st.info(f"**Namespace:** `{current_incident['namespace']}`")
    with m_col3:
        status_color = "red" if "Crash" in current_incident['status'] or "OOM" in current_incident['status'] else "orange"
        if status_color == "red":
            st.error(f"**Status:** `{current_incident['status']}`")
        else:
            st.warning(f"**Status:** `{current_incident['status']}`")
    with m_col4:
        st.info(f"**Target Node:** `{current_incident['node']}`")

    # Status Brief Banner
    st.markdown(f"""
    <div style="background-color: rgba(56, 189, 248, 0.08); border-left: 4px solid #38BDF8; padding: 12px 16px; border-radius: 6px; margin: 12px 0 16px 0; font-size: 13px; color: #E2E8F0;">
        💡 <strong>Status Brief ({current_incident['status']}):</strong> {current_incident['status_brief']}
    </div>
    """, unsafe_allow_html=True)

    # Tabs for structured viewing
    tab_desc, tab_pod, tab_events, tab_logs = st.tabs([
        "Incident Description", 
        "Pod Status", 
        "Kubernetes Events", 
        "Application Logs"
    ])
    
    with tab_desc:
        st.write(current_incident['description'])
    
    with tab_pod:
        st.code(current_incident['pod_details'], language="text")
        
    with tab_events:
        # Display events table / formatted list
        st.dataframe(
            current_incident['events'],
            use_container_width=True,
            column_config={
                "time": "Age",
                "type": "Type",
                "reason": "Reason",
                "object": "Object",
                "message": "Message"
            }
        )
        
    with tab_logs:
        st.code(current_incident['logs'], language="log")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Analyze Button & State Handling
# ---------------------------------------------------------
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    analyze_clicked = st.button("Analyze Incident", type="primary", use_container_width=True)

# Store selected incident analysis state
if "analyzed_incidents" not in st.session_state:
    st.session_state.analyzed_incidents = set()

if analyze_clicked:
    st.session_state.analyzed_incidents.add(incident_key)

# Render Analysis Results if button clicked for current incident
if incident_key in st.session_state.analyzed_incidents:
    analysis = analyze_incident(current_incident)
    
    st.markdown("""<div class="result-section">""", unsafe_allow_html=True)
    st.markdown('<div class="section-header">INVESTIGATION RESULT</div>', unsafe_allow_html=True)
    
    # 1. Confidence & Severity Metrics
    res_m1, res_m2, res_m3 = st.columns([1, 1, 2])
    with res_m1:
        st.metric("1. Confidence", analysis["confidence"])
    with res_m2:
        st.metric("Severity", analysis["severity"])
    with res_m3:
        st.metric("Engine", "Automated Incident Analysis (Deterministic V1)")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Probable Root Cause
    st.markdown("#### 2. Probable Root Cause")
    st.error(f"**{analysis['root_cause']}**")

    # 3. Supporting Evidence
    st.markdown("#### 3. Supporting Evidence")
    for ev in analysis["evidence"]:
        st.markdown(f"• {ev}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Recommended Actions
    st.markdown("#### 4. Recommended Actions")
    for idx, act in enumerate(analysis["actions"], start=1):
        st.markdown(f"**{idx}.** {act}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Diagnostic Commands
    st.markdown("#### 5. Diagnostic Commands")
    cmd_text = "\n".join(analysis["commands"])
    st.code(cmd_text, language="bash")

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. Generated RCA
    st.markdown("#### 6. Generated Root Cause Analysis (RCA)")
    rca = analysis["rca"]
    
    with st.expander("📄 View & Export Full SRE Root Cause Analysis (RCA) Report", expanded=True):
        st.markdown(f"### {rca['incident_title']}")
        st.markdown(f"**Impact:** {rca['impact']}")
        st.markdown(f"**Observed Symptoms:** {rca['observed_symptoms']}")
        st.markdown(f"**Probable Root Cause:** {rca['probable_root_cause']}")
        
        st.markdown("**Supporting Evidence:**")
        for item in rca['supporting_evidence']:
            st.markdown(f"- {item}")
            
        st.markdown("**Recommended Resolution:**")
        for item in rca['recommended_resolution']:
            st.markdown(f"- {item}")
            
        st.markdown("**Validation Steps:**")
        for item in rca['validation_steps']:
            st.markdown(f"- {item}")
            
        st.markdown("**Preventive Actions:**")
        for item in rca['preventive_actions']:
            st.markdown(f"- {item}")

        # Markdown Export string generator
        rca_md = f"""# SRE Incident Report: {rca['incident_title']}

## Impact
{rca['impact']}

## Observed Symptoms
{rca['observed_symptoms']}

## Probable Root Cause
{rca['probable_root_cause']}

## Supporting Evidence
{chr(10).join(['- ' + e for e in rca['supporting_evidence']])}

## Recommended Resolution
{chr(10).join(['- ' + r for r in rca['recommended_resolution']])}

## Validation Steps
{chr(10).join(['- ' + v for v in rca['validation_steps']])}

## Preventive Actions
{chr(10).join(['- ' + p for p in rca['preventive_actions']])}

---
Generated by Anmol AI Ops Incident Investigator
"""
        st.download_button(
            label="Download RCA Report (.md)",
            data=rca_md,
            file_name=f"RCA_{current_incident['id']}.md",
            mime="text/markdown"
        )

    st.markdown("</div>", unsafe_allow_html=True)
