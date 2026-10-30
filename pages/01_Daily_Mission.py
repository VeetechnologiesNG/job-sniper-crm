"""
Page 1: Daily Mission Control
Live quota tracker and quick application logging form across Track A, Track B, and Track C.
"""
import streamlit as st
from datetime import date
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database.queries import add_application, get_all_applications, update_application_status, delete_application
from services.quota_service import get_today_summary
from config import STATUS_CHOICES, TRACK_LABELS

st.title("📋 Daily Mission Control")
st.caption("Log your applications and hit your 23 daily targets across Track A (9), Track B (10), and Track C (4).")

today_str = date.today().strftime("%Y-%m-%d")
summary = get_today_summary()

# Quota Meters (4 columns)
col_tot, col_a, col_b, col_c = st.columns(4)
with col_tot:
    st.metric(
        label="Total Daily Applications",
        value=f"{summary['total_applied']} / {summary['total_target']}",
        delta=f"{summary['total_remaining']} to go" if summary['total_remaining'] > 0 else "Goal Met!"
    )
    st.progress(summary['total_pct'] / 100)

with col_a:
    st.metric(
        label="Track A: Tech Support / IT / QA",
        value=f"{summary['applied_track_a']} / {summary['target_track_a']}",
        delta=f"Wellfound: {summary['applied_wellfound_a']}/10 | Himalayas: {summary['applied_himalayas_a']}/5"
    )
    st.progress(summary['track_a_pct'] / 100)

with col_b:
    st.metric(
        label="Track B: Basic Support & Ops",
        value=f"{summary['applied_track_b']} / {summary['target_track_b']}",
        delta=f"Himalayas: {summary['applied_himalayas_b']}/4"
    )
    st.progress(summary['track_b_pct'] / 100)

with col_c:
    st.metric(
        label="Track C: Writing & Fast Gigs",
        value=f"{summary['applied_track_c']} / {summary['target_track_c']}",
        delta="BloggingPro (2) | ProBlogger (1) | ModSquad (1)"
    )
    st.progress(summary['track_c_pct'] / 100)

st.divider()

# Quick Log Form
st.subheader("⚡ Quick Log Application")

with st.form("quick_log_form", clear_on_submit=True):
    row1_c1, row1_c2, row1_c3 = st.columns([1, 1, 1])
    
    with row1_c1:
        track = st.selectbox(
            "Target Track*",
            options=["track_a_tech", "track_b_basic", "track_c_gigs"],
            format_func=lambda x: TRACK_LABELS.get(x, x)
        )
    with row1_c2:
        platform = st.selectbox(
            "Platform*",
            options=[
                "Wellfound", "Himalayas", "BloggingPro", "ProBlogger", "MotionArt / ModSquad", "Other"
            ]
        )
    with row1_c3:
        status = st.selectbox("Current Status", options=STATUS_CHOICES, index=0)

    row2_c1, row2_c2 = st.columns([1, 1])
    with row2_c1:
        company_name = st.text_input("Company Name*", placeholder="e.g. REWORKIO, Keygate, Supabase, Modular Agency")
    with row2_c2:
        job_title = st.text_input("Job Title*", placeholder="e.g. Technical Support Specialist, Manual QA, Customer Support")

    row3_c1, row3_c2 = st.columns([1, 1])
    with row3_c1:
        job_url = st.text_input("Job / Application URL", placeholder="https://...")
    with row3_c2:
        salary_offered = st.text_input("Salary / Compensation Offered", placeholder="e.g. $2,500/mo, $1,500/mo, $150/article")

    row4_c1, row4_c2 = st.columns([1, 1])
    with row4_c1:
        cv_used = st.selectbox(
            "CV Attached",
            options=["Technical_Engineering_CV", "Operations_VA_Resume", "Other"],
            index=0 if track == "track_a_tech" else 1
        )
    with row4_c2:
        notes = st.text_input("Notes / Pitch Highlights", placeholder="e.g. Highlighted CS background, Windows troubleshooting, 24/7 solar power")

    submitted = st.form_submit_button("Record Application", use_container_width=True)
    if submitted:
        if not company_name or not job_title:
            st.error("Please provide both Company Name and Job Title.")
        else:
            new_id = add_application({
                "date_applied": today_str,
                "track": track,
                "platform": platform,
                "company_name": company_name,
                "job_title": job_title,
                "job_url": job_url,
                "salary_offered": salary_offered,
                "cv_used": cv_used,
                "status": status,
                "notes": notes,
            })
            st.success(f"Recorded! Application #{new_id} ({company_name} : {job_title}) saved.")
            st.rerun()

st.divider()

# Today's Applications Table
st.subheader(f"📅 Applications Submitted Today ({today_str})")
today_apps = get_all_applications(date_from=today_str, date_to=today_str)

if not today_apps:
    st.info("No applications logged for today yet. Use the form above to log your first job!")
else:
    for app in today_apps:
        with st.container():
            c_info, c_status, c_act = st.columns([3, 1, 1])
            with c_info:
                if app["track"] == "track_a_tech":
                    track_badge = "🛠️ Track A: Tech Support / IT / QA"
                elif app["track"] == "track_c_gigs":
                    track_badge = "✍️ Track C: Writing & Gigs"
                else:
                    track_badge = "⚡ Track B: Basic Support & Ops"
                st.markdown(f"**{app['company_name']}** : {app['job_title']} `[{track_badge}]`")
                st.caption(f"Platform: **{app['platform']}** | Salary: {app['salary_offered'] or 'Unlisted'} | CV: `{app['cv_used']}`")
                if app["job_url"]:
                    st.caption(f"[View Posting]({app['job_url']})")
            
            with c_status:
                current_st = app["status"]
                new_st = st.selectbox(
                    "Status",
                    options=STATUS_CHOICES,
                    index=STATUS_CHOICES.index(current_st) if current_st in STATUS_CHOICES else 0,
                    key=f"status_today_{app['id']}"
                )
                if new_st != current_st:
                    update_application_status(app["id"], new_st)
                    st.success("Updated!")
                    st.rerun()
                    
            with c_act:
                st.write("")
                if st.button("🗑️ Delete", key=f"del_today_{app['id']}"):
                    delete_application(app["id"])
                    st.rerun()
            st.divider()
