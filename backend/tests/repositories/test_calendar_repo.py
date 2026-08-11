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
        }
    ]
    repo = CalendarRepository(connection)

    result = repo.all()

    connection.execute.assert_called_with("SELECT * FROM calendar ORDER BY id")
    assert result == [
        Calendar(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")
    ]


def test_create_inserts_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.create("2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    connection.execute.assert_called_with(
        "INSERT INTO calendar (date, start_time, end_time, content, title) VALUES (%s, %s, %s, %s, %s)",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday"],
    )
    assert result is None


def test_delete_removes_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.delete(1)

    connection.execute.assert_called_with("DELETE FROM calendar WHERE ID = %s", [1])
    assert result is None


def test_update_modifies_entry():
    connection = Mock()
    repo = CalendarRepository(connection)

    result = repo.update(1, "2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday")

    connection.execute.assert_called_with(
        "UPDATE calendar SET date = %s, start_time = %s, end_time = %s, content = %s, title = %s WHERE id = %s",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", 1],
    )
    assert result is None
