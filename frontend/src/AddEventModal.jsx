import { useState } from "react";

const RECURRENCE_OPTIONS = [
  { value: "none", label: "Does not repeat" },
  { value: "daily", label: "Daily" },
  { value: "every_other_day", label: "Every other day" },
  { value: "weekly", label: "Weekly" },
  { value: "biweekly", label: "Bi weekly (every 2 weeks)" },
  { value: "monthly", label: "Monthly" },
  { value: "annually", label: "Annually" },
];

function AddEventModal({ onClose, onCreate, initialDate = "" }) {
  const [date, setDate] = useState(initialDate);
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [recurrence, setRecurrence] = useState("none");
  const [recurrenceEndType, setRecurrenceEndType] = useState("count");
  const [recurrenceCount, setRecurrenceCount] = useState(5);
  const [recurrenceEndDate, setRecurrenceEndDate] = useState("");
  const [error, setError] = useState(null);
  const [isSaving, setIsSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);

    const event = {
      date,
      start_time: startTime,
      end_time: endTime,
      title,
      content,
      recurrence,
    };

    if (recurrence !== "none") {
      event.recurrence_end_type = recurrenceEndType;
      if (recurrenceEndType === "count") {
        event.recurrence_count = Number(recurrenceCount);
      } else {
        event.recurrence_end_date = recurrenceEndDate;
      }
    }

    try {
      await onCreate(event);
    } catch (err) {
      setError(err.message);
      setIsSaving(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-box" onClick={(e) => e.stopPropagation()}>
        <h2>Add Event</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Date
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
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
            <input
              type="time"
              value={endTime}
              onChange={(e) => setEndTime(e.target.value)}
            />
          </label>
          <label>
            Title
            <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
          </label>
          <label>
            Content
            <textarea value={content} onChange={(e) => setContent(e.target.value)} />
          </label>

          <label>
            Repeats
            <select value={recurrence} onChange={(e) => setRecurrence(e.target.value)}>
              {RECURRENCE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          {recurrence !== "none" && (
            <>
              <label>
                Ends
                <select
                  value={recurrenceEndType}
                  onChange={(e) => setRecurrenceEndType(e.target.value)}
                >
                  <option value="count">After a number of times</option>
                  <option value="date">On a date</option>
                </select>
              </label>

              {recurrenceEndType === "count" ? (
                <label>
                  Number of times
                  <input
                    type="number"
                    min="2"
                    value={recurrenceCount}
                    onChange={(e) => setRecurrenceCount(e.target.value)}
                    required
                  />
                </label>
              ) : (
                <label>
                  End date
                  <input
                    type="date"
                    value={recurrenceEndDate}
                    onChange={(e) => setRecurrenceEndDate(e.target.value)}
                    required
                  />
                </label>
              )}
            </>
          )}

          {error && <p className="error">Could not save event: {error}</p>}

          <div className="modal-actions">
            <button type="button" onClick={onClose}>
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

export default AddEventModal;
