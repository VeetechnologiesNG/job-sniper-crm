"""
Job Sniper CRM Database Queries
Handles all CRUD operations for applications, 3-track daily quotas, and interview tracking.
"""
from datetime import datetime, date
from database.connection import get_connection
from config import DEFAULT_DAILY_QUOTA

def add_application(data: dict) -> int:
    """Inserts a new job application and returns the new ID."""
    conn = get_connection()
    try:
        now = datetime.now()
        date_applied = data.get("date_applied", now.strftime("%Y-%m-%d"))
        time_applied = data.get("time_applied", now.strftime("%H:%M:%S"))
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO applications (
                date_applied, time_applied, track, platform, company_name,
                job_title, job_url, salary_offered, cv_used, pitch_sent,
                status, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date_applied,
            time_applied,
            data.get("track", "track_a_tech"),
            data.get("platform", "Other"),
            data.get("company_name", "").strip(),
            data.get("job_title", "").strip(),
            data.get("job_url", "").strip(),
            data.get("salary_offered", "").strip(),
            data.get("cv_used", "Technical_Engineering_CV"),
            data.get("pitch_sent", ""),
            data.get("status", "Applied"),
            data.get("notes", ""),
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_all_applications(track=None, platform=None, status=None, search=None, date_applied=None, date_from=None, date_to=None, limit=500) -> list:
    """Fetches applications with optional filtering."""
    conn = get_connection()
    try:
        query = "SELECT * FROM applications WHERE 1=1"
        params = []
        
        if track and track != "All":
            query += " AND track = ?"
            params.append(track)
        if platform and platform != "All":
            query += " AND platform = ?"
            params.append(platform)
        if status and status != "All":
            query += " AND status = ?"
            params.append(status)
        if date_applied:
            query += " AND date_applied = ?"
            params.append(date_applied)
        if date_from:
            query += " AND date_applied >= ?"
            params.append(date_from)
        if date_to:
            query += " AND date_applied <= ?"
            params.append(date_to)
        if search:
            query += " AND (company_name LIKE ? OR job_title LIKE ? OR notes LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])
            
        query += " ORDER BY date_applied DESC, time_applied DESC LIMIT ?"
        params.append(limit)
        
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_application_by_id(app_id: int) -> dict:
    """Fetches a single application by ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def update_application_status(app_id: int, new_status: str, notes: str = None) -> bool:
    """Updates the status and optional notes of an application."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if notes is not None:
            cursor.execute("""
                UPDATE applications 
                SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_status, notes, app_id))
        else:
            cursor.execute("""
                UPDATE applications 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_status, app_id))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def delete_application(app_id: int) -> bool:
    """Deletes an application by ID."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_or_create_daily_quota(target_date: str = None) -> dict:
    """Gets or initializes the 3-track quota record for a given date, synced to DEFAULT_DAILY_QUOTA."""
    if not target_date:
        target_date = date.today().strftime("%Y-%m-%d")
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_quotas WHERE date = ?", (target_date,))
        row = cursor.fetchone()
        
        if not row:
            cursor.execute("""
                INSERT INTO daily_quotas (
                    date, target_track_a, target_track_b, target_track_c,
                    target_wellfound_a, target_himalayas_a,
                    target_himalayas_b, target_other_b
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                target_date,
                DEFAULT_DAILY_QUOTA["track_a_total"],
                DEFAULT_DAILY_QUOTA["track_b_total"],
                DEFAULT_DAILY_QUOTA["track_c_total"],
                DEFAULT_DAILY_QUOTA["wellfound_track_a"],
                DEFAULT_DAILY_QUOTA["himalayas_track_a"],
                DEFAULT_DAILY_QUOTA["himalayas_track_b"],
                DEFAULT_DAILY_QUOTA["other_track_b"],
            ))
            conn.commit()
            cursor.execute("SELECT * FROM daily_quotas WHERE date = ?", (target_date,))
            row = cursor.fetchone()
        elif (row["target_track_a"] != DEFAULT_DAILY_QUOTA["track_a_total"] or
              row["target_track_b"] != DEFAULT_DAILY_QUOTA["track_b_total"] or
              row["target_track_c"] != DEFAULT_DAILY_QUOTA["track_c_total"]):
            cursor.execute("""
                UPDATE daily_quotas
                SET target_track_a = ?, target_track_b = ?, target_track_c = ?,
                    target_wellfound_a = ?, target_himalayas_a = ?,
                    target_himalayas_b = ?, target_other_b = ?
                WHERE date = ?
            """, (
                DEFAULT_DAILY_QUOTA["track_a_total"],
                DEFAULT_DAILY_QUOTA["track_b_total"],
                DEFAULT_DAILY_QUOTA["track_c_total"],
                DEFAULT_DAILY_QUOTA["wellfound_track_a"],
                DEFAULT_DAILY_QUOTA["himalayas_track_a"],
                DEFAULT_DAILY_QUOTA["himalayas_track_b"],
                DEFAULT_DAILY_QUOTA["other_track_b"],
                target_date,
            ))
            conn.commit()
            cursor.execute("SELECT * FROM daily_quotas WHERE date = ?", (target_date,))
            row = cursor.fetchone()
            
        return dict(row)
    finally:
        conn.close()

def get_daily_progress(target_date: str = None) -> dict:
    """Calculates applied counts versus target quotas across Track A, Track B, and Track C."""
    if not target_date:
        target_date = date.today().strftime("%Y-%m-%d")
        
    quota = get_or_create_daily_quota(target_date)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Track A counts
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_a_tech'
        """, (target_date,))
        applied_a = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_a_tech' AND platform = 'Wellfound'
        """, (target_date,))
        applied_wf_a = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_a_tech' AND platform = 'Himalayas'
        """, (target_date,))
        applied_him_a = cursor.fetchone()[0]
        
        applied_other_a = max(0, applied_a - applied_wf_a - applied_him_a)
        
        # Track B counts
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_b_basic'
        """, (target_date,))
        applied_b = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_b_basic' AND platform = 'Himalayas'
        """, (target_date,))
        applied_him_b = cursor.fetchone()[0]
        
        applied_other_b = max(0, applied_b - applied_him_b)
        
        # Track C counts
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_c_gigs'
        """, (target_date,))
        applied_c = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM applications 
            WHERE date_applied = ? AND track = 'track_c_gigs' AND platform = 'ProBlogger'
        """, (target_date,))
        applied_pb_c = cursor.fetchone()[0]
        
        applied_other_c = max(0, applied_c - applied_pb_c)
        
        total_applied = applied_a + applied_b + applied_c
        total_target = quota["target_track_a"] + quota["target_track_b"] + quota["target_track_c"]
        
        return {
            "date": target_date,
            "applied_track_a": applied_a,
            "target_track_a": quota["target_track_a"],
            "applied_wellfound_a": applied_wf_a,
            "target_wellfound_a": quota["target_wellfound_a"],
            "applied_himalayas_a": applied_him_a,
            "target_himalayas_a": quota["target_himalayas_a"],
            "applied_other_a": applied_other_a,
            
            "applied_track_b": applied_b,
            "target_track_b": quota["target_track_b"],
            "applied_himalayas_b": applied_him_b,
            "target_himalayas_b": quota["target_himalayas_b"],
            "applied_other_b": applied_other_b,
            "target_other_b": quota["target_other_b"],
            
            "applied_track_c": applied_c,
            "target_track_c": quota["target_track_c"],
            "applied_problogger_c": applied_pb_c,
            "applied_other_c": applied_other_c,
            
            "total_applied": total_applied,
            "total_target": total_target,
            "quota_met": total_applied >= total_target,
        }
    finally:
        conn.close()

def add_interview(data: dict) -> int:
    """Saves a new interview appointment."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO interviews (
                application_id, interview_date, interview_time,
                interviewer_name, stage, meeting_link, notes, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["application_id"],
            data.get("interview_date", date.today().strftime("%Y-%m-%d")),
            data.get("interview_time", "10:00 AM"),
            data.get("interviewer_name", ""),
            data.get("stage", "Screening"),
            data.get("meeting_link", ""),
            data.get("notes", ""),
            data.get("status", "Scheduled"),
        ))
        
        cursor.execute("""
            UPDATE applications SET status = 'Interview Booked', updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (data["application_id"],))
        
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_upcoming_interviews() -> list:
    """Fetches scheduled upcoming interviews with parent application details."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.*, a.company_name, a.job_title, a.track, a.platform
            FROM interviews i
            JOIN applications a ON i.application_id = a.id
            WHERE i.status = 'Scheduled'
            ORDER BY i.interview_date ASC, i.interview_time ASC
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def seed_initial_applications():
    """Seeds initial applications if empty."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM applications")
        count = cursor.fetchone()[0]
        if count > 0:
            return
    finally:
        conn.close()
