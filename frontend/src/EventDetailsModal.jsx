import { useState } from "react";
import { formatDate } from "./dateUtils";

function EventDetailsModal({ event, onClose, onUpdate, onUpdateSeries, onDelete, onDeleteSeries }) {
  const [isEditing, setIsEditing] = useState(false);
  const [date, setDate] = useState(event.date);
  const [startTime, setStartTime] = useState(event.start_time || "");
  const [endTime, setEndTime] = useState(event.end_time || "");
  const [title, setTitle] = useState(event.title);
  const [content, setContent] = useState(event.content || "");
  const [applyToSeries, setApplyToSeries] = useState(false);
  const [error, setError] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isConfirmingDelete, setIsConfirmingDelete] = useState(false);

  const handleSave = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);
    try {
      if (applyToSeries) {
        await onUpdateSeries(event.recurrence_group_id, {
          start_time: startTime,
          end_time: endTime,
          title,
          content,
        });
      } else {
        await onUpdate(event.id, {
          date,
          start_time: startTime,
          end_time: endTime,
          title,
          content,
          is_recurring: event.is_recurring,
        });
      }
    } catch (err) {
      setError(err.message);
      setIsSaving(false);
    }
  };

  const handleDelete = async (wholeSeries) => {
    setIsDeleting(true);
    setError(null);
    try {
      if (wholeSeries) {
        await onDeleteSeries(event.recurrence_group_id);
      } else {
        await onDelete(event.id);
      }
    } catch (err) {
      setError(err.message);
      setIsDeleting(false);
    }
  };

  if (isEditing) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-box" onClick={(e) => e.stopPropagation()}>
          <h2>Edit Event</h2>
          <form onSubmit={handleSave}>
            <label>
              Date
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                disabled={applyToSeries}
                required
              />
            </label>
            <label>
              Start time (leave blank for all day)
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
              />
            </label>
            <label>
              End time (leave blank for all day)
              <input type="time" value={endTime} onChange={(e) => setEndTime(e.target.value)} />
            </label>
            <label>
              Title
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </label>
            <label>
              Content
              <textarea value={content} onChange={(e) => setContent(e.target.value)} />
            </label>

            {event.is_recurring && (
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={applyToSeries}
                  onChange={(e) => setApplyToSeries(e.target.checked)}
                />
                Apply to entire series (each occurrence keeps its own date)
              </label>
            )}

            {error && <p className="error">Could not save event: {error}</p>}

            <div className="modal-actions">
              <button type="button" onClick={() => setIsEditing(false)}>
                Cancel
              </button>
              <button type="submit" disabled={isSaving}>
                {isSaving ? "Saving..." : "Save"}
              </button>
            </div>
          </form>
        </div>
      </div>
    );
  }

  if (isConfirmingDelete) {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-box" onClick={(e) => e.stopPropagation()}>
          <h2>Delete Event</h2>
          <p>
            Delete "{event.title}" on {formatDate(event.date)}? This can't be undone.
          </p>

          {error && <p className="error">{error}</p>}

          <div className="modal-actions">
            <button
              type="button"
              onClick={() => setIsConfirmingDelete(false)}
              disabled={isDeleting}
            >
              Cancel
            </button>
            {event.is_recurring ? (
              <>
                <button type="button" onClick={() => handleDelete(false)} disabled={isDeleting}>
                  {isDeleting ? "Deleting..." : "This event"}
                </button>
                <button type="button" onClick={() => handleDelete(true)} disabled={isDeleting}>
                  {isDeleting ? "Deleting..." : "Whole series"}
                </button>
              </>
            ) : (
              <button type="button" onClick={() => handleDelete(false)} disabled={isDeleting}>
                {isDeleting ? "Deleting..." : "Yes, delete"}
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <h2>{event.title}</h2>
        <dl className="event-details">
          <dt>Date</dt>
          <dd>{formatDate(event.date)}</dd>

          <dt>Time</dt>
          <dd>
            {event.start_time && event.end_time
              ? `${event.start_time} – ${event.end_time}`
              : "All day"}
          </dd>

          <dt>Content</dt>
          <dd>{event.content || "—"}</dd>

          {event.is_recurring && (
            <>
              <dt>Recurring</dt>
              <dd>Yes</dd>
            </>
          )}
        </dl>

        {error && <p className="error">{error}</p>}

        <div className="modal-actions">
          <button type="button" onClick={() => setIsConfirmingDelete(true)}>
            Delete
          </button>
          <button type="button" onClick={() => setIsEditing(true)}>
            Edit
          </button>
          <button type="button" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default EventDetailsModal;
