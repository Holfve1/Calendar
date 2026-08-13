from datetime import date

from lib.recurrence import generate_occurrence_dates


def test_none_returns_single_date():
    dates = generate_occurrence_dates(date(2026, 8, 20), "none", end_type=None)

    assert dates == [date(2026, 8, 20)]


def test_daily_with_count():
    dates = generate_occurrence_dates(date(2026, 8, 20), "daily", "count", count=3)

    assert dates == [date(2026, 8, 20), date(2026, 8, 21), date(2026, 8, 22)]


def test_every_other_day_with_count():
    dates = generate_occurrence_dates(date(2026, 8, 20), "every_other_day", "count", count=3)

    assert dates == [date(2026, 8, 20), date(2026, 8, 22), date(2026, 8, 24)]


def test_weekly_with_end_date():
    dates = generate_occurrence_dates(
        date(2026, 8, 1), "weekly", "date", end_date=date(2026, 8, 22)
    )

    assert dates == [date(2026, 8, 1), date(2026, 8, 8), date(2026, 8, 15), date(2026, 8, 22)]


def test_weekly_end_date_excludes_dates_after_it():
    dates = generate_occurrence_dates(
        date(2026, 8, 1), "weekly", "date", end_date=date(2026, 8, 20)
    )

    assert dates == [date(2026, 8, 1), date(2026, 8, 8), date(2026, 8, 15)]


def test_biweekly_with_count():
    dates = generate_occurrence_dates(date(2026, 8, 1), "biweekly", "count", count=3)

    assert dates == [date(2026, 8, 1), date(2026, 8, 15), date(2026, 8, 29)]


def test_annually_keeps_anchor_day_across_leap_years():
    dates = generate_occurrence_dates(date(2028, 2, 29), "annually", "count", count=3)

    assert dates == [date(2028, 2, 29), date(2029, 2, 28), date(2030, 2, 28)]


def test_monthly_keeps_anchor_day_across_short_months():
    dates = generate_occurrence_dates(date(2026, 1, 31), "monthly", "count", count=4)

    assert dates == [
        date(2026, 1, 31),
        date(2026, 2, 28),
        date(2026, 3, 31),
        date(2026, 4, 30),
    ]


def test_caps_at_max_occurrences():
    dates = generate_occurrence_dates(date(2026, 1, 1), "daily", "count", count=1000)

    assert len(dates) == 366
