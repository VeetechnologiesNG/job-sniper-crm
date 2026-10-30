"""
Job Sniper CRM Configuration
Defines default daily quotas across Track A (Tech Support/IT/QA/AI Ops), Track B (Basic Operations & Customer Support),
and Track C (Fast Writing & Crowdsource Gigs).
Permanently eliminates predatory paywall platforms (Remotive, We Work Remotely).
Consolidates all applications onto 100% verified free direct boards:
- Wellfound: 10/day (Track A)
- Himalayas: 9/day (5 Track A + 4 Track B)
- Track C Gigs: 4/day (BloggingPro 2, ProBlogger 1, MotionArt/ModSquad 1)
Total: 23/day
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "job_tracker.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

# CV Library Paths
CV_DIR = r"C:\Users\YungVee\Documents\smiper crm\CV_Library"
TECH_CV_PATH = os.path.join(CV_DIR, "01_Technical_Engineering_CVs", "Muhammed_Nafiu_Technical_Support_Operations_CV.pdf")
OPS_CV_PATH = os.path.join(CV_DIR, "02_Operations_VA_Support_CVs", "Muhammed_Nafiu_Resume.pdf")
DOWNLOADS_DIR = r"C:\Users\YungVee\Downloads"

# Daily Target Settings (23 Total: 15 Track A + 4 Track B + 4 Track C)
DEFAULT_DAILY_QUOTA = {
    "track_a_total": 15,
    "track_b_total": 4,
    "track_c_total": 4,
    "total": 23,
    "wellfound_track_a": 10,
    "himalayas_track_a": 5,
    "himalayas_track_b": 4,
    "other_track_b": 0,
}

# Candidate Profile Constants
CANDIDATE = {
    "name": "Muhammed Nafiu",
    "email": "nafiu@getveetech.com",
    "phone": "+234 707 257 8187",
    "location": "Abuja, Nigeria (Remote)",
    "portfolio": "veetechstudio.com",
    "linkedin": "linkedin.com/in/muhammed-nafiu",
    "infrastructure": "24/7 dedicated solar inverter power backup, redundant fiber internet, Windows 11 workstation",
}

# Pitch Templates
PITCH_TEMPLATES = {
    "track_a_tech": (
        "Hello {company} Team,\n\n"
        "I am applying for your {title} role.\n\n"
        "With a Computer Science background (OND) and hands-on experience in Windows systems troubleshooting, "
        "command-line diagnostics, and AI-assisted workflow automation, I specialize in diagnosing technical blockers, "
        "inspecting webhook/API payloads, and keeping operations running smoothly.\n\n"
        "What I bring to your team:\n"
        "1. Technical troubleshooting & OS diagnostics: Strong command of Windows internals, Command Prompt (cmd), browser devtools, and step-by-step bug reproduction.\n"
        "2. AI-assisted workflow & CRM operations: Experienced in building and operating local SQLite databases, automated pipelines, and quality assurance gates using agentic AI tools.\n"
        "3. 24/7 remote reliability: Operating from a private home office in Abuja, Nigeria, equipped with a dedicated solar inverter backup power system and redundant fiber internet.\n\n"
        "My resume and details are attached. I look forward to speaking with your team.\n\n"
        "Best regards,\n"
        "Muhammed Nafiu\n"
        "nafiu@getveetech.com | +234 707 257 8187\n"
        "Portfolio: veetechstudio.com"
    ),
    "track_b_basic": (
        "Hi {company} Hiring Team,\n\n"
        "I am applying for your {title} position.\n\n"
        "I specialize in remote customer support, spreadsheet management, and administrative operations. "
        "My priority is fast response times, meticulous data entry, and clear, empathetic customer communication.\n\n"
        "What I bring to your team:\n"
        "1. High accuracy & organization: Experienced in CRM updating, database hygiene, ticket resolution, and spreadsheet workflows.\n"
        "2. Fast response time: Skilled in live chat, email ticketing, and managing high-volume customer inquiries.\n"
        "3. 100% remote reliability: I operate from a private home office equipped with a dedicated 24/7 solar inverter backup system "
        "and redundant fiber internet, ensuring zero downtime or missed shifts.\n\n"
        "I am available to start immediately and can easily align with your team's operating hours. My resume is attached.\n\n"
        "Warm regards,\n"
        "Muhammed Nafiu\n"
        "nafiu@getveetech.com | +234 707 257 8187\n"
        "Abuja, Nigeria (Remote)"
    ),
    "track_c_writing": (
        "Subject: Article Pitch: 3 Content Angles for {company} : Muhammed Nafiu\n\n"
        "Hi {company} Editorial Team,\n\n"
        "I saw your call for freelance writers and wanted to pitch directly.\n\n"
        "I specialize in writing clear, well-researched, and actionable content covering technology, AI automation workflows, "
        "system troubleshooting, and B2B operations. I produce clean drafts that require minimal editorial revision, formatted "
        "with proper headings, screenshots, and metadata.\n\n"
        "3 quick topic angles I can write for you this week:\n"
        "1. Why Most AI Automation Workflows Fail in Production (And the Simple Guardrails That Fix Them)\n"
        "2. How Growing Teams Eliminate Manual Data Entry Bottlenecks Without Expensive SaaS Bloat\n"
        "3. A Practical Step-by-Step Guide to Troubleshooting Common Webhook and CRM Sync Failures\n\n"
        "My typical turnaround is 24 to 48 hours per 1,000 words. You can view my portfolio at veetechstudio.com.\n\n"
        "Would you like me to tackle a trial draft for you this week?\n\n"
        "Best regards,\n"
        "Muhammed Nafiu\n"
        "nafiu@getveetech.com | +234 707 257 8187"
    ),
}

# Platform Directories and Guides (Clean, 100% Free Direct Boards)
PLATFORMS = {
    "Wellfound (Track A: 10/day - Tech Support, IT, QA & AI Ops)": {
        "platform_key": "Wellfound",
        "track": "track_a_tech",
        "url": "https://wellfound.com/jobs",
        "filters": [
            "1. Filter Roles: 'Technical Support', 'QA Engineer', 'IT Support', 'Solutions Engineer', 'Operations'",
            "2. Location: Remote only -> Worldwide",
            "3. Excluded keywords: 'Senior Software', 'Staff Engineer', 'Principal', 'LeetCode'",
            "4. 100% Free: Click Apply, paste tailored pitch, and submit directly to founders/HR",
        ],
        "cv_recommended": "Muhammed_Nafiu_Technical_Support_Operations_CV.pdf",
        "cv_path": TECH_CV_PATH,
        "pitch_key": "track_a_tech",
        "target_daily": 10,
    },
    "Himalayas (Track A: 5/day - Tech Support, IT Helpdesk, QA)": {
        "platform_key": "Himalayas",
        "track": "track_a_tech",
        "url": "https://himalayas.app/jobs/technical-support",
        "filters": [
            "1. Categories: 'Technical Support', 'IT Support', 'Help Desk', 'QA'",
            "2. Experience Level: Check 'Entry-level' and 'Mid-level' (Uncheck Senior/Staff)",
            "3. Location: Worldwide / Work from anywhere",
            "4. 100% Free: Direct ATS links (Ashby, Greenhouse, Lever, SmartRecruiters)",
        ],
        "cv_recommended": "Muhammed_Nafiu_Technical_Support_Operations_CV.pdf",
        "cv_path": TECH_CV_PATH,
        "pitch_key": "track_a_tech",
        "target_daily": 5,
    },
    "Himalayas (Track B: 4/day - Customer Support & Operations)": {
        "platform_key": "Himalayas",
        "track": "track_b_basic",
        "url": "https://himalayas.app/jobs/customer-support",
        "filters": [
            "1. Categories: 'Customer Support', 'Customer Service', 'Virtual Assistant', 'Operations'",
            "2. Location: Worldwide / Work from anywhere",
            "3. Non-coding roles (chat, email ticketing, client onboarding, data verification)",
            "4. 100% Free: Direct company ATS application forms",
        ],
        "cv_recommended": "Muhammed_Nafiu_Resume.pdf (Operations & VA Resume)",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_b_basic",
        "target_daily": 4,
    },
    "BloggingPro (Track C: 2/day - Paid Writing Gigs)": {
        "platform_key": "BloggingPro",
        "track": "track_c_gigs",
        "url": "https://www.bloggingpro.com/job-category/freelance-writing-jobs/",
        "filters": [
            "1. Category: Freelance Writing Jobs / Remote Writing",
            "2. Send 3-headline article pitch with 24-48h turnaround offer",
            "3. 100% Free direct pitch emails to editorial leads",
        ],
        "cv_recommended": "3-Headline Pitch Email + Portfolio Link",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_c_writing",
        "target_daily": 2,
    },
    "ProBlogger (Track C: 1/day - Tech & B2B Writing)": {
        "platform_key": "ProBlogger",
        "track": "track_c_gigs",
        "url": "https://problogger.com/jobs/pages/advanced-search",
        "filters": [
            "1. Keywords: Tech, AI, SaaS, Software, Operations",
            "2. Check 'Work can be done remotely'",
            "3. 100% Free direct email / application link",
        ],
        "cv_recommended": "3-Headline Pitch Email + Portfolio Link",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_c_writing",
        "target_daily": 1,
    },
    "MotionArt / ModSquad (Track C: 1/day - YouTube Scripts & Ticket Moderation)": {
        "platform_key": "MotionArt / ModSquad",
        "track": "track_c_gigs",
        "url": "https://join.modsquad.com/",
        "filters": [
            "1. MotionArt: YouTube Scriptwriting ($40/script, fast turnarounds)",
            "2. ModSquad: Remote Independent Contractor (Mod)",
            "3. Influx (influx.com/careers): Worldwide Support Agent",
        ],
        "cv_recommended": "Muhammed_Nafiu_Resume.pdf (Operations & VA Resume)",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_b_basic",
        "target_daily": 1,
    },
}

STATUS_CHOICES = [
    "Applied",
    "Interview Booked",
    "Take-Home / Assessment",
    "Offer Accepted",
    "Rejected",
    "No Response",
]

TRACK_CHOICES = [
    "track_a_tech",
    "track_b_basic",
    "track_c_gigs",
]

TRACK_LABELS = {
    "track_a_tech": "Track A: Tech Support, IT, QA & AI Ops (15/day)",
    "track_b_basic": "Track B: Basic Customer Support & Ops (4/day)",
    "track_c_gigs": "Track C: Fast Writing & Crowdsource Gigs (4/day)",
}
