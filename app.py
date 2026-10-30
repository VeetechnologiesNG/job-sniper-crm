"""
Job Sniper CRM - Main Entrypoint
Local-first application management engine enforcing the 23-application 3-track daily workflow.
"""
import streamlit as st
import os
import sys

# Ensure local modules are found
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database.connection import init_db
from database.queries import seed_initial_applications, get_upcoming_interviews
from services.quota_service import get_today_summary
from config import CANDIDATE, TECH_CV_PATH, OPS_CV_PATH

st.set_page_config(
    page_title="Job Sniper CRM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database and seed if first run
init_db()
seed_initial_applications()

# Custom Styling (Dark-mode, sleek, compact)
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 1.85rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-sub {
        color: #38bdf8;
        font-size: 0.8rem;
        margin-top: 2px;
    }
    .alert-banner {
        background-color: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎯 Job Sniper CRM")
    st.caption("23-Application 3-Track Acquisition Engine")
    st.divider()
    
    st.write(f"**Candidate:** {CANDIDATE['name']}")
    st.write(f"**Email:** `{CANDIDATE['email']}`")
    st.write(f"**Location:** {CANDIDATE['location']}")
    st.divider()
    
    st.subheader("📄 Quick CV References")
    st.caption("Track A CV (Tech Support / IT / QA / AI Ops):")
    st.code(TECH_CV_PATH, language="text")
    st.caption("Track B & C Resume (Ops / Support / Writing):")
    st.code(OPS_CV_PATH, language="text")
    st.divider()
    
    st.caption("Active Setup: 24/7 Solar Power Backup • Redundant Fiber")

# Main Content Header
today_data = get_today_summary()

st.title("🚀 Career Mission Control")
st.markdown(
    f"""
    <div class="alert-banner">
        <strong>Daily Quota Target:</strong> 23 Total Applications (9 Track A Tech Support/IT/QA/AI Ops + 10 Track B Basic Ops/Support + 4 Track C Fast Writing & Gigs).
        Currently logged today: <strong>{today_data['total_applied']} / {today_data['total_target']}</strong>.
    </div>
    """,
    unsafe_allow_html=True
)

# 4 Primary Progress Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Overall Daily Quota</div>
        <div class="metric-value">{today_data['total_applied']} / {today_data['total_target']}</div>
        <div class="metric-sub">{today_data['total_pct']}% Completed ({today_data['total_remaining']} remaining)</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(today_data['total_pct'] / 100)

with col2:
    sub_a = f"Wellfound: {today_data['applied_wellfound_a']}/{today_data['target_wellfound_a']} • Himalayas: {today_data['applied_himalayas_a']}/{today_data['target_himalayas_a']}"
    if today_data.get('applied_other_a', 0) > 0:
        sub_a += f" • Other: {today_data['applied_other_a']}"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Track A: Tech Support, IT & QA ($1.5k-$4k)</div>
        <div class="metric-value">{today_data['applied_track_a']} / {today_data['target_track_a']}</div>
        <div class="metric-sub">{sub_a}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(today_data['track_a_pct'] / 100)

with col3:
    sub_b = f"Himalayas: {today_data['applied_himalayas_b']}/{today_data['target_himalayas_b']} • Direct ATS / Other: {today_data['applied_other_b']}/{today_data['target_other_b']}"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Track B: Basic Support & Ops ($800-$2k)</div>
        <div class="metric-value">{today_data['applied_track_b']} / {today_data['target_track_b']}</div>
        <div class="metric-sub">{sub_b}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(today_data['track_b_pct'] / 100)

with col4:
    sub_c = f"ProBlogger: {today_data.get('applied_problogger_c', 0)}/2 • Gigs: {today_data.get('applied_other_c', 0)}/2"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Track C: Writing & Fast Gigs ($50-$200/item)</div>
        <div class="metric-value">{today_data['applied_track_c']} / {today_data['target_track_c']}</div>
        <div class="metric-sub">{sub_c}</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(today_data['track_c_pct'] / 100)

st.write("")

# Upcoming Interviews Alert
interviews = get_upcoming_interviews()
if interviews:
    st.subheader("🗓️ Scheduled Interviews")
    for iv in interviews:
        st.info(
            f"**{iv['company_name']}** : {iv['job_title']} `[{iv['stage']}]`\n\n"
            f"• Date & Time: **{iv['interview_date']}** at **{iv['interview_time']}**\n"
            f"• Interviewer: {iv['interviewer_name'] or 'Not specified'} | Link: {iv['meeting_link'] or 'Pending email invite'}\n"
            f"• Notes: {iv['notes'] or 'None'}"
        )
    st.divider()

# Quick Navigation & Action Guide
c_nav1, c_nav2, c_nav3 = st.columns(3)

with c_nav1:
    st.markdown("### 📋 1. Daily Mission")
    st.write("Track live quota progress and log today's applications across all 3 tracks.")
    st.page_link("pages/01_Daily_Mission.py", label="Open Daily Mission Control →", icon="📋")

with c_nav2:
    st.markdown("### 🧭 2. Platform Guides")
    st.write("Access direct search links, required keyword filters, and 1-click tailored pitch notes.")
    st.page_link("pages/02_Platform_Guide.py", label="Open Platform Guide →", icon="🧭")

with c_nav3:
    st.markdown("### 📊 3. Pipeline Board")
    st.write("Manage active applications, update candidate status, and schedule interview invitations.")
    st.page_link("pages/03_Pipeline_Board.py", label="Open Pipeline Board →", icon="📊")
