export function formatDate(isoDate) {
  const [year, month, day] = isoDate.split("-");
  return `${day}/${month}/${year}`;
}

export function sortByDate(events) {
  return [...events].sort((a, b) => {
    if (a.date !== b.date) return a.date < b.date ? -1 : 1;
    const aTime = a.start_time || "";
    const bTime = b.start_time || "";
    return aTime < bTime ? -1 : aTime > bTime ? 1 : 0;
  });
}

function toIso(date) {
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${date.getFullYear()}-${month}-${day}`;
}

function todayIso() {
  return toIso(new Date());
}

export function isPast(isoDate) {
  return isoDate < todayIso();
}

export function isInMonth(isoDate, year, month) {
  const [eventYear, eventMonth] = isoDate.split("-").map(Number);
  return eventYear === year && eventMonth === month;
}

export const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

export const WEEKDAYS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

function getStartOfWeek(date = new Date()) {
  const jsDay = date.getDay();
  const diffToMonday = jsDay === 0 ? -6 : 1 - jsDay;
  const monday = new Date(date);
  monday.setHours(0, 0, 0, 0);
  monday.setDate(date.getDate() + diffToMonday);
  return monday;
}

export function getWeekDates(weekOffset = 0) {
  const reference = new Date();
  reference.setDate(reference.getDate() + weekOffset * 7);
  const start = getStartOfWeek(reference);
  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date(start);
    date.setDate(start.getDate() + index);
    return toIso(date);
  });
}

export function getWeekRangeLabel(weekDates) {
  return `${formatDate(weekDates[0])} - ${formatDate(weekDates[6])}`;
}
