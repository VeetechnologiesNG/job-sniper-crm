PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS applications (
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
);

CREATE TABLE IF NOT EXISTS daily_quotas (
    date TEXT PRIMARY KEY,
    target_track_a INTEGER DEFAULT 9,
    target_track_b INTEGER DEFAULT 10,
    target_track_c INTEGER DEFAULT 4,
    target_wellfound_a INTEGER DEFAULT 6,
    target_himalayas_a INTEGER DEFAULT 3,
    target_himalayas_b INTEGER DEFAULT 3,
    target_other_b INTEGER DEFAULT 7
);

CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    interview_date TEXT NOT NULL,
    interview_time TEXT,
    interviewer_name TEXT,
    stage TEXT DEFAULT 'Screening',
    meeting_link TEXT,
    notes TEXT,
    status TEXT DEFAULT 'Scheduled',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_apps_date ON applications(date_applied);
CREATE INDEX IF NOT EXISTS idx_apps_track ON applications(track);
CREATE INDEX IF NOT EXISTS idx_apps_platform ON applications(platform);
CREATE INDEX IF NOT EXISTS idx_apps_status ON applications(status);
