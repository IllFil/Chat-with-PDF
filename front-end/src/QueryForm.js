import React, { useState } from "react";
import axios from "axios";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false); // Added loading state

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Set loading to true when request starts
    setResponse(""); // Clear previous response

    try {
      const result = await axios.post("http://localhost:5000/query", { query });
      setResponse(result.data.response);
    } catch (error) {
      console.error("Error submitting query:", error);
      setResponse("Failed to get response");
    } finally {
      setLoading(false); // Set loading to false after request completes
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          rows="4"
          cols="50"
          placeholder="Enter your query"
        />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
      <div>
        <h3>Response:</h3>
        <pre>{response}</pre>
      </div>
    </div>
  );
}

export default QueryForm;
