import React, { useState } from "react";
import axios from "axios";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false); // Added loading state
  const [status, setStatus] = useState(""); // Added status state

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true); // Set loading to true when request starts
    setResponse(""); // Clear previous response
    setStatus(""); // Clear previous status

    const formData = new FormData();
    formData.append("query", query);
    if (file) {
      formData.append("file", file);
    }

    try {
      setStatus("Submitting..."); // Inform the user that the request is being processed
      const result = await axios.post("http://localhost:5000/query", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(result.data.response);
      setStatus("Query processed successfully!");
    } catch (error) {
      console.error("Error submitting query:", error);
      setResponse("Failed to get response");
      setStatus("An error occurred while processing the request.");
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
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <br />
        <button type="submit" disabled={loading}>
          {loading ? "Submitting..." : "Submit"}
        </button>
      </form>
      <div>
        <h3>Response:</h3>
        <pre>{response}</pre>
      </div>
      <div>
        <h3>Status:</h3>
        <pre>{status}</pre>
      </div>
    </div>
  );
}

export default QueryForm;
