import AddEventModal from "../AddEventModal";
import EventCard from "../EventCard";
import EventDetailsModal from "../EventDetailsModal";
import PageHeader from "../PageHeader";
import { isPast, sortByDate } from "../dateUtils";
import { useCalendarEvents } from "../useCalendarEvents";

function CalendarPage() {
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
  const upcomingEvents = sortByDate(
    events.filter((event) => !isPast(event.date) && !event.is_recurring)
  );

  return (
    <>
      <PageHeader title="Calendar" onAddClick={() => setIsModalOpen(true)} />

      {isLoading && <p>Loading events...</p>}
      {error && <p className="error">Could not load events: {error}</p>}
      {!isLoading && !error && upcomingEvents.length === 0 && <p>No events yet.</p>}

      <ul className="event-list">
        {upcomingEvents.map((event) => (
          <EventCard key={event.id} event={event} onClick={setSelectedEvent} />
        ))}
      </ul>

      {isModalOpen && (
        <AddEventModal onClose={() => setIsModalOpen(false)} onCreate={handleCreate} />
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

export default CalendarPage;
