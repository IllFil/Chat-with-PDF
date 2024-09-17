import React from "react";
import "./styles.scss";

function FileInput({ onFileChange }) {
  const handleChange = (event) => {
    onFileChange(event.target.files[0]);
  };

  return (
    <input type="file" accept=".pdf" onChange={handleChange} />
  );
}

export default FileInput;
