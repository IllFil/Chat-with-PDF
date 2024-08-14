import React, { useState, useEffect } from "react";
import axios from "axios";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  axios.defaults.withCredentials = true;
  useEffect(() => {
    // Fetch chat history when component mounts
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    try {
      const result = await axios.get("http://localhost:5000/chat_history");
      setChatHistory(result.data.history);
    } catch (error) {
      console.error("Error fetching chat history:", error);
      setStatus("Failed to fetch chat history.");
    }
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) return; // Prevent empty queries

    setLoading(true);
    setStatus("");

    const formData = new FormData();
    formData.append("query", query);
    if (file) {
      formData.append("file", file);
    }

    try {
      setStatus("Submitting...");
      const result = await axios.post("http://localhost:5000/query", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const newResponse = result.data.response;
      setResponse(newResponse);

      // Update chat history with the new query and response
      setChatHistory((prev) => [...prev, { query, response: newResponse }]);

      setStatus("Query processed successfully!");
    } catch (error) {
      console.error("Error submitting query:", error);
      setResponse("Failed to get response");
      setStatus("An error occurred while processing the request.");
    } finally {
      setLoading(false);
      setQuery(""); // Clear the query input after submission
    }
  };

  const handleClearHistory = async () => {
    try {
      await axios.post("http://localhost:5000/clear_history");
      setChatHistory([]);
      setStatus("Chat history cleared successfully!");
    } catch (error) {
      console.error("Error clearing chat history:", error);
      setStatus("Failed to clear chat history.");
    }
  };
  return (
    <div>
      <h1>Chat</h1>
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
        <button type="button" onClick={handleClearHistory}>
          Clear Chat History
        </button>
      </form>
      <div>
        <h3>Status:</h3>
        <pre>{status}</pre>
      </div>
      <div>
        <h3>Chat History:</h3>
        <ul>
          {chatHistory.map((entry, index) => (
            <li key={index}>
              <strong>User:</strong> {entry.query}
              <br />
              <strong>AI:</strong> {entry.response}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default QueryForm;
