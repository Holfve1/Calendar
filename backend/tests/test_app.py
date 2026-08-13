from unittest.mock import Mock

from lib.app import create_app


def test_get_calendar_entries():
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
    client = create_app(connection).test_client()

    response = client.get("/calendar")

    assert response.status_code == 200
    assert response.get_json() == [
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


def test_create_calendar_entry():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post(
        "/calendar",
        json={
            "date": "2026-08-20",
            "start_time": "01:00",
            "end_time": "23:59",
            "content": "Going to go theatre",
            "title": "Monica Birthday",
        },
    )

    assert response.status_code == 201
    connection.execute.assert_called_with(
        "INSERT INTO calendar (date, start_time, end_time, content, title, is_recurring, recurrence_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, None],
    )


def test_create_all_day_calendar_entry():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post(
        "/calendar",
        json={
            "date": "2026-08-20",
            "start_time": "",
            "end_time": "",
            "content": "Going to go theatre",
            "title": "Monica Birthday",
        },
    )

    assert response.status_code == 201
    connection.execute.assert_called_with(
        "INSERT INTO calendar (date, start_time, end_time, content, title, is_recurring, recurrence_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        ["2026-08-20", None, None, "Going to go theatre", "Monica Birthday", False, None],
    )


def test_get_calendar_entries_with_no_times():
    connection = Mock()
    connection.execute.return_value = [
        {
            "id": 1,
            "date": "2026-08-20",
            "start_time": None,
            "end_time": None,
            "content": "Going to go theatre",
            "title": "Monica Birthday",
            "is_recurring": False,
            "recurrence_group_id": None,
        }
    ]
    client = create_app(connection).test_client()

    response = client.get("/calendar")

    assert response.get_json() == [
        {
            "id": 1,
            "date": "2026-08-20",
            "start_time": None,
            "end_time": None,
            "content": "Going to go theatre",
            "title": "Monica Birthday",
            "is_recurring": False,
            "recurrence_group_id": None,
        }
    ]


def test_create_recurring_calendar_entry():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post(
        "/calendar",
        json={
            "date": "2026-08-20",
            "start_time": "01:00",
            "end_time": "23:59",
            "content": "Going to go theatre",
            "title": "Monica Birthday",
            "recurrence": "daily",
            "recurrence_end_type": "count",
            "recurrence_count": 3,
        },
    )

    assert response.status_code == 201
    assert connection.execute.call_count == 3
    inserted_dates = [call.args[1][0] for call in connection.execute.call_args_list]
    assert inserted_dates == ["2026-08-20", "2026-08-21", "2026-08-22"]
    inserted_is_recurring = [call.args[1][5] for call in connection.execute.call_args_list]
    assert inserted_is_recurring == [True, True, True]
    inserted_group_ids = [call.args[1][6] for call in connection.execute.call_args_list]
    assert len(set(inserted_group_ids)) == 1
    assert inserted_group_ids[0] is not None


def test_create_calendar_entry_missing_title_returns_400():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post("/calendar", json={"date": "2026-08-20"})

    assert response.status_code == 400
    assert "title" in response.get_json()["error"]
    connection.execute.assert_not_called()


def test_create_calendar_entry_invalid_date_returns_400():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post("/calendar", json={"date": "not-a-date", "title": "Standup"})

    assert response.status_code == 400
    assert "date" in response.get_json()["error"]
    connection.execute.assert_not_called()


def test_create_calendar_entry_invalid_recurrence_returns_400():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post(
        "/calendar",
        json={"date": "2026-08-20", "title": "Standup", "recurrence": "hourly"},
    )

    assert response.status_code == 400
    assert "recurrence" in response.get_json()["error"]
    connection.execute.assert_not_called()


def test_create_calendar_entry_non_json_body_returns_400():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.post("/calendar", data="not json")

    assert response.status_code == 400
    connection.execute.assert_not_called()


def test_update_calendar_entry():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.patch(
        "/calendar/1",
        json={
            "date": "2026-08-20",
            "start_time": "01:00",
            "end_time": "23:59",
            "content": "Going to go theatre",
            "title": "Monica Birthday",
        },
    )

    assert response.status_code == 200
    connection.execute.assert_called_with(
        "UPDATE calendar SET date = %s, start_time = %s, end_time = %s, content = %s, title = %s, is_recurring = %s WHERE id = %s",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", False, 1],
    )


def test_update_calendar_entry_preserves_is_recurring():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.patch(
        "/calendar/1",
        json={
            "date": "2026-08-20",
            "start_time": "01:00",
            "end_time": "23:59",
            "content": "Going to go theatre",
            "title": "Monica Birthday",
            "is_recurring": True,
        },
    )

    assert response.status_code == 200
    connection.execute.assert_called_with(
        "UPDATE calendar SET date = %s, start_time = %s, end_time = %s, content = %s, title = %s, is_recurring = %s WHERE id = %s",
        ["2026-08-20", "01:00", "23:59", "Going to go theatre", "Monica Birthday", True, 1],
    )


def test_delete_calendar_entry():
    connection = Mock()
    client = create_app(connection).test_client()

    response = client.delete("/calendar/1")

    assert response.status_code == 204
    connection.execute.assert_called_with("DELETE FROM calendar WHERE ID = %s", [1])


def test_update_calendar_series():
    connection = Mock()
    client = create_app(connection).test_client()
    group_id = "11111111-1111-1111-1111-111111111111"

    response = client.patch(
        f"/calendar/series/{group_id}",
        json={
            "start_time": "09:00",
            "end_time": "10:00",
            "content": "Standup",
            "title": "Daily Standup",
        },
    )

    assert response.status_code == 200
    connection.execute.assert_called_with(
        "UPDATE calendar SET start_time = %s, end_time = %s, content = %s, title = %s WHERE recurrence_group_id = %s",
        ["09:00", "10:00", "Standup", "Daily Standup", group_id],
    )


def test_update_calendar_series_missing_title_returns_400():
    connection = Mock()
    client = create_app(connection).test_client()
    group_id = "11111111-1111-1111-1111-111111111111"

    response = client.patch(f"/calendar/series/{group_id}", json={"start_time": "09:00"})

    assert response.status_code == 400
    connection.execute.assert_not_called()


def test_delete_calendar_series():
    connection = Mock()
    client = create_app(connection).test_client()
    group_id = "11111111-1111-1111-1111-111111111111"

    response = client.delete(f"/calendar/series/{group_id}")

    assert response.status_code == 204
    connection.execute.assert_called_with(
        "DELETE FROM calendar WHERE recurrence_group_id = %s", [group_id]
    )
