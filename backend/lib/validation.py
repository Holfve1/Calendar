from datetime import date, datetime

VALID_RECURRENCES = {
    "none",
    "daily",
    "every_other_day",
    "weekly",
    "biweekly",
    "monthly",
    "annually",
}


class ValidationError(Exception):
    pass


def require_field(data, field):
    value = data.get(field)
    if value in (None, ""):
        raise ValidationError(f"'{field}' is required")
    return value


def parse_iso_date(value, field):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValidationError(f"'{field}' must be a valid date (YYYY-MM-DD)")


def parse_optional_time(value, field):
    if not value:
        return None
    try:
        datetime.strptime(value, "%H:%M")
    except (TypeError, ValueError):
        raise ValidationError(f"'{field}' must be in HH:MM format")
    return value


def parse_recurrence(data):
    recurrence = data.get("recurrence") or "none"
    if recurrence not in VALID_RECURRENCES:
        raise ValidationError(f"'recurrence' must be one of {sorted(VALID_RECURRENCES)}")

    if recurrence == "none":
        return recurrence, None, None, None

    end_type = data.get("recurrence_end_type")
    if end_type not in ("count", "date"):
        raise ValidationError("'recurrence_end_type' must be 'count' or 'date' when repeating")

    if end_type == "count":
        count = data.get("recurrence_count")
        if not isinstance(count, (int, float)) or count != int(count) or count < 2:
            raise ValidationError("'recurrence_count' must be a whole number of 2 or more")
        return recurrence, end_type, int(count), None

    end_date = parse_iso_date(data.get("recurrence_end_date"), "recurrence_end_date")
    return recurrence, end_type, None, end_date


def parse_event_payload(data):
    event_date = parse_iso_date(require_field(data, "date"), "date")
    title = require_field(data, "title")
    start_time = parse_optional_time(data.get("start_time"), "start_time")
    end_time = parse_optional_time(data.get("end_time"), "end_time")
    content = data.get("content")
    return event_date, title, start_time, end_time, content
