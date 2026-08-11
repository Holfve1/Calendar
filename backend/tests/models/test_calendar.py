from lib.models.calendar import Calendar


def test_constructor_sets_attributes():
    calendar = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    assert calendar.id == 1
    assert calendar.date == "2026-08-20"
    assert calendar.start_time == "01:00"
    assert calendar.end_time == "23:59"
    assert calendar.content == "Going to go theatre"
    assert calendar.title == "Monica Birthday"


def test_equality():
    calendar_1 = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")
    calendar_2 = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    assert calendar_1 == calendar_2


def test_inequality():
    calendar_1 = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")
    calendar_2 = Calendar(2, "2026-08-21", "09:00", "10:00", "Standup", "Team Meeting")

    assert calendar_1 != calendar_2


def test_repr():
    calendar = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    assert str(calendar) == "Calendar(1, 2026-08-20, 01:00, 23:59, Going to go theatre, Monica Birthday)"
