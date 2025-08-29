from datetime import datetime
import pytz


def convert_to_timezone(dt: datetime, tz_str: str) -> str:
    """Convert UTC datetime to target timezone string."""
    utc = pytz.utc.localize(dt)
    target = pytz.timezone(tz_str)
    return utc.astimezone(target).strftime("%Y-%m-%d %H:%M:%S %Z")
