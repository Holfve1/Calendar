import { Route, Routes } from "react-router-dom";
import NavBar from "./NavBar";
import CalendarPage from "./pages/CalendarPage";
import MonthlyCalendarPage from "./pages/MonthlyCalendarPage";
import WeeklyCalendarPage from "./pages/WeeklyCalendarPage";
import "./App.css";

function App() {
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
