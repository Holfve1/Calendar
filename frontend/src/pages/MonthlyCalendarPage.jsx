import { useState } from "react";
import AddEventModal from "../AddEventModal";
import EventCard from "../EventCard";
import EventDetailsModal from "../EventDetailsModal";
import PageHeader from "../PageHeader";
import { MONTH_NAMES, isInMonth, sortByDate } from "../dateUtils";
import { useCalendarEvents } from "../useCalendarEvents";

const now = new Date();
const YEAR_OPTIONS = Array.from({ length: 8 }, (_, i) => now.getFullYear() - 2 + i);

function MonthlyCalendarPage() {
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
  const [selectedMonth, setSelectedMonth] = useState(now.getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(now.getFullYear());

  const monthEvents = sortByDate(
    events.filter((event) => isInMonth(event.date, selectedYear, selectedMonth))
  );

  return (
    <>
      <PageHeader title="Monthly Calendar" onAddClick={() => setIsModalOpen(true)}>
        <select
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(Number(e.target.value))}
        >
          {MONTH_NAMES.map((name, index) => (
            <option key={name} value={index + 1}>
              {name}
            </option>
          ))}
        </select>
        <select value={selectedYear} onChange={(e) => setSelectedYear(Number(e.target.value))}>
          {YEAR_OPTIONS.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </PageHeader>

      {isLoading && <p>Loading events...</p>}
      {error && <p className="error">Could not load events: {error}</p>}
      {!isLoading && !error && monthEvents.length === 0 && <p>No events this month.</p>}

      <ul className="event-list">
        {monthEvents.map((event) => (
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

export default MonthlyCalendarPage;
