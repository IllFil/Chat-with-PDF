import React from "react";
import HeroSection from "../../components/sections/hero-section";
import HowItWorksSection from "../../components/sections/how-it-works";
import FunctionsSection from "../../components/sections/functions";
import ContactsSection from "../../components/sections/contacts";
import AboutSection from "../../components/sections/about";

function Home() {
  return (
    <div id="home-page">
      <HeroSection />
      <HowItWorksSection />
      <FunctionsSection />
      <ContactsSection />
      <AboutSection />
    </div>
  );
}

export default Home;
