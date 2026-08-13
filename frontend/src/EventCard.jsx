import { formatDate } from "./dateUtils";

function EventCard({ event, onClick, showDate = true, showTime = false }) {
  return (
    <li
      className="event-card"
      onClick={(e) => {
        e.stopPropagation();
        onClick(event);
      }}
    >
      {showDate && <div className="event-date">{formatDate(event.date)}</div>}
      <div className="event-title">{event.title}</div>
      {showTime && event.start_time && (
        <div className="event-time">{event.start_time}</div>
      )}
    </li>
  );
}

export default EventCard;
