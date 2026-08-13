import { useState } from "react";
import { Route, Routes } from "react-router-dom";
import LoginGate from "./LoginGate";
import NavBar from "./NavBar";
import CalendarPage from "./pages/CalendarPage";
import MonthlyCalendarPage from "./pages/MonthlyCalendarPage";
import WeeklyCalendarPage from "./pages/WeeklyCalendarPage";
import { hasCredentials } from "./auth";
import "./App.css";

function App() {
  const [isAuthed, setIsAuthed] = useState(hasCredentials());

  if (!isAuthed) {
    return <LoginGate onSuccess={() => setIsAuthed(true)} />;
  }

  return (
    <>
      <NavBar />
      <main className="calendar-page">
        <Routes>
          <Route path="/" element={<CalendarPage />} />
          <Route path="/monthly" element={<MonthlyCalendarPage />} />
          <Route path="/weekly" element={<WeeklyCalendarPage />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
