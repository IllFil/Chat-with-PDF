import React from "react";
import NewChat from "../../assets/icons/new-chat.svg";
import Journal from "../../assets/icons/journal.svg";
import User from "../../assets/icons/user.svg";

import "./styles.scss";

function LeftSidebar() {
  return (
    <div className="left-sidebar section-wrapper">
        <div className="actions-menu">
            <button><img src={NewChat}/></button>
            <button><img src={Journal}/></button>
            <div className="divider"></div>
        </div>
        <div className="account-menu">
            <div className="divider"></div>
            <button><img src={User}/></button>
        </div>
    </div>
  );
}

export default LeftSidebar;
