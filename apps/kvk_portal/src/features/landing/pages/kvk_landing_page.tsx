import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  Microscope,
  FileCheck,
  Activity,
  Send,
  Clock,
  BookOpen,
  Layers,
  ChevronRight,
  Menu,
  X,
  Stethoscope,
  Radio,
  FileSpreadsheet,
  AlertTriangle,
} from 'lucide-react';
import bhoomiLogo from '../../../assets/bhoomi_logo.png';
import kvkHeroBg from '../../../assets/kvk_hero_bg.jpg';
import { authStore } from '../../../core/auth/auth_store';

export const KvkLandingPage: React.FC = () => {
  const agronomist = authStore.getCurrentAgronomist();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 selection:bg-[#2E7D32] selection:text-white font-sans antialiased overflow-x-hidden">
      {/* ========================================================================= */}
      {/* 1. TOP INSTITUTIONAL NAVIGATION BAR (LIGHT DASHBOARD THEME) */}
      {/* ========================================================================= */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-200/80 bg-white/95 backdrop-blur-md shadow-xs">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Brand Logo & Portal Identification */}
          <div className="flex items-center gap-3.5">
            <Link to="/" className="flex items-center gap-3 group">
              <img
                src={bhoomiLogo}
                alt="BHOOMI Logo"
                className="h-10 w-10 rounded-xl object-contain bg-white p-0.5 border border-slate-100 shadow-xs transition-transform duration-300 group-hover:scale-105"
                onError={(e) => {
                  (e.target as HTMLImageElement).src = '/bhoomi_logo.png';
                }}
              />
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-base font-extrabold tracking-tight text-slate-900 font-heading">
                    BHOOMI
                  </span>
                  <span className="hidden sm:inline-flex items-center rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-[#2E7D32]">
                    KVK AGRONOMIST PORTAL
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 font-medium">
                  {agronomist.kvkCenter}
                </p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-8 text-xs font-semibold text-slate-600">
            <a
              href="#capabilities"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              Capabilities
            </a>
            <a
              href="#workflow"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              Clinical Workflow
            </a>
            <a
              href="#safety"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              Confidence Gate & Safety
            </a>
            <a
              href="#icar-standards"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              ICAR Ground Truth
            </a>
          </nav>

          {/* Right Action: Enter Console CTA */}
          <div className="hidden sm:flex items-center gap-4">
            <Link
              to="/queue"
              className="group inline-flex items-center gap-2 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] px-4 py-2 text-xs font-bold text-white shadow-xs transition-all duration-200 hover:shadow-sm"
            >
              <span>Agronomist Console</span>
              <ArrowRight className="h-3.5 w-3.5 transition-transform duration-200 group-hover:translate-x-0.5" />
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-500 hover:text-slate-900 focus:outline-none"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown */}
        {mobileMenuOpen && (
          <div className="md:hidden border-b border-slate-200 bg-white px-6 py-4 space-y-3 shadow-md">
            <a
              href="#capabilities"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              Capabilities
            </a>
            <a
              href="#workflow"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              Clinical Workflow
            </a>
            <a
              href="#safety"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              Confidence Gate & Safety
            </a>
            <a
              href="#icar-standards"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              ICAR Ground Truth
            </a>
            <div className="pt-2">
              <Link
                to="/queue"
                onClick={() => setMobileMenuOpen(false)}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] py-2.5 text-xs font-bold text-white shadow-xs"
              >
                <span>Enter Agronomist Console</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </div>
        )}
      </header>

      {/* ========================================================================= */}
      {/* 2. HERO SECTION (LIGHT AGRICULTURAL THEME) */}
      {/* ========================================================================= */}
      <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden bg-slate-50 border-b border-slate-200/80">
        {/* Background Image with Light Tone Layer */}
        <div className="absolute inset-0 z-0">
          <img
            src={kvkHeroBg}
            alt="Agricultural Expert and Farmer in Paddy Field"
            className="h-full w-full object-cover object-center opacity-15"
          />
          {/* Subtle Light Gradients */}
          <div className="absolute inset-0 bg-gradient-to-r from-slate-50 via-slate-50/95 to-slate-50/80" />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-50/40 to-slate-50" />
        </div>

        {/* Hero Content */}
        <div className="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 lg:py-24 w-full">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Left Column: Heading & Value Proposition */}
            <div className="lg:col-span-7 space-y-6">
              {/* Institutional Badge */}
              <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3.5 py-1.5 shadow-xs">
                <span className="flex h-2 w-2 rounded-full bg-[#2E7D32]" />
                <span className="text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
                  ICAR-KVK Expert Agronomic Intelligence
                </span>
              </div>

              {/* Main Headline */}
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-slate-900 leading-[1.18]">
                Empowering Agricultural Experts with{' '}
                <span className="text-[#2E7D32]">
                  Multimodal AI & Clinical Triage
                </span>
              </h1>

              {/* Sub-headline */}
              <p className="text-sm sm:text-base text-slate-600 leading-relaxed max-w-2xl font-normal">
                BHOOMI bridges smallholder farmers and Krishi Vigyan Kendra agronomists.
                When crop anomaly confidence falls below the strict 0.70 safety threshold,
                cases are routed directly to your expert clinical queue for verified ICAR-grounded diagnosis and signed remediation.
              </p>

              {/* CTA Group */}
              <div className="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5">
                <Link
                  to="/queue"
                  className="inline-flex items-center justify-center gap-2.5 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] px-6 py-3.5 text-sm font-bold text-white shadow-xs transition-all duration-200 hover:shadow-sm"
                >
                  <span>Review Escalated Cases</span>
                  <ArrowRight className="h-4 w-4" />
                </Link>

                <a
                  href="#capabilities"
                  className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 px-5 py-3.5 text-sm font-bold text-slate-700 shadow-xs transition-all duration-200"
                >
                  <Microscope className="h-4 w-4 text-[#2E7D32]" />
                  <span>Explore Capabilities</span>
                </a>
              </div>

              {/* Metric Highlights Strip */}
              <div className="pt-6 border-t border-slate-200/80 grid grid-cols-2 sm:grid-cols-3 gap-4 text-left">
                <div className="space-y-0.5">
                  <div className="text-xl font-black text-slate-900">0.70 Floor</div>
                  <div className="text-[11px] text-slate-500">Confidence Gate Guarantee</div>
                </div>
                <div className="space-y-0.5">
                  <div className="text-xl font-black text-[#2E7D32]">8 Curated PoPs</div>
                  <div className="text-[11px] text-slate-500">ICAR & TNAU Ground Truth</div>
                </div>
                <div className="space-y-0.5 col-span-2 sm:col-span-1">
                  <div className="text-xl font-black text-slate-800">48h Verification</div>
                  <div className="text-[11px] text-slate-500">Longitudinal Efficacy Loop</div>
                </div>
              </div>
            </div>

            {/* Right Column: Interactive Agronomist Case Card (Light Dashboard Style) */}
            <div className="lg:col-span-5">
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 relative">
                {/* Accent Top Border */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-[#2E7D32] rounded-t-2xl" />

                {/* Card Header */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-red-50 text-red-600">
                      <AlertTriangle className="h-4 w-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-slate-900">Escalation ID: ESC-ERD-104</span>
                      <p className="text-[10px] text-slate-500">Farmer Murugan &bull; Erode, Tamil Nadu</p>
                    </div>
                  </div>
                  <span className="rounded-full bg-amber-50 border border-amber-200 px-2.5 py-0.5 text-[10px] font-bold text-amber-800">
                    Gate Triaged (0.58)
                  </span>
                </div>

                {/* Case Diagnostic Summary */}
                <div className="space-y-2.5 text-xs">
                  <div className="flex justify-between items-center rounded-xl bg-slate-50/80 p-3 border border-slate-200/60">
                    <span className="text-slate-500">Crop & Stage:</span>
                    <span className="font-bold text-slate-800">Samba Paddy &bull; Tillering</span>
                  </div>

                  <div className="flex justify-between items-center rounded-xl bg-slate-50/80 p-3 border border-slate-200/60">
                    <span className="text-slate-500">Observed Anomaly:</span>
                    <span className="font-bold text-amber-700">Irregular leaf margin discoloration</span>
                  </div>

                  <div className="flex justify-between items-center rounded-xl bg-slate-50/80 p-3 border border-slate-200/60">
                    <span className="text-slate-500">ICAR Ground Truth Match:</span>
                    <span className="font-bold text-[#2E7D32]">Paddy PoP §4.2 (Bacterial Blight)</span>
                  </div>

                  <div className="rounded-xl bg-emerald-50/60 border border-emerald-200/70 p-3 space-y-1.5">
                    <div className="flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32] uppercase tracking-wider">
                      <Stethoscope className="h-3.5 w-3.5" />
                      <span>Recommended Clinical Action</span>
                    </div>
                    <p className="text-[11px] text-slate-600 leading-relaxed">
                      Agronomist prescription ready for sign-off: Spray <i>Pseudomonas fluorescens</i> (2.5 kg/ha) + adjust field drainage.
                    </p>
                  </div>
                </div>

                {/* Card Action */}
                <div className="pt-2">
                  <Link
                    to="/queue"
                    className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-100 hover:bg-slate-200 border border-slate-200 py-2.5 text-xs font-bold text-slate-800 transition-colors"
                  >
                    <span>Open Case in Agronomist Workspace</span>
                    <ChevronRight className="h-4 w-4 text-[#2E7D32]" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 3. WHAT KVK EXPERTS CAN DO (LIGHT THEME GRID) */}
      {/* ========================================================================= */}
      <section id="capabilities" className="py-20 bg-white relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {/* Section Header */}
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
              <Microscope className="h-3.5 w-3.5" />
              <span>Platform Capabilities</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              Clinical Tools Built for Agricultural Scientists
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              Every feature in the BHOOMI KVK Portal is engineered around scientific rigor,
              deterministic validation, and actionable extension advisory.
            </p>
          </div>

          {/* Capabilities Grid */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Capability 1 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <AlertTriangle className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Multimodal Escalation Triage
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Review high-resolution symptom imagery and recorded farmer voice notes.
                Automated confidence gate routing ensures cases with ambiguity (&lt;0.70) are prioritized for immediate clinical intervention.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>0.70 Threshold Gate</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 2 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <BookOpen className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                ICAR & TNAU Ground Truth
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Direct access to 8 curated Package of Practices (PoP) documents.
                Our RAG pipeline performs strict retrieval over certified agricultural bulletins with zero model hallucination.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Zero Speculative Advice</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 3 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <Activity className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Deterministic Health Scoring
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Evaluate farms using transparent composite scores (0-100).
                Indices decompose into Vegetative Canopy, Soil Moisture, Pest Vulnerability, and Weather Threat subindices.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Explainable Subindices</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 4 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <FileCheck className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Official Prescription Authoring
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Formulate certified agronomic prescriptions with precise dosage, cultural interventions, and bio-control inputs.
                Prescriptions carry agronomist identity and official KVK credentials.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Signed Clinical Advice</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 5 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <Send className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Bilingual Voice & Text Delivery
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Dispatched prescriptions are automatically converted into localized audio synthesized in Tamil/English and delivered straight to the farmer’s mobile application.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Voice-First Farmer Access</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 6 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <Clock className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Treatment Efficacy & 48h Feedback
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Close the loop with automated 48-hour farmer check-ins.
                Monitor recovery trajectories and track aggregate treatment success rates across agrarian clusters.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Clinical Outcomes Closed</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 4. CLINICAL WORKFLOW / HOW IT WORKS (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section id="workflow" className="py-20 bg-slate-50 relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
              <Layers className="h-3.5 w-3.5" />
              <span>4-Step Clinical Protocol</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              How BHOOMI Triage Works in the Field
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              A transparent, closed-loop diagnostic protocol designed to prevent agricultural misdiagnosis and ensure timely expert intervention.
            </p>
          </div>

          {/* Steps Timeline */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Step 1 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#2E7D32]/10 text-[#2E7D32] font-black text-xs border border-[#2E7D32]/20">
                  01
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  Farmer Action
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Farmer Field Query</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Farmer uploads crop symptom photograph and speaks their query in regional dialect through the mobile application.
              </p>
            </div>

            {/* Step 2 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-700 font-black text-xs border border-amber-200">
                  02
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  Automated Gate
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Confidence Gating</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                The multimodal pipeline evaluates diagnosis certainty. If below the 0.70 floor, direct advice is gated and routed to KVK.
              </p>
            </div>

            {/* Step 3 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-blue-700 font-black text-xs border border-blue-200">
                  03
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  KVK Specialist
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Agronomist Review</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                KVK agronomist analyzes leaf images, farm land verification, weather telemetry, and verified ICAR reference bulletins.
              </p>
            </div>

            {/* Step 4 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-50 text-purple-700 font-black text-xs border border-purple-200">
                  04
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  Closed-Loop
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Prescription & Follow-up</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Official prescription is delivered to the farmer with audio playback; 48-hour check-in records treatment response.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 5. CONFIDENCE GATE & SAFETY MATRIX (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section id="safety" className="py-20 bg-white relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div className="lg:col-span-6 space-y-6">
              <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3.5 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
                <ShieldCheck className="h-4 w-4" />
                <span>Deterministic Safety Architecture</span>
              </div>

              <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
                Zero Speculative Advice. Full Agronomic Accountability.
              </h2>

              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                In agricultural advisory, a fabricated chemical recommendation or incorrect pest diagnosis can devastate an entire harvest.
                BHOOMI enforces strict programmatic gates in backend code—not loose LLM prompts.
              </p>

              <div className="space-y-3 pt-2">
                <div className="flex items-start gap-3 rounded-2xl bg-slate-50 p-4 border border-slate-200/80">
                  <CheckCircle2 className="h-5 w-5 text-[#2E7D32] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Hard-Coded Confidence Floor (0.70)</h4>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Any image diagnosis scoring &lt;0.70 triggers an escalation event. No speculative chemical advice is ever returned to the farmer.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-2xl bg-slate-50 p-4 border border-slate-200/80">
                  <CheckCircle2 className="h-5 w-5 text-[#2E7D32] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Zero-Retrieval Honest Refusal</h4>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      If retrieval relevance is below the threshold, the system returns an honest no-retrieval notification and escalates immediately to KVK.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-2xl bg-slate-50 p-4 border border-slate-200/80">
                  <CheckCircle2 className="h-5 w-5 text-[#2E7D32] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Deterministic Health Score Engine</h4>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Health scores are computed using pure mathematical subindices. Same inputs guarantee identical outputs every single time.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Comparison Matrix Table Card */}
            <div className="lg:col-span-6">
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
                <div className="border-b border-slate-100 pb-3">
                  <h3 className="text-sm font-bold text-slate-900">Safety Comparison Framework</h3>
                  <p className="text-[11px] text-slate-500">Generic AI chatbots vs. BHOOMI KVK Intelligence</p>
                </div>

                <div className="space-y-2 text-xs">
                  {/* Row 1 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Low Confidence Handling</div>
                    <div className="col-span-4 text-red-700 bg-red-50/80 px-2 py-0.5 rounded text-[10px] border border-red-100">Guesses / Hallucinates</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>Escalates to KVK</span>
                    </div>
                  </div>

                  {/* Row 2 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Chemical Advice</div>
                    <div className="col-span-4 text-red-700 bg-red-50/80 px-2 py-0.5 rounded text-[10px] border border-red-100">Unchecked Dosage</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>ICAR PoP Grounded</span>
                    </div>
                  </div>

                  {/* Row 3 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Prescription Signing</div>
                    <div className="col-span-4 text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[10px]">Anonymous / None</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>KVK Agronomist ID</span>
                    </div>
                  </div>

                  {/* Row 4 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Post-Treatment Follow-up</div>
                    <div className="col-span-4 text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[10px]">No Tracking</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>48h Clinical Loop</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2">
                  <div className="rounded-xl bg-[#2E7D32]/5 border border-[#2E7D32]/20 p-2.5 text-center">
                    <p className="text-[11px] text-[#2E7D32] font-semibold">
                      Enforced by BHOOMI Core Architecture (SIH25076)
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 6. ICAR GROUND TRUTH STANDARDS (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section id="icar-standards" className="py-20 bg-slate-50 relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
              <FileSpreadsheet className="h-3.5 w-3.5" />
              <span>Certified Knowledge Base</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              Curated ICAR & TNAU Package of Practices
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              Our retrieval engine operates over structured, peer-reviewed agronomic documentation covering key crops, stages, and diagnostic thresholds.
            </p>
          </div>

          {/* Corpus Cards */}
          <div className="mt-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Crop Bulletin</span>
              <h4 className="text-sm font-bold text-slate-900">Samba & Kuruvai Paddy</h4>
              <p className="text-[11px] text-slate-500">
                Pest identification, brown plant hopper management, blast treatment, and nutrient deficiency protocols.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Crop Bulletin</span>
              <h4 className="text-sm font-bold text-slate-900">Sugarcane & Ratoon Crops</h4>
              <p className="text-[11px] text-slate-500">
                Early shoot borer, red rot control, bio-fertilizer schedules, and drought resilience practices.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Crop Bulletin</span>
              <h4 className="text-sm font-bold text-slate-900">Cotton & Oilseeds</h4>
              <p className="text-[11px] text-slate-500">
                Bollworm management, sucking pest control, leaf reddening remedies, and certified IPM strategies.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Crop Bulletin</span>
              <h4 className="text-sm font-bold text-slate-900">Horticultural Crops</h4>
              <p className="text-[11px] text-slate-500">
                Banana sigatoka leaf spot, wilt control, micronutrient spray schedules, and organic soil amendments.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 7. FINAL CALL TO ACTION (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section className="py-20 bg-white relative border-b border-slate-200 overflow-hidden">
        <div className="relative z-10 mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-4 py-1.5 shadow-xs">
            <Radio className="h-4 w-4 text-[#2E7D32]" />
            <span className="text-xs font-bold uppercase tracking-widest text-[#2E7D32]">
              Active KVK Center: {agronomist.kvkCenter}
            </span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-slate-900 tracking-tight">
            Ready to Review Today’s Agronomic Escalation Queue?
          </h2>

          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Logged in as <strong className="text-slate-900 font-bold">{agronomist.name}</strong> ({agronomist.specialization}).
            Access the agronomist console to diagnose pending cases, sign clinical prescriptions, and support regional farmers.
          </p>

          <div className="pt-3 flex flex-col sm:flex-row items-center justify-center gap-3.5">
            <Link
              to="/queue"
              className="inline-flex w-full sm:w-auto items-center justify-center gap-2.5 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] px-8 py-3.5 text-sm font-bold text-white shadow-xs transition-all duration-200 hover:shadow-sm"
            >
              <span>Launch Agronomist Console</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              to="/settings"
              className="inline-flex w-full sm:w-auto items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 px-7 py-3.5 text-sm font-bold text-slate-700 shadow-xs transition-colors"
            >
              <span>View KVK Profile & Settings</span>
            </Link>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 8. INSTITUTIONAL FOOTER (LIGHT THEME) */}
      {/* ========================================================================= */}
      <footer className="border-t border-slate-200 bg-white py-12 text-slate-500 text-xs">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-8 border-b border-slate-100">
            {/* Branding Column */}
            <div className="space-y-3 md:col-span-2">
              <div className="flex items-center gap-2.5">
                <img
                  src={bhoomiLogo}
                  alt="BHOOMI Logo"
                  className="h-8 w-8 rounded-lg object-contain bg-white p-0.5 border border-slate-100 shadow-xs"
                  onError={(e) => {
                    (e.target as HTMLImageElement).src = '/bhoomi_logo.png';
                  }}
                />
                <span className="text-base font-extrabold text-slate-900 tracking-tight">BHOOMI</span>
                <span className="text-[10px] font-bold text-[#2E7D32] bg-[#2E7D32]/10 px-2 py-0.5 rounded-full uppercase tracking-wider">
                  KVK Portal
                </span>
              </div>
              <p className="text-xs text-slate-500 max-w-md leading-relaxed">
                BHOOMI AI Agricultural Intelligence & Clinical Escalation Platform.
                Developed for Krishi Vigyan Kendras, Agricultural Officers, and Indian smallholder farmers.
              </p>
            </div>

            {/* Quick Links Column */}
            <div className="space-y-2.5">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-800">
                Agronomist Workspace
              </span>
              <ul className="space-y-2 text-xs">
                <li>
                  <Link to="/queue" className="hover:text-[#2E7D32] transition-colors">
                    Escalation Queue
                  </Link>
                </li>
                <li>
                  <Link to="/review" className="hover:text-[#2E7D32] transition-colors">
                    Cases Under Review
                  </Link>
                </li>
                <li>
                  <Link to="/history" className="hover:text-[#2E7D32] transition-colors">
                    Resolved History
                  </Link>
                </li>
                <li>
                  <Link to="/efficacy" className="hover:text-[#2E7D32] transition-colors">
                    Treatment Efficacy Analytics
                  </Link>
                </li>
              </ul>
            </div>

            {/* Institution Column */}
            <div className="space-y-2.5">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-800">
                Institutional Extension
              </span>
              <ul className="space-y-2 text-xs">
                <li>
                  <Link to="/settings" className="hover:text-[#2E7D32] transition-colors">
                    KVK Center Credentials
                  </Link>
                </li>
                <li>
                  <a href="#icar-standards" className="hover:text-[#2E7D32] transition-colors">
                    ICAR / TNAU PoP Standards
                  </a>
                </li>
                <li>
                  <a href="#safety" className="hover:text-[#2E7D32] transition-colors">
                    Confidence Gate Policy (0.70)
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
            <p>
              &copy; {new Date().getFullYear()} BHOOMI Agricultural Advisory System. All rights reserved.
            </p>
            <p className="font-mono text-[10px] text-slate-500">
              KVK Node: ICAR-KVK Erode &bull; Intelligence Layer SIH25076
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};
