import calendar
from datetime import date, timedelta

MAX_OCCURRENCES = 366

_STEP_DAYS = {
    "daily": 1,
    "every_other_day": 2,
    "weekly": 7,
    "biweekly": 14,
}


def generate_occurrence_dates(start_date, recurrence, end_type, count=None, end_date=None):
    if recurrence == "none":
        return [start_date]

    dates = [start_date]
    current = start_date

    while len(dates) < MAX_OCCURRENCES:
        if end_type == "count" and len(dates) >= count:
            break

        current = _next_date(current, recurrence, start_date.day)

        if end_type == "date" and current > end_date:
            break

        dates.append(current)

    return dates


def _next_date(current, recurrence, anchor_day):
    if recurrence == "monthly":
        month = current.month + 1
        year = current.year + (month - 1) // 12
        month = (month - 1) % 12 + 1
        day = min(anchor_day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    if recurrence == "annually":
        year = current.year + 1
        day = min(anchor_day, calendar.monthrange(year, current.month)[1])
        return date(year, current.month, day)

    return current + timedelta(days=_STEP_DAYS[recurrence])
