from dateutil.rrule import DAILY, MONTHLY, rrule, YEARLY
from datetime import datetime as dt


def period_of_time(start, end, group_type):
    return list(rrule(freq=group_type, dtstart=start, until=end))


start = dt.fromisoformat('2022-10-01T00:00:00')
end = dt.fromisoformat('2022-11-30T23:59:00')
group_type = DAILY

period = period_of_time(start=start, end=end, group_type=group_type)
