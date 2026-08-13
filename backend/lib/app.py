import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from lib.recurrence import generate_occurrence_dates
from lib.repositories.calendar_repo import CalendarRepository
from lib.validation import (
    ValidationError,
    parse_event_payload,
    parse_optional_time,
    parse_recurrence,
    require_field,
)


def serialize_entry(entry):
    return {
        "id": entry.id,
        "date": str(entry.date),
        "start_time": str(entry.start_time) if entry.start_time is not None else None,
        "end_time": str(entry.end_time) if entry.end_time is not None else None,
        "content": entry.content,
        "title": entry.title,
        "is_recurring": entry.is_recurring,
        "recurrence_group_id": entry.recurrence_group_id,
    }


def create_app(connection):
    app = Flask(__name__)
    CORS(app)

    @app.route("/calendar", methods=["GET"])
    def get_calendar_entries():
        repository = CalendarRepository(connection)
        entries = repository.all()
        return jsonify([serialize_entry(entry) for entry in entries])

    @app.route("/calendar", methods=["POST"])
    def create_calendar_entry():
        repository = CalendarRepository(connection)
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        try:
            event_date, title, start_time, end_time, content = parse_event_payload(data)
            recurrence, end_type, count, end_date = parse_recurrence(data)
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400

        occurrence_dates = generate_occurrence_dates(
            event_date, recurrence, end_type, count=count, end_date=end_date
        )

        is_recurring = recurrence != "none"
        group_id = str(uuid.uuid4()) if is_recurring else None

        for occurrence_date in occurrence_dates:
            repository.create(
                occurrence_date.isoformat(),
                start_time,
                end_time,
                content,
                title,
                is_recurring=is_recurring,
                recurrence_group_id=group_id,
            )

        return "", 201

    @app.route("/calendar/<int:id>", methods=["PATCH"])
    def update_calendar_entry(id):
        repository = CalendarRepository(connection)
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        try:
            event_date, title, start_time, end_time, content = parse_event_payload(data)
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400

        is_recurring = bool(data.get("is_recurring", False))
        repository.update(
            id, event_date.isoformat(), start_time, end_time, content, title, is_recurring
        )
        return "", 200

    @app.route("/calendar/<int:id>", methods=["DELETE"])
    def delete_calendar_entry(id):
        repository = CalendarRepository(connection)
        repository.delete(id)
        return "", 204

    @app.route("/calendar/series/<uuid:group_id>", methods=["PATCH"])
    def update_calendar_series(group_id):
        repository = CalendarRepository(connection)
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        try:
            title = require_field(data, "title")
            start_time = parse_optional_time(data.get("start_time"), "start_time")
            end_time = parse_optional_time(data.get("end_time"), "end_time")
        except ValidationError as error:
            return jsonify({"error": str(error)}), 400

        repository.update_series(str(group_id), start_time, end_time, data.get("content"), title)
        return "", 200

    @app.route("/calendar/series/<uuid:group_id>", methods=["DELETE"])
    def delete_calendar_series(group_id):
        repository = CalendarRepository(connection)
        repository.delete_series(str(group_id))
        return "", 204

    return app
