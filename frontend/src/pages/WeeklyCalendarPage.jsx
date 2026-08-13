import { useState } from "react";
import AddEventModal from "../AddEventModal";
import EventCard from "../EventCard";
import EventDetailsModal from "../EventDetailsModal";
import PageHeader from "../PageHeader";
import { WEEKDAYS, formatDate, getWeekDates, getWeekRangeLabel } from "../dateUtils";
import { useCalendarEvents } from "../useCalendarEvents";

function WeeklyCalendarPage() {
  const {
    events,
    error,
    isLoading,
    isModalOpen,
    setIsModalOpen,
    handleCreate,
    handleUpdate,
    handleUpdateSeries,
    handleDelete,
    handleDeleteSeries,
    selectedEvent,
    setSelectedEvent,
  } = useCalendarEvents();
  const [initialDate, setInitialDate] = useState("");
  const [weekOffset, setWeekOffset] = useState(0);

  const weekDates = getWeekDates(weekOffset);
  const weekEvents = events.filter((event) => weekDates.includes(event.date));
  const eventsByDay = weekDates.map((date) =>
    weekEvents.filter((event) => event.date === date)
  );

  const openAddModal = (date = "") => {
    setInitialDate(date);
    setIsModalOpen(true);
  };

  return (
    <>
      <PageHeader title="Weekly Calendar" onAddClick={() => openAddModal()}>
        <button type="button" onClick={() => setWeekOffset((offset) => offset - 1)}>
          ‹ Prev
        </button>
        <span className="week-range-label">{getWeekRangeLabel(weekDates)}</span>
        <button type="button" onClick={() => setWeekOffset((offset) => offset + 1)}>
          Next ›
        </button>
        {weekOffset !== 0 && (
          <button type="button" onClick={() => setWeekOffset(0)}>
            Today
          </button>
        )}
      </PageHeader>

      {isLoading && <p>Loading events...</p>}
      {error && <p className="error">Could not load events: {error}</p>}

      <div className="week-grid">
        {WEEKDAYS.map((day, index) => (
          <div
            key={day}
            className="week-day-row"
            onClick={() => openAddModal(weekDates[index])}
          >
            <div className="week-day-label">
              {day} <span className="week-day-date">{formatDate(weekDates[index])}</span>
            </div>
            <ul className="event-list">
              {eventsByDay[index].length === 0 && <li className="no-events">No events</li>}
              {eventsByDay[index].map((event) => (
                <EventCard
                  key={event.id}
                  event={event}
                  onClick={setSelectedEvent}
                  showDate={false}
                  showTime
                />
              ))}
            </ul>
          </div>
        ))}
      </div>

      {isModalOpen && (
        <AddEventModal
          onClose={() => setIsModalOpen(false)}
          onCreate={handleCreate}
          initialDate={initialDate}
        />
      )}

      {selectedEvent && (
        <EventDetailsModal
          event={selectedEvent}
          onClose={() => setSelectedEvent(null)}
          onUpdate={handleUpdate}
          onUpdateSeries={handleUpdateSeries}
          onDelete={handleDelete}
          onDeleteSeries={handleDeleteSeries}
        />
      )}
    </>
  );
}

export default WeeklyCalendarPage;
