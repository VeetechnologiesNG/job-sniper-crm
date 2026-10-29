"""
Quota Service
Calculates daily progress, completion percentages, streaks, and platform-level targets.
"""
from datetime import date, timedelta
from database.queries import get_daily_progress, get_all_applications

def get_today_summary() -> dict:
    """Returns today's progress breakdown and percentage completion across 3 tracks."""
    today_str = date.today().strftime("%Y-%m-%d")
    progress = get_daily_progress(today_str)
    
    track_a_pct = min(100, int((progress["applied_track_a"] / max(1, progress["target_track_a"])) * 100))
    track_b_pct = min(100, int((progress["applied_track_b"] / max(1, progress["target_track_b"])) * 100))
    track_c_pct = min(100, int((progress["applied_track_c"] / max(1, progress["target_track_c"])) * 100))
    total_pct = min(100, int((progress["total_applied"] / max(1, progress["total_target"])) * 100))
    
    return {
        **progress,
        "track_a_pct": track_a_pct,
        "track_b_pct": track_b_pct,
        "track_c_pct": track_c_pct,
        "total_pct": total_pct,
        "track_a_remaining": max(0, progress["target_track_a"] - progress["applied_track_a"]),
        "track_b_remaining": max(0, progress["target_track_b"] - progress["applied_track_b"]),
        "track_c_remaining": max(0, progress["target_track_c"] - progress["applied_track_c"]),
        "total_remaining": max(0, progress["total_target"] - progress["total_applied"]),
    }

def get_streak_count() -> int:
    """Calculates consecutive days where total quota was met."""
    streak = 0
    today = date.today()
    for i in range(1, 31):
        day_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        progress = get_daily_progress(day_str)
        if progress["quota_met"]:
            streak += 1
        else:
            break
    return streak
