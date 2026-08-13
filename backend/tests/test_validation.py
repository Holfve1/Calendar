from datetime import date

import pytest

from lib.validation import ValidationError, parse_event_payload, parse_recurrence


def test_parse_event_payload_requires_date():
    with pytest.raises(ValidationError, match="'date' is required"):
        parse_event_payload({"title": "Standup"})


def test_parse_event_payload_requires_title():
    with pytest.raises(ValidationError, match="'title' is required"):
        parse_event_payload({"date": "2026-08-20"})


def test_parse_event_payload_rejects_invalid_date():
    with pytest.raises(ValidationError, match="'date' must be a valid date"):
        parse_event_payload({"date": "not-a-date", "title": "Standup"})


def test_parse_event_payload_rejects_invalid_time():
    with pytest.raises(ValidationError, match="'start_time' must be in HH:MM format"):
        parse_event_payload({"date": "2026-08-20", "title": "Standup", "start_time": "9am"})


def test_parse_event_payload_allows_blank_times():
    event_date, title, start_time, end_time, content = parse_event_payload(
        {"date": "2026-08-20", "title": "Standup", "start_time": "", "end_time": ""}
    )

    assert event_date == date(2026, 8, 20)
    assert title == "Standup"
    assert start_time is None
    assert end_time is None
    assert content is None


def test_parse_recurrence_defaults_to_none():
    assert parse_recurrence({}) == ("none", None, None, None)


def test_parse_recurrence_rejects_unknown_type():
    with pytest.raises(ValidationError, match="'recurrence' must be one of"):
        parse_recurrence({"recurrence": "hourly"})


def test_parse_recurrence_requires_end_type_when_repeating():
    with pytest.raises(ValidationError, match="'recurrence_end_type'"):
        parse_recurrence({"recurrence": "daily"})


def test_parse_recurrence_requires_valid_count():
    with pytest.raises(ValidationError, match="'recurrence_count'"):
        parse_recurrence({"recurrence": "daily", "recurrence_end_type": "count", "recurrence_count": 1})


def test_parse_recurrence_requires_valid_end_date():
    with pytest.raises(ValidationError, match="'recurrence_end_date'"):
        parse_recurrence({"recurrence": "daily", "recurrence_end_type": "date"})


def test_parse_recurrence_with_valid_count():
    assert parse_recurrence(
        {"recurrence": "daily", "recurrence_end_type": "count", "recurrence_count": 5}
    ) == ("daily", "count", 5, None)


def test_parse_recurrence_with_valid_end_date():
    assert parse_recurrence(
        {"recurrence": "weekly", "recurrence_end_type": "date", "recurrence_end_date": "2026-09-01"}
    ) == ("weekly", "date", None, date(2026, 9, 1))
