import React from "react";
import FileInput from "./FileInput";

function UserInput({
  query,
  setQuery,
  handleFileChange,  // Correct prop name
  handleSubmit,
  handleClearHistory,
  loading,
}) {
  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows="4"
        cols="50"
        placeholder="Enter your query"
      />
      <br />
      <FileInput onFileChange={handleFileChange} />  {/* Passed correctly */}
      <br />
      <button type="submit" disabled={loading}>
        {loading ? "Submitting..." : "Submit"}
      </button>
      <button type="button" onClick={handleClearHistory}>
        Clear Chat History
      </button>
    </form>
  );
}

export default UserInput;
