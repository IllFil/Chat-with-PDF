import React from "react";

import Navbar from "./components/navbar/navbar";
import Footer from "./components/footer/footer";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Home from "./pages/home/home";
import Chat from "./pages/chat/QueryForm";

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Navbar />
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>

        <Footer />
      </div>
    </Router>
  );
}

export default App;
