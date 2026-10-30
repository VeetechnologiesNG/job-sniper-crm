"""
Database Connection Manager
Provides SQLite connection with WAL mode and automatic 3-track migration.
"""
import os
import sqlite3
from config import DB_PATH, DATA_DIR, SCHEMA_PATH, DEFAULT_DAILY_QUOTA

def get_connection():
    """Returns a thread-safe connection to the SQLite database with WAL mode enabled."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes the database schema and synchronizes daily quotas with active config targets."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = get_connection()
    try:
        cursor = conn.cursor()
        # Check if applications table exists and has old CHECK constraint
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='applications'")
        row = cursor.fetchone()
        if row and "basic_cashflow" in (row["sql"] or ""):
            cursor.execute("PRAGMA foreign_keys = OFF;")
            cursor.execute("""
                CREATE TABLE applications_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_applied TEXT NOT NULL,
                    time_applied TEXT NOT NULL,
                    track TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    company_name TEXT NOT NULL,
                    job_title TEXT NOT NULL,
                    job_url TEXT,
                    salary_offered TEXT,
                    cv_used TEXT NOT NULL,
                    pitch_sent TEXT,
                    status TEXT NOT NULL DEFAULT 'Applied',
                    notes TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                INSERT INTO applications_new (
                    id, date_applied, time_applied, track, platform, company_name,
                    job_title, job_url, salary_offered, cv_used, pitch_sent, status, notes, created_at, updated_at
                )
                SELECT
                    id, date_applied, time_applied,
                    CASE
                        WHEN track = 'engineering' THEN 'track_a_tech'
                        WHEN platform IN ('ProBlogger', 'BloggingPro', 'ModSquad / Influx') THEN 'track_c_gigs'
                        ELSE 'track_b_basic'
                    END,
                    platform, company_name, job_title, job_url, salary_offered,
                    cv_used, pitch_sent, status, notes, created_at, updated_at
                FROM applications
            """)
            cursor.execute("DROP TABLE applications")
            cursor.execute("ALTER TABLE applications_new RENAME TO applications")
            cursor.execute("PRAGMA foreign_keys = ON;")

        # Check if daily_quotas has old columns
        cursor.execute("PRAGMA table_info(daily_quotas)")
        cols = [c["name"] for c in cursor.fetchall()]
        if cols and "target_track_a" not in cols:
            cursor.execute("DROP TABLE daily_quotas")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

        # Synchronize all daily_quotas rows to active DEFAULT_DAILY_QUOTA targets
        cursor.execute("""
            UPDATE daily_quotas
            SET target_track_a = ?,
                target_track_b = ?,
                target_track_c = ?,
                target_wellfound_a = ?,
                target_himalayas_a = ?,
                target_himalayas_b = ?,
                target_other_b = ?
        """, (
            DEFAULT_DAILY_QUOTA["track_a_total"],
            DEFAULT_DAILY_QUOTA["track_b_total"],
            DEFAULT_DAILY_QUOTA["track_c_total"],
            DEFAULT_DAILY_QUOTA["wellfound_track_a"],
            DEFAULT_DAILY_QUOTA["himalayas_track_a"],
            DEFAULT_DAILY_QUOTA["himalayas_track_b"],
            DEFAULT_DAILY_QUOTA["other_track_b"],
        ))

        conn.commit()
    finally:
        conn.close()
