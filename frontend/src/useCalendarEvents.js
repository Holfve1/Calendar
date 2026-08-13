import { useEffect, useState } from "react";
import {
  createEvent,
  deleteEvent,
  deleteEventSeries,
  fetchEvents,
  updateEvent,
  updateEventSeries,
} from "./api";

export function useCalendarEvents() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const loadEvents = () => {
    setIsLoading(true);
    fetchEvents()
      .then(setEvents)
      .catch((err) => setError(err.message))
      .finally(() => setIsLoading(false));
  };

  useEffect(loadEvents, []);

  const handleCreate = async (event) => {
    await createEvent(event);
    setIsModalOpen(false);
    loadEvents();
  };

  const handleUpdate = async (id, event) => {
    await updateEvent(id, event);
    setSelectedEvent(null);
    loadEvents();
  };

  const handleUpdateSeries = async (groupId, event) => {
    await updateEventSeries(groupId, event);
    setSelectedEvent(null);
    loadEvents();
  };

  const handleDelete = async (id) => {
    await deleteEvent(id);
    setSelectedEvent(null);
    loadEvents();
  };

  const handleDeleteSeries = async (groupId) => {
    await deleteEventSeries(groupId);
    setSelectedEvent(null);
    loadEvents();
  };

  return {
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
  };
}
