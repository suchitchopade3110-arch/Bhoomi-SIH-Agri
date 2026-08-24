import React, { useState } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import HowItWorksSection from './components/HowItWorksSection';
import FarmHealthSection from './components/FarmHealthSection';
import FarmIntelligenceSection from './components/FarmIntelligenceSection';
import ExplainableAiSection from './components/ExplainableAiSection';
import DiseaseDetectionSection from './components/DiseaseDetectionSection';
import FarmTimelineSection from './components/FarmTimelineSection';
import DashboardPreviewSection from './components/DashboardPreviewSection';
import Footer from './components/Footer';
import OfficerPortalModal from './components/OfficerPortalModal';
import AgronomistPortalModal from './components/AgronomistPortalModal';
import VoiceQueryModal from './components/VoiceQueryModal';

import { INITIAL_FARM_DATA } from './data/farmStore';
import { PRESET_SCENARIOS } from './data/healthScoreEngine';

export default function App() {
  const [farmData, setFarmData] = useState(INITIAL_FARM_DATA);
  const [activeScenario, setActiveScenario] = useState(PRESET_SCENARIOS.baseline);
  const [activeLanguage, setActiveLanguage] = useState('ta'); // 'ta' | 'en' | 'hi' | 'te'

  // Modals state
  const [isVoiceModalOpen, setIsVoiceModalOpen] = useState(false);
  const [isOfficerPortalOpen, setIsOfficerPortalOpen] = useState(false);
  const [isAgronomistPortalOpen, setIsAgronomistPortalOpen] = useState(false);

  const handleInspectScore = () => {
    const el = document.getElementById('farm-health');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-[#f8faf5] text-slate-900 flex flex-col selection:bg-emerald-200 selection:text-emerald-900">
      
      {/* 1. Top Navigation Bar */}
      <Navbar
        onOpenVoiceModal={() => setIsVoiceModalOpen(true)}
        onOpenOfficerPortal={() => setIsOfficerPortalOpen(true)}
        onOpenAgronomistPortal={() => setIsAgronomistPortalOpen(true)}
        activeLanguage={activeLanguage}
        onChangeLanguage={(lang) => setActiveLanguage(lang)}
      />

      <main className="flex-grow">
        {/* 2. Hero Section with Live Farm Health Card */}
        <HeroSection
          farm={farmData}
          activeScenario={activeScenario}
          onInspectScore={handleInspectScore}
          onOpenVoiceModal={() => setIsVoiceModalOpen(true)}
          onOpenOfficerPortal={() => setIsOfficerPortalOpen(true)}
        />

        {/* Powerful Features (visually updated FarmIntelligenceSection) */}
        <FarmIntelligenceSection />

        {/* 3. How Bhoomi Works */}
        <HowItWorksSection 
          onOpenVoiceModal={() => setIsVoiceModalOpen(true)} 
        />


        {/* 10. Final Call to Action */}
        <section className="py-24 bg-[#0f172a] text-white relative overflow-hidden text-center border-t border-slate-800">
          <div className="absolute inset-0 opacity-20 mix-blend-overlay" style={{ backgroundImage: "url('https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=2000&auto=format&fit=crop')", backgroundSize: 'cover', backgroundPosition: 'center' }}></div>
          
          <div className="container relative z-10 max-w-3xl mx-auto space-y-8">
            <h2 className="text-3xl sm:text-5xl font-bold text-white leading-tight">
              Govern with verified data.<br />
              Disburse subsidies securely.
            </h2>

            <div className="pt-4 flex justify-center">
              <button
                onClick={() => setIsOfficerPortalOpen(true)}
                className="bg-blue-600 text-white px-8 py-3.5 rounded-full font-bold inline-flex items-center gap-2 hover:bg-blue-700 transition-colors shadow-xl"
              >
                <span className="text-white">🛡️</span> Access Officer Dashboard
              </button>
            </div>
          </div>
        </section>

        {/* Preserved functionality sections (Hidden from primary visual flow to match Image 2) */}
        <div className="hidden">
          <FarmHealthSection
            activeScenario={activeScenario}
            onSelectScenario={(scen) => setActiveScenario(scen)}
          />
          <ExplainableAiSection />
          <DiseaseDetectionSection
            onOpenAgronomistPortal={() => setIsAgronomistPortalOpen(true)}
          />
          <FarmTimelineSection
            onSelectScenario={(scen) => setActiveScenario(scen)}
            onOpenVoiceModal={() => setIsVoiceModalOpen(true)}
          />
        </div>
      </main>

      {/* 11. Footer */}
      <Footer />

      {/* HITL & Interactive Modals */}
      <OfficerPortalModal
        isOpen={isOfficerPortalOpen}
        onClose={() => setIsOfficerPortalOpen(false)}
      />

      <AgronomistPortalModal
        isOpen={isAgronomistPortalOpen}
        onClose={() => setIsAgronomistPortalOpen(false)}
      />

      <VoiceQueryModal
        isOpen={isVoiceModalOpen}
        onClose={() => setIsVoiceModalOpen(false)}
        onSelectScenario={(scen) => setActiveScenario(scen)}
      />

    </div>
  );
}
