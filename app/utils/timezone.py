from datetime import datetime
import pytz


def convert_to_timezone(dt: datetime, target_tz: str = "Asia/Kolkata") -> datetime:
    """
    Convert a UTC datetime to the target timezone and return datetime object.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:  # assume UTC if naive
        dt = dt.replace(tzinfo=pytz.UTC)

    tz = pytz.timezone(target_tz)
    return dt.astimezone(tz)  # still datetime object (not string!)