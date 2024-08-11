import React from "react";
import Logo from "../../assets/logo.png";
import Arrow_right from "../../assets/icons/arrow-right-white.svg";
import "./navbar.scss";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="Navbar">
      <div className="logo-image">
        <img src={Logo} />
      </div>
      <div className="navbar-menu">
        <a href="#hero-section">Home</a>
        <a href="#contacts">Contacts</a>
        <a href="#about">About</a>
      </div>
      <Link className="navbar-action" to="/chat">
        <div>Call to action</div>
        <img src={Arrow_right} />
      </Link>
    </nav>
  );
}

export default Navbar;
