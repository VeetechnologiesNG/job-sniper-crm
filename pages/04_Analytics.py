"""
Page 4: Analytics & Funnel Conversion
Visualizes conversion rates, platform distribution, and interview outcomes across 3 tracks.
"""
import streamlit as st
import pandas as pd
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database.queries import get_all_applications

st.title("📈 Career Acquisition Analytics")
st.caption("Measure your pipeline conversion rates, platform velocity, and interview yield across Track A, Track B, and Track C.")

apps = get_all_applications(limit=1000)

if not apps:
    st.info("No applications logged yet. Once you log applications, analytics will appear here.")
else:
    df = pd.DataFrame(apps)
    
    total_apps = len(df)
    interviews_count = len(df[df["status"] == "Interview Booked"])
    assessments_count = len(df[df["status"] == "Take-Home / Assessment"])
    offers_count = len(df[df["status"] == "Offer Accepted"])
    
    interview_rate = (interviews_count / max(1, total_apps)) * 100
    
    # High-level Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Applications", total_apps)
    with m2:
        st.metric("Interviews Booked", interviews_count, delta=f"{interview_rate:.1f}% Yield")
    with m3:
        st.metric("Take-Home Assessments", assessments_count)
    with m4:
        st.metric("Offers Accepted", offers_count)
        
    st.divider()
    
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.subheader("Distribution by Track")
        track_counts = df["track"].value_counts().reset_index()
        track_counts.columns = ["Track", "Count"]
        track_counts["Track"] = track_counts["Track"].replace({
            "track_a_tech": "Track A: Tech Support / IT / QA",
            "track_b_basic": "Track B: Basic Support & Ops",
            "track_c_gigs": "Track C: Writing & Gigs",
            "engineering": "Track A: Tech Support / IT / QA",
            "basic_cashflow": "Track B: Basic Support & Ops"
        })
        st.bar_chart(data=track_counts.set_index("Track"))
        
    with col_chart2:
        st.subheader("Applications by Platform")
        plat_counts = df["platform"].value_counts().reset_index()
        plat_counts.columns = ["Platform", "Count"]
        st.bar_chart(data=plat_counts.set_index("Platform"))
        
    st.divider()
    
    st.subheader("Status Breakdown Table")
    status_summary = df.groupby(["track", "status"]).size().unstack(fill_value=0)
    st.dataframe(status_summary, use_container_width=True)
