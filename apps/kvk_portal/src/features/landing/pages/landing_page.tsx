import React from 'react';
import { Link } from 'react-router-dom';
import {
  Sprout,
  BookOpen,
  Activity,
  ArrowRight,
  Sparkles,
  ChevronRight,
  Bot,
  Users,
  HeartHandshake,
  Stethoscope,
  Microscope,
  GraduationCap
} from 'lucide-react';
import bhoomiLogo from '../../../assets/bhoomi.png';
import kvkHeroBg from '../../../assets/kvk_hero_bg.jpg';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 selection:bg-emerald-500 selection:text-white">
      {/* 1. Public Landing Navigation Bar */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-200/80 bg-white/90 backdrop-blur-md">
        <div className="mx-auto flex h-18 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Branding */}
          <Link to="/landing" className="flex items-center gap-3 group">
            <img
              src={bhoomiLogo}
              alt="BHOOMI Logo"
              className="h-10 w-10 rounded-xl object-contain shadow-xs border border-slate-100 bg-emerald-50/50 p-0.5 transition-transform group-hover:scale-105"
              onError={(e) => {
                (e.target as HTMLImageElement).src = '/bhoomi.png';
              }}
            />
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-black tracking-tight text-slate-900">
                  BHOOMI
                </span>
                <span className="rounded bg-[#2E7D32]/10 px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider text-[#2E7D32]">
                  KVK PORTAL
                </span>
              </div>
              <p className="text-[11px] font-semibold text-slate-500">
                ICAR-KVK Agronomic Advisory &amp; Knowledge Network
              </p>
            </div>
          </Link>

          {/* Quick Nav Links */}
          <nav className="hidden md:flex items-center gap-8 text-xs font-bold text-slate-600">
            <a href="#overview" className="transition-colors hover:text-[#2E7D32]">
              Overview
            </a>
            <a href="#support" className="transition-colors hover:text-[#2E7D32]">
              Farmer Support
            </a>
            <a href="#workflow" className="transition-colors hover:text-[#2E7D32]">
              Advisory Flow
            </a>
            <a href="#impact" className="transition-colors hover:text-[#2E7D32]">
              Impact
            </a>
          </nav>

          {/* Primary CTA */}
          <div className="flex items-center gap-3">
            <Link
              to="/"
              className="flex items-center gap-2 rounded-xl bg-[#2E7D32] px-4 py-2.5 text-xs font-extrabold text-white shadow-xs transition-all hover:bg-[#1B5E20] hover:shadow-md active:scale-98"
            >
              <span>Access KVK Portal</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </div>
      </header>

      <main>
        {/* 2. Hero Section with Background Image */}
        <section id="overview" className="relative min-h-[620px] lg:min-h-[700px] flex items-center overflow-hidden">
          {/* Background Image Container */}
          <div className="absolute inset-0 z-0">
            <img
              src={kvkHeroBg}
              alt="KVK Agronomist consulting with an Indian farmer in field"
              className="h-full w-full object-cover object-center"
            />
            {/* Multi-layered Vignette & Dark Emerald Overlay */}
            <div className="absolute inset-0 bg-gradient-to-r from-slate-950/95 via-slate-900/85 to-slate-950/65" />
            <div className="absolute inset-0 bg-radial-at-t from-transparent via-slate-950/40 to-slate-950/90" />
          </div>

          <div className="relative z-10 mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
            <div className="max-w-3xl space-y-6">
              {/* Eyebrow Badge */}
              <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3.5 py-1.5 backdrop-blur-md">
                <Sparkles className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-xs font-extrabold tracking-wide uppercase text-emerald-300">
                  BHOOMI Knowledge &amp; Advisory Network
                </span>
              </div>

              {/* Main Headline */}
              <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white leading-[1.15]">
                Turning Agricultural Knowledge into <span className="text-emerald-400">Farmer Action.</span>
              </h1>

              {/* Supporting Description */}
              <p className="text-sm sm:text-base lg:text-lg text-slate-300 font-medium leading-relaxed max-w-2xl">
                Bridging Krishi Vigyan Kendra agronomists and plant pathology specialists directly with smallholder farmers to evaluate crop symptoms, deliver ICAR-grounded clinical prescriptions, and track longitudinal field recovery.
              </p>

              {/* CTAs */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link
                  to="/"
                  className="flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-3.5 text-sm font-extrabold text-slate-950 shadow-lg shadow-emerald-500/20 transition-all hover:bg-emerald-400 hover:shadow-emerald-500/30 active:scale-98"
                >
                  <span>Access KVK Portal</span>
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <a
                  href="#support"
                  className="flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-6 py-3.5 text-sm font-extrabold text-white backdrop-blur-md transition-all hover:bg-white/20 hover:border-white/30 active:scale-98"
                >
                  <span>Explore Capabilities</span>
                  <ChevronRight className="h-4 w-4 text-slate-300" />
                </a>
              </div>

              {/* Live Metric Strip */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 pt-8 border-t border-white/10">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                    <BookOpen className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-black text-white">ICAR &amp; TNAU</div>
                    <div className="text-[11px] text-slate-400 font-medium">Grounded Knowledge Base</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                    <Stethoscope className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-black text-white">Clinical-Grade</div>
                    <div className="text-[11px] text-slate-400 font-medium">Multi-Modal Diagnosis</div>
                  </div>
                </div>

                <div className="flex items-center gap-3 col-span-2 sm:col-span-1">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                    <Activity className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-black text-white">Longitudinal</div>
                    <div className="text-[11px] text-slate-400 font-medium">Treatment Efficacy Tracking</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 3. Expert Support for Farmers */}
        <section id="support" className="py-20 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <div className="inline-flex items-center gap-1.5 rounded-full bg-[#2E7D32]/10 px-3 py-1 text-xs font-bold text-[#2E7D32]">
                <Microscope className="h-3.5 w-3.5" />
                <span>EXPERT FARMER ASSISTANCE</span>
              </div>
              <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
                Empowering Extension Scientists
              </h2>
              <p className="mt-3 text-sm text-slate-600">
                Specialized clinical tools designed for Krishi Vigyan Kendra agronomists to diagnose complex pest and disease anomalies without guesswork.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Capability 1 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <Stethoscope className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Clinical Crop Advisory
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Review farmer-uploaded crop photos, audio transcriptions, and symptom checklists to prescribe targeted biochemical &amp; organic remedies.
                </p>
              </div>

              {/* Capability 2 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <BookOpen className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Curated PoP Repository
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Access 8-crop ICAR Package of Practices documentation, validated active ingredients, dosage rates, and chemical safety periods.
                </p>
              </div>

              {/* Capability 3 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <Activity className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Treatment Efficacy Tracking
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Monitor the 0–100 Treatment Response subindex over time to evaluate recovery post-spray and verify remedy effectiveness.
                </p>
              </div>

              {/* Capability 4 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <Bot className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Multi-Lingual Audio Delivery
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Prescriptions automatically synthesize into high-fidelity spoken Tamil audio summaries for easy comprehension by illiterate farmers.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 4. From Knowledge to Action (Workflow) */}
        <section id="workflow" className="py-20 bg-slate-100/70 border-y border-slate-200">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <div className="inline-flex items-center gap-1.5 rounded-full bg-[#2E7D32]/10 px-3 py-1 text-xs font-bold text-[#2E7D32]">
                <GraduationCap className="h-3.5 w-3.5" />
                <span>CLINICAL WORKFLOW</span>
              </div>
              <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
                From Agronomic Science to Field Recovery
              </h2>
              <p className="mt-3 text-sm text-slate-600">
                How BHOOMI guides agricultural expertise into tangible field improvements.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
              {/* Step 1 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">01</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <Sprout className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Field Issue Escalation</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    AI confidence gate automatically routes ambiguous or high-severity pest symptoms to the KVK queue.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32]">
                  <span>AI Confidence Gate</span>
                </div>
              </div>

              {/* Step 2 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">02</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <Microscope className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Agronomist Review</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    Expert evaluates crop variety, growth stage day, soil moisture, and previous treatments in the dossier.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32]">
                  <span>KVK Expert Portal</span>
                </div>
              </div>

              {/* Step 3 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">03</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <HeartHandshake className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Signed Prescription</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    Expert issues 3-point chemical &amp; biological dosage action plan with safety waiting periods.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32]">
                  <span>Grounded Advisory</span>
                </div>
              </div>

              {/* Step 4 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">04</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <Activity className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Recovery &amp; Follow-up</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    Farmer executes the remedy; follow-up scans compute health index recovery on the agronomist dashboard.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32]">
                  <span>Efficacy Tracking</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 5. Human-Centered Impact */}
        <section id="impact" className="py-20 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <div className="inline-flex items-center gap-1.5 rounded-full bg-[#2E7D32]/10 px-3 py-1 text-xs font-bold text-[#2E7D32]">
                <Users className="h-3.5 w-3.5" />
                <span>HUMAN-CENTERED IMPACT</span>
              </div>
              <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
                Transforming Farm Outcomes Across Districts
              </h2>
              <p className="mt-3 text-sm text-slate-600">
                Real benefits for agricultural scientists and the farmers they serve.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">0-Guesswork</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Safe Guidance</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Strict confidence gates prevent AI hallucinations from ever reaching farmer fields.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">&lt;24 hrs</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Rapid Response</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Direct escalation prioritization ensures timely intervention during critical disease outbreak windows.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">100% Native</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Voice Synthesis</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Tamil audio voice notes bridge the literacy barrier so all farmers understand exact dosages.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">Verifiable</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Efficacy Metric</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Empirical tracking of crop recovery confirms whether treatment successfully restored farm health.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 6. Final Call to Action Section */}
        <section className="py-16 bg-[#1B5E20] text-white">
          <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center space-y-6">
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
              Ready to Expand Your Agronomic Reach?
            </h2>
            <p className="text-sm sm:text-base text-emerald-100 max-w-2xl mx-auto">
              Access the BHOOMI KVK Portal to review escalated crop cases, consult the scientific knowledge base, and track treatment efficacy.
            </p>
            <div className="pt-2">
              <Link
                to="/"
                className="inline-flex items-center gap-2 rounded-xl bg-white px-8 py-3.5 text-sm font-extrabold text-[#1B5E20] shadow-lg transition-all hover:bg-emerald-50 hover:shadow-xl active:scale-98"
              >
                <span>Enter KVK Portal</span>
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* 7. Footer */}
      <footer className="border-t border-slate-200 bg-white py-8 text-xs text-slate-500">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Sprout className="h-4 w-4 text-[#2E7D32]" />
            <span className="font-bold text-slate-700">BHOOMI &bull; ICAR-KVK Advisory Network</span>
            <span>&bull;</span>
            <span>SIH25076</span>
          </div>
          <p className="text-center sm:text-right text-slate-400">
            &copy; {new Date().getFullYear()} ICAR-KVK Erode (MYRADA) &bull; National Agricultural Research System
          </p>
        </div>
      </footer>
    </div>
  );
};
