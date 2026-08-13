const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

export async function fetchEvents() {
  const response = await fetch(`${API_URL}/calendar`);
  if (!response.ok) {
    throw new Error(`Failed to fetch events: ${response.status}`);
  }
  return response.json();
}

export async function createEvent(event) {
  const response = await fetch(`${API_URL}/calendar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  if (!response.ok) {
    throw new Error(`Failed to create event: ${response.status}`);
  }
}

export async function updateEvent(id, event) {
  const response = await fetch(`${API_URL}/calendar/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  if (!response.ok) {
    throw new Error(`Failed to update event: ${response.status}`);
  }
}

export async function deleteEvent(id) {
  const response = await fetch(`${API_URL}/calendar/${id}`, { method: "DELETE" });
  if (!response.ok) {
    throw new Error(`Failed to delete event: ${response.status}`);
  }
}

export async function updateEventSeries(groupId, event) {
  const response = await fetch(`${API_URL}/calendar/series/${groupId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  if (!response.ok) {
    throw new Error(`Failed to update series: ${response.status}`);
  }
}

export async function deleteEventSeries(groupId) {
  const response = await fetch(`${API_URL}/calendar/series/${groupId}`, { method: "DELETE" });
  if (!response.ok) {
    throw new Error(`Failed to delete series: ${response.status}`);
  }
}
