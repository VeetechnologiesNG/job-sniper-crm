"""
Page 5: Settings & Database Maintenance
Configure daily quotas across Track A, Track B, and Track C, export CSV data, and perform automated database backups.
"""
import streamlit as st
import shutil
from datetime import datetime, date
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from config import DB_PATH, BASE_DIR
from database.connection import get_connection
from database.queries import get_or_create_daily_quota
from services.export_service import export_applications_to_csv

st.title("⚙️ Settings & Data Control")
st.caption("Manage your daily targets across Track A, Track B, and Track C, backup your SQLite database, and export CSV files.")

st.divider()

# Daily Quota Adjustment
st.subheader("🎯 Configure Daily Targets")
today_str = date.today().strftime("%Y-%m-%d")
quota = get_or_create_daily_quota(today_str)

with st.form("quota_config_form"):
    q1, q2, q3 = st.columns([1, 1, 1])
    with q1:
        new_track_a = st.number_input(
            "Track A Target: Tech Support / IT / QA / Day",
            min_value=1,
            max_value=30,
            value=quota.get("target_track_a", 9)
        )
    with q2:
        new_track_b = st.number_input(
            "Track B Target: Basic Support & Ops / Day",
            min_value=1,
            max_value=30,
            value=quota.get("target_track_b", 10)
        )
    with q3:
        new_track_c = st.number_input(
            "Track C Target: Fast Writing & Gigs / Day",
            min_value=1,
            max_value=20,
            value=quota.get("target_track_c", 4)
        )
        
    save_quota = st.form_submit_button("Update Daily Targets", use_container_width=True)
    if save_quota:
        conn = get_connection()
        try:
            conn.execute("""
                UPDATE daily_quotas 
                SET target_track_a = ?, target_track_b = ?, target_track_c = ?
                WHERE date = ?
            """, (new_track_a, new_track_b, new_track_c, today_str))
            conn.commit()
            st.success(f"Targets updated! Total daily quota is now {new_track_a + new_track_b + new_track_c} applications.")
            st.rerun()
        finally:
            conn.close()

st.divider()

# CSV Export Section
st.subheader("📥 Export Applications Data")
st.caption("Download your complete application history as a CSV spreadsheet:")

csv_data = export_applications_to_csv()
if csv_data:
    st.download_button(
        label="Download Applications CSV",
        data=csv_data,
        file_name=f"job_applications_export_{today_str}.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("No applications to export.")

st.divider()

# Database Backup Section
st.subheader("💾 Database Backup & Maintenance")
db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0

st.write(f"**Database Location:** `{DB_PATH}`")
st.write(f"**Database Size:** `{db_size / 1024:.2f} KB`")

if st.button("Create Immediate SQLite Backup", use_container_width=True):
    backup_dir = os.path.join(BASE_DIR, "backups")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"job_tracker_backup_{timestamp}.db")
    shutil.copy2(DB_PATH, backup_path)
    st.success(f"Backup created at: `{backup_path}`")
