import { NavLink } from "react-router-dom";

function NavBar() {
  return (
    <nav className="nav-bar">
      <NavLink to="/" end>
        Home
      </NavLink>
      <NavLink to="/monthly">Monthly</NavLink>
      <NavLink to="/weekly">Weekly</NavLink>
    </nav>
  );
}

export default NavBar;
