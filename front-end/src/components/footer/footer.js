import React from "react";
import Logo from "../../assets/logo.png";
import "./footer.scss";

function Footer() {
  return (
    <footer className="Footer">
      <div className="logo-image">
        <img src={Logo} />
      </div>
      <div className="footer-menu">
        <a href="#hero-section">Home</a>
        <a href="#contacts">Contacts</a>
        <a href="#about">About</a>
      </div>
    </footer>
  );
}

export default Footer;
