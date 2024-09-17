import React, { useState, useEffect } from "react";
import axios from "axios";

import ChatHeader from "../../components/chat/ChatHeader";
import ChatHistory from "../../components/chat/ChatHistory";
import StatusMessage from "../../components/chat/StatusMessage";
import FileInput from "../../components/chat/FileInput";
import UserInput from "../../components/chat/UserInput";

import LeftSidebar from "../../components/sidebars/LeftSidebar";
import "./styles.scss";

function QueryForm() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  // Important for session managing
  axios.defaults.withCredentials = true;

  useEffect(() => {
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

  const handleFileChange = (file) => {
    setFile(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) return;

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

      setChatHistory((prev) => [...prev, { query, response: newResponse }]);
      setStatus("Query processed successfully!");
    } catch (error) {
      console.error("Error submitting query:", error);
      setResponse("Failed to get response");
      setStatus("An error occurred while processing the request.");
    } finally {
      setLoading(false);
      setQuery(""); // Clear the query input after submission
      setFile(null); // Clear the file input after submission
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
    <div className="query-form">
      <LeftSidebar />
      <div className="section-wrapper">
        <ChatHeader chatHeader={'This is a chat header!'} />
        <ChatHistory chatHistory={chatHistory} />
        <UserInput 
          query={query}
          setQuery={setQuery}
          handleFileChange={handleFileChange}
          handleSubmit={handleSubmit}
          handleClearHistory={handleClearHistory}
          loading={loading}
        />

        {/* <form onSubmit={handleSubmit}>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows="4"
            cols="50"
            placeholder="Enter your query"
          />
          <br />
          <FileInput onFileChange={handleFileChange} />
          <br />
          <button type="submit" disabled={loading}>
            {loading ? "Submitting..." : "Submit"}
          </button>
          <button type="button" onClick={handleClearHistory}>
            Clear Chat History
          </button>
        </form> */}
      </div>
    </div>
  );
}

export default QueryForm;
