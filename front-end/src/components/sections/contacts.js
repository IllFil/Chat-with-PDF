import React from "react";
import "./sections.scss";

import ImagePlaceholder from "./../../assets/placeholder-image.jpg";

function ContactsSection() {
  return (
    <section id="contacts">
      <div className="card">
        <div className="card-header">
          <div className="round-image">
            <img src={ImagePlaceholder} />
          </div>
          <div className="header">Illia Filipas</div>
        </div>
        <div className="sub-header">
          <ul>
            <li>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </li>
            <li>
              Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat.
            </li>
          </ul>
        </div>
      </div>
      <div className="card">
        <div className="card-header">
          <div className="round-image">
            <img src={ImagePlaceholder} />
          </div>
          <div className="header">Anastasiia Ivanchenko</div>
        </div>
        <div className="sub-header">
          <ul>
            <li>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua.
            </li>
            <li>
              Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat.
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}

export default ContactsSection;
