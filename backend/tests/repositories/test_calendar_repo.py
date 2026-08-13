from unittest.mock import Mock

from lib.models.calendar import Calendar
from lib.repositories.calendar_repo import CalendarRepository


def test_all_returns_calendar_entries():
    connection = Mock()
    connection.execute.return_value = [
        {
            "id": 1,
            "date": "2026-08-20",
            "start_time": "01:00",
            "end_time": "23:59",
            "content": "Going to go theatre",
            "title": "Monica Birthday",
            "is_recurring": False,
            "recurrence_group_id": None,
        }
    ]
    repo = CalendarRepository(connection)

    result = repo.all()

    connection.execute.assert_called_with("SELECT * FROM calendar ORDER BY id")
    assert result == [
        Calendar(
            1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None
        )
    ]


def test_create_inserts_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.create("2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    connection.execute.assert_called_with(
        "INSERT INTO calendar (date, start_time, end_time, content, title, is_recurring, recurrence_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None],
    )
    assert result is None


def test_create_inserts_recurring_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    repo.create(
        "2026-08-20",
        "01:00",
        "23:59",
        "Going to go theatre",
        "Monica Birthday",
        is_recurring=True,
        recurrence_group_id="group-1",
    )

    connection.execute.assert_called_with(
        "INSERT INTO calendar (date, start_time, end_time, content, title, is_recurring, recurrence_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", True, "group-1"],
    )


def test_delete_removes_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.delete(1)

    connection.execute.assert_called_with("DELETE FROM calendar WHERE ID = %s", [1])
    assert result is None


def test_delete_series_removes_all_matching_entries():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.delete_series("group-1")

    connection.execute.assert_called_with(
        "DELETE FROM calendar WHERE recurrence_group_id = %s", ["group-1"]
    )
    assert result is None


def test_update_modifies_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.update(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    connection.execute.assert_called_with(
        "UPDATE calendar SET date = %s, start_time = %s, end_time = %s, content = %s, title = %s, is_recurring = %s WHERE id = %s",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, 1],
    )
    assert result is None


def test_update_series_modifies_all_matching_entries():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.update_series("group-1", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    connection.execute.assert_called_with(
        "UPDATE calendar SET start_time = %s, end_time = %s, content = %s, title = %s WHERE recurrence_group_id = %s",
        ["01:00", "23:59", "Going to go theatre", "Monica Birthday", "group-1"],
    )
    assert result is None
