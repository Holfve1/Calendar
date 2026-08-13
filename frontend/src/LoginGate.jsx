import { useState } from "react";
import { fetchEvents } from "./api";
import { setCredentials } from "./auth";

function LoginGate({ onSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [isChecking, setIsChecking] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsChecking(true);
    setError(null);
    setCredentials(username, password);

    try {
      await fetchEvents();
      onSuccess();
    } catch (err) {
      setError("Invalid username or password");
      setIsChecking(false);
    }
  };

  return (
    <div className="login-gate">
      <div className="modal-box">
        <h2>Calendar Login</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Username
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </label>

          {error && <p className="error">{error}</p>}

          <div className="modal-actions">
            <button type="submit" disabled={isChecking}>
              {isChecking ? "Checking..." : "Log in"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default LoginGate;
