# Date and time management package
from datetime import datetime
# Package to manage timezones
import pytz

def request_time_of(timeStr, userTZ):
    return pytz.utc.localize(
        datetime.strptime(
            timeStr,
            "%Y-%m-%dT%H:%M:%SZ"
        )
    ).astimezone(userTZ[0]).strftime("%Y/%m/%d - %H:%M:%S")
