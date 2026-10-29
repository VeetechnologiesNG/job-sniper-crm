"""
Job Sniper CRM Configuration
Defines default daily quotas across Track A (Tech Support/IT/QA/AI Ops), Track B (Basic Operations & Customer Support),
and Track C (Fast Writing & Crowdsource Gigs).
Anchor: Wellfound = 6 (Track A), Himalayas = 3 (Track A) + 3 (Track B) = 6.
Remotive is permanently removed and replaced with We Work Remotely (4/day) and Jobspresso (3/day).
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

# Daily Target Settings (23 Total: 9 Track A + 10 Track B + 4 Track C)
# Anchor: Wellfound = 6 (Track A), Himalayas = 3 (Track A) + 3 (Track B) = 6. Combined = 12.
# Other Track B: We Work Remotely (4) + Jobspresso (3) = 7.
DEFAULT_DAILY_QUOTA = {
    "track_a_total": 9,
    "track_b_total": 10,
    "track_c_total": 4,
    "total": 23,
    "wellfound_track_a": 6,
    "himalayas_track_a": 3,
    "himalayas_track_b": 3,
    "other_track_b": 7,
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

# Platform Directories and Guides (Remotive removed; WWR and Jobspresso expanded)
PLATFORMS = {
    "Wellfound (Track A: 6/day - Tech Support, IT, QA & AI Ops)": {
        "platform_key": "Wellfound",
        "track": "track_a_tech",
        "url": "https://wellfound.com/jobs",
        "filters": [
            "1. Click Role filter -> Keep 'Technical Support', 'QA Engineer', 'IT Support', 'Solutions Engineer'",
            "2. Location: Remote only -> Worldwide",
            "3. Excluded keywords: 'Senior Software', 'Staff Engineer', 'Principal', 'LeetCode'",
            "4. Skip any listing asking for 3+ years of manual production Python/Node.js coding",
        ],
        "cv_recommended": "Muhammed_Nafiu_Technical_Support_Operations_CV.pdf",
        "cv_path": TECH_CV_PATH,
        "pitch_key": "track_a_tech",
        "target_daily": 6,
    },
    "Himalayas (Track A: 3/day - Tech Support, IT Helpdesk, QA)": {
        "platform_key": "Himalayas",
        "track": "track_a_tech",
        "url": "https://himalayas.app/jobs/technical-support",
        "filters": [
            "1. Categories: 'Technical Support', 'IT Support', 'Help Desk', 'QA'",
            "2. Experience Level: Check 'Entry-level' and 'Mid-level' (Uncheck Senior/Staff)",
            "3. Location: Worldwide / Work from anywhere",
            "4. Apply directly on the company's free ATS form (Ashby, Greenhouse, Lever)",
        ],
        "cv_recommended": "Muhammed_Nafiu_Technical_Support_Operations_CV.pdf",
        "cv_path": TECH_CV_PATH,
        "pitch_key": "track_a_tech",
        "target_daily": 3,
    },
    "Himalayas (Track B: 3/day - Basic Support, Admin & VA)": {
        "platform_key": "Himalayas",
        "track": "track_b_basic",
        "url": "https://himalayas.app/jobs/customer-support",
        "filters": [
            "1. Categories: 'Customer Support', 'Customer Service', 'Virtual Assistant', 'Operations'",
            "2. Location: Worldwide / Work from anywhere",
            "3. Non-coding roles (chat, email, scheduling, data entry, client onboarding)",
        ],
        "cv_recommended": "Muhammed_Nafiu_Resume.pdf (Operations & VA Resume)",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_b_basic",
        "target_daily": 3,
    },
    "We Work Remotely (Track B: 4/day - Customer Support & Ops)": {
        "platform_key": "We Work Remotely",
        "track": "track_b_basic",
        "url": "https://weworkremotely.com/categories/remote-customer-support-jobs",
        "filters": [
            "1. Look strictly for the blue 'Anywhere in the World' badge on each listing",
            "2. Categories: Customer Support, Operations, Back-Office",
            "3. 100% free direct ATS link, zero paywalls or blurred company names",
        ],
        "cv_recommended": "Muhammed_Nafiu_Resume.pdf (Operations & VA Resume)",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_b_basic",
        "target_daily": 4,
    },
    "Jobspresso (Track B: 3/day - Worldwide Support & Ops)": {
        "platform_key": "Jobspresso",
        "track": "track_b_basic",
        "url": "https://jobspresso.co/remote-support-jobs/",
        "filters": [
            "1. Browse 'Support' and 'Operations' categories",
            "2. Filter Location: Select 'Worldwide' listings",
            "3. Click 'Apply' to go directly to company's hiring page",
        ],
        "cv_recommended": "Muhammed_Nafiu_Resume.pdf (Operations & VA Resume)",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_b_basic",
        "target_daily": 3,
    },
    "BloggingPro (Track C: 2/day - Paid Writing Gigs)": {
        "platform_key": "BloggingPro",
        "track": "track_c_gigs",
        "url": "https://www.bloggingpro.com/job-category/freelance-writing-jobs/",
        "filters": [
            "1. Category: Freelance Writing Jobs / Remote Writing",
            "2. Send 3-headline article pitch with 24-48h turnaround offer",
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
        ],
        "cv_recommended": "3-Headline Pitch Email + Portfolio Link",
        "cv_path": OPS_CV_PATH,
        "pitch_key": "track_c_writing",
        "target_daily": 1,
    },
    "ModSquad / Influx (Track C: 1/day - Crowdsource Chat & Ticket Support)": {
        "platform_key": "ModSquad / Influx",
        "track": "track_c_gigs",
        "url": "https://join.modsquad.com/",
        "filters": [
            "1. ModSquad: Apply as Remote Independent Contractor (Mod)",
            "2. Influx (influx.com/careers): Apply for Worldwide Support Agent",
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
    "track_a_tech": "Track A: Tech Support, IT, QA & AI Ops (9/day)",
    "track_b_basic": "Track B: Basic Customer Support & Ops (10/day)",
    "track_c_gigs": "Track C: Fast Writing & Crowdsource Gigs (4/day)",
}
