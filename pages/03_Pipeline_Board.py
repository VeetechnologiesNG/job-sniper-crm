"""
Page 3: Pipeline & Interview Tracker
Manages the lifecycle of submitted jobs from Applied to Interview Booked and Offer Accepted.
"""
import streamlit as st
from datetime import date
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database.queries import (
    get_all_applications, update_application_status, delete_application,
    add_interview, get_upcoming_interviews
)
from config import STATUS_CHOICES, TRACK_LABELS

st.title("📊 Applications & Interview Pipeline")
st.caption("Track submitted applications across Track A, Track B, and Track C, schedule interviews, and monitor offers.")

# Upcoming Interviews Section
upcoming = get_upcoming_interviews()
if upcoming:
    st.subheader("📅 Active Interview Schedule")
    for iv in upcoming:
        st.info(
            f"**{iv['company_name']}** : {iv['job_title']} `[{iv['stage']}]`\n\n"
            f"• Date & Time: **{iv['interview_date']}** at **{iv['interview_time']}**\n"
            f"• Interviewer: {iv['interviewer_name'] or 'Not specified'} | Link: {iv['meeting_link'] or 'Pending email invite'}\n"
            f"• Notes: {iv['notes'] or 'None'}"
        )
    st.divider()

# Book Interview Expander
with st.expander("➕ Log an Interview Invitation", expanded=False):
    all_apps = get_all_applications(limit=100)
    if not all_apps:
        st.caption("No applications available to attach an interview to.")
    else:
        app_options = {f"#{a['id']} : {a['company_name']} ({a['job_title']})": a['id'] for a in all_apps}
        sel_app_label = st.selectbox("Select Application", options=list(app_options.keys()))
        sel_app_id = app_options[sel_app_label]
        
        c_iv1, c_iv2 = st.columns([1, 1])
        with c_iv1:
            iv_date = st.date_input("Interview Date", value=date.today())
            iv_time = st.text_input("Time & Timezone", value="10:00 AM (CET / US Central)")
            iv_stage = st.selectbox("Stage", options=["Screening", "Technical Support / Ops Walkthrough", "Founder Chat", "Final Offer"])
        with c_iv2:
            iv_name = st.text_input("Interviewer Name / Title", placeholder="e.g. Sarah Jenkins, Head of Support")
            iv_link = st.text_input("Meeting Link", placeholder="https://meet.google.com/...")
            iv_notes = st.text_input("Preparation Notes", placeholder="e.g. Prepare troubleshooting walkthrough and CRM workflow demo")
            
        if st.button("Save Interview", use_container_width=True):
            add_interview({
                "application_id": sel_app_id,
                "interview_date": iv_date.strftime("%Y-%m-%d"),
                "interview_time": iv_time,
                "interviewer_name": iv_name,
                "stage": iv_stage,
                "meeting_link": iv_link,
                "notes": iv_notes,
            })
            st.success("Interview scheduled and application status updated to 'Interview Booked'!")
            st.rerun()

st.divider()

# Filter Bar
st.subheader("📁 Application Pipeline Directory")
f_col1, f_col2, f_col3 = st.columns([1, 1, 2])

with f_col1:
    f_track = st.selectbox(
        "Filter Track",
        options=["All", "track_a_tech", "track_b_basic", "track_c_gigs"],
        format_func=lambda x: "All Tracks" if x == "All" else TRACK_LABELS.get(x, x)
    )
with f_col2:
    f_status = st.selectbox("Filter Status", options=["All"] + STATUS_CHOICES)
with f_col3:
    f_search = st.text_input("Search (Company, Role, Notes)", placeholder="Type to search...")

apps = get_all_applications(
    track=None if f_track == "All" else f_track,
    status=None if f_status == "All" else f_status,
    search=f_search if f_search else None
)

st.write(f"Showing **{len(apps)}** applications:")

if not apps:
    st.info("No applications match the current filter criteria.")
else:
    for a in apps:
        with st.container():
            c1, c2, c3 = st.columns([3, 1, 1])
            with c1:
                if a["track"] == "track_a_tech":
                    track_label = "🛠️ Track A: Tech Support / IT / QA"
                elif a["track"] == "track_c_gigs":
                    track_label = "✍️ Track C: Writing & Gigs"
                else:
                    track_label = "⚡ Track B: Basic Support & Ops"
                st.markdown(f"**#{a['id']} • {a['company_name']}** : {a['job_title']} `[{track_label}]`")
                st.caption(f"Platform: **{a['platform']}** | Applied: {a['date_applied']} | Salary: {a['salary_offered'] or 'Unlisted'}")
                if a["notes"]:
                    st.caption(f"Notes: {a['notes']}")
                if a["job_url"]:
                    st.caption(f"[Job URL]({a['job_url']})")
                    
            with c2:
                cur_status = a["status"]
                new_status = st.selectbox(
                    "Status",
                    options=STATUS_CHOICES,
                    index=STATUS_CHOICES.index(cur_status) if cur_status in STATUS_CHOICES else 0,
                    key=f"pipe_status_{a['id']}"
                )
                if new_status != cur_status:
                    update_application_status(a["id"], new_status)
                    st.success("Status updated!")
                    st.rerun()
                    
            with c3:
                st.write("")
                if st.button("🗑️ Delete", key=f"del_pipe_{a['id']}"):
                    delete_application(a["id"])
                    st.rerun()
            st.divider()
