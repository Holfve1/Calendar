const STORAGE_KEY = "calendar_auth";

export function hasCredentials() {
  return sessionStorage.getItem(STORAGE_KEY) !== null;
}

export function setCredentials(username, password) {
  sessionStorage.setItem(STORAGE_KEY, btoa(`${username}:${password}`));
}

export function clearCredentials() {
  sessionStorage.removeItem(STORAGE_KEY);
}

export function getAuthHeader() {
  const stored = sessionStorage.getItem(STORAGE_KEY);
  return stored ? { Authorization: `Basic ${stored}` } : {};
}
