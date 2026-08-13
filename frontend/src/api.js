import { clearCredentials, getAuthHeader } from "./auth";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      ...getAuthHeader(),
      ...options.headers,
    },
  });

  if (response.status === 401) {
    clearCredentials();
    window.location.reload();
  }

  return response;
}

export async function fetchEvents() {
  const response = await request("/calendar");
  if (!response.ok) {
    throw new Error(`Failed to fetch events: ${response.status}`);
  }
  return response.json();
}

export async function createEvent(event) {
  const response = await request("/calendar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  if (!response.ok) {
    throw new Error(`Failed to create event: ${response.status}`);
  }
}

export async function updateEvent(id, event) {
  const response = await request(`/calendar/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  if (!response.ok) {
    throw new Error(`Failed to update event: ${response.status}`);
  }
}

export async function deleteEvent(id) {
  const response = await request(`/calendar/${id}`, { method: "DELETE" });
  if (!response.ok) {
    throw new Error(`Failed to delete event: ${response.status}`);
  }
}

export async function updateEventSeries(groupId, event) {
  const response = await request(`/calendar/series/${groupId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event),
  });
  if (!response.ok) {
    throw new Error(`Failed to update series: ${response.status}`);
  }
}

export async function deleteEventSeries(groupId) {
  const response = await request(`/calendar/series/${groupId}`, { method: "DELETE" });
  if (!response.ok) {
    throw new Error(`Failed to delete series: ${response.status}`);
  }
}
