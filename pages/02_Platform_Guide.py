"""
Page 2: Platform Guides & Guided Navigator
Step-by-step guidance showing exact filters, pre-filtered links, CV badges, and 1-click pitch templates.
"""
import streamlit as st
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from config import PLATFORMS, PITCH_TEMPLATES, TRACK_LABELS

st.title("🧭 Platform Guides & Search Navigator")
st.caption("Select any platform across Track A, Track B, or Track C to see exact search filters, direct links, and 1-click pitch copy.")

platform_names = list(PLATFORMS.keys())
selected_name = st.selectbox("Select Target Job Board / Platform", options=platform_names, index=0)
guide = PLATFORMS[selected_name]

st.divider()

col_left, col_right = st.columns([1, 1])

with col_left:
    track_title = TRACK_LABELS.get(guide["track"], guide["track"])
    st.subheader(f"{selected_name}")
    st.markdown(f"**Target Track:** `{track_title}`")
    st.markdown(f"**Daily Allocation Target:** `{guide['target_daily']} applications`")
    
    st.write("")
    st.link_button(
        f"🔗 Launch {guide['platform_key']} in Browser →",
        url=guide["url"],
        use_container_width=True
    )
    st.caption(f"Direct Search URL: `{guide['url']}`")
    
    st.write("")
    st.markdown("### 🔍 Required Search Filters")
    st.markdown("Set these exact options on the site before browsing to avoid manual coding tests, geofenced jobs, or low-ball listings:")
    for f in guide["filters"]:
        st.markdown(f"• **{f}**")
        
    st.write("")
    st.markdown("### 📄 Mandatory CV Attachment")
    if guide["track"] == "track_a_tech":
        st.success(f"**Use:** {guide['cv_recommended']}")
        st.caption("Best for Technical Support, IT Helpdesk, Manual QA, Solutions Engineer, and AI Operations roles.")
    else:
        st.warning(f"**Use:** {guide['cv_recommended']}")
        st.caption("Best for Customer Support, Executive VA, Lead Gen, and Content Writing roles.")
    st.code(guide["cv_path"], language="text")

with col_right:
    st.subheader("📝 Tailored Pitch Generator")
    st.caption("Enter the target company and title to generate a personalized pitch ready to send:")
    
    default_role = (
        "Technical Support Specialist" if guide["track"] == "track_a_tech"
        else ("Content Writer" if guide["track"] == "track_c_gigs" else "Customer Support Specialist")
    )
    c_comp = st.text_input("Company Name", value="The Team", key=f"pitch_comp_{selected_name}")
    c_role = st.text_input("Role Title", value=default_role, key=f"pitch_role_{selected_name}")
    
    raw_pitch = PITCH_TEMPLATES.get(guide["pitch_key"], "")
    formatted_pitch = raw_pitch.format(company=c_comp, title=c_role)
    
    st.write("**Copy-Paste Application Note:**")
    st.text_area("Pitch Note", value=formatted_pitch, height=280, key=f"pitch_area_{selected_name}")
    st.caption("Click into the box above and press Ctrl+A, then Ctrl+C to copy.")
