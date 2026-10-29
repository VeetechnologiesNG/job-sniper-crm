"""
Export Service
Exports applications data to CSV format.
"""
import io
import pandas as pd
from database.queries import get_all_applications

def get_applications_df(track=None, platform=None, status=None) -> pd.DataFrame:
    """Returns a pandas DataFrame of filtered applications."""
    apps = get_all_applications(track=track, platform=platform, status=status)
    if not apps:
        return pd.DataFrame()
    return pd.DataFrame(apps)

def export_applications_to_csv() -> str:
    """Generates a CSV string of all applications in the database."""
    apps = get_all_applications()
    if not apps:
        return ""
    df = pd.DataFrame(apps)
    return df.to_csv(index=False)
