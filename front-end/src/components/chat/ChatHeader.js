import React from "react";

import ChatImg from "../../assets/icons/chat.svg";
import ChevronDown from "../../assets/icons/chevron-down.svg"

import "./styles.scss";

function ChatHeader({ chatHeader }) {
  return (
    <div className="chat-header">
        <img src={ChatImg}/>
        <div>{ chatHeader }</div>
        <img src={ChevronDown}/>
    </div>
  );
}

export default ChatHeader;