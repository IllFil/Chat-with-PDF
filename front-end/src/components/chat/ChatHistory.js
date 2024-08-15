import React from "react";

import AiQuery from "../../assets/icons/logo-query.svg";
import UserQuery from "../../assets/icons/user.svg"

function ChatHistory({ chatHistory }) {
  return (
    <div className="chat-history">
        {chatHistory.map((entry, index) => (
          <div className="chat-dialogue" key={index}>
            <div className="query">
              <div className="message">{entry.query}</div>
              <img src={UserQuery}/> 
            </div>
            <div className="response">
              <img src={AiQuery}/>
              <div className="message">{entry.response}</div>
            </div>
          </div>
        ))}
    </div>
  );
}

export default ChatHistory;
