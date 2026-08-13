from lib.models.calendar import Calendar


def test_constructor_sets_attributes():
    calendar = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None)

    assert calendar.id == 1
    assert calendar.date == "2026-08-20"
    assert calendar.start_time == "01:00"
    assert calendar.end_time == "23:59"
    assert calendar.content == "Going to go theatre"
    assert calendar.title == "Monica Birthday"
    assert calendar.is_recurring is False
    assert calendar.recurrence_group_id is None


def test_equality():
    calendar_1 = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None)
    calendar_2 = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None)

    assert calendar_1 == calendar_2


def test_inequality():
    calendar_1 = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None)
    calendar_2 = Calendar(2, "2026-08-21", "09:00", "10:00", "Standup", "Team Meeting", True, "group-1")

    assert calendar_1 != calendar_2


def test_repr():
    calendar = Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None)

    assert str(calendar) == "Calendar(1, 2026-08-20, 01:00, 23:59, Going to go theatre, Monica Birthday, False, None)"
