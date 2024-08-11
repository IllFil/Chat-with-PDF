import React from "react";
import "./sections.scss";
import ImagePlaceholder from "./../../assets/placeholder-image.jpg";

function HeroSection() {
  return (
    <section id="hero-section">
      <div className="hero-image">
        <img src={ImagePlaceholder} />
      </div>
      <div className="hero-text">
        <div className="header">Chat with your PDF file</div>
        <div className="sub-header">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </div>
    </section>
  );
}

export default HeroSection;
