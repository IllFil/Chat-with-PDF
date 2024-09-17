import React from "react";

function StatusMessage({ status }) {
  return (
    <div>
      <h3>Status:</h3>
      <pre>{status}</pre>
    </div>
  );
}

export default StatusMessage;
