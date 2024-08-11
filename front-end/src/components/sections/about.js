import React from "react";
import "./sections.scss";
import Arrow_right from "../../assets/icons/arrow-right-white.svg";
import { Link } from "react-router-dom";

function AboutSection() {
  return (
    <section id="about">
      <div className="header">This is our pet project</div>
      <div className="divider"></div>
      <div className="sub-header">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </div>
      <Link className="navbar-action" to="/chat">
        <div>Call to action</div>
        <img src={Arrow_right} />
      </Link>
    </section>
  );
}

export default AboutSection;
