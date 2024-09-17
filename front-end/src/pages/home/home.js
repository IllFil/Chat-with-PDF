import React from "react";
import HeroSection from "../../components/sections/hero-section";
import HowItWorksSection from "../../components/sections/how-it-works";
import FunctionsSection from "../../components/sections/functions";
import ContactsSection from "../../components/sections/contacts";
import AboutSection from "../../components/sections/about";

import Navbar from "../../components/navbar/navbar";
import Footer from "../../components/footer/footer";

function Home() {
  return (
    <div id="home-page">
      <header className="App-header">
          <Navbar />
        </header>
      <HeroSection />
      <HowItWorksSection />
      <FunctionsSection />
      <ContactsSection />
      <AboutSection />

      <Footer />
    </div>
  );
}

export default Home;
