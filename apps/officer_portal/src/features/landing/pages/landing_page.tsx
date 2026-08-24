import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  MapPin,
  FileCheck2,
  BarChart3,
  Layers,
  ArrowRight,
  Sparkles,
  ChevronRight,
  Activity,
  CheckCircle2,
  Clock,
  Compass,
  Cpu
} from 'lucide-react';
import bhoomiLogo from '../../../assets/bhoomi.png';
import officerHeroBg from '../../../assets/officer_hero_bg.jpg';

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
                  OFFICER PORTAL
                </span>
              </div>
              <p className="text-[11px] font-semibold text-slate-500">
                Agricultural Administration &amp; Land Intelligence
              </p>
            </div>
          </Link>

          {/* Quick Nav Links */}
          <nav className="hidden md:flex items-center gap-8 text-xs font-bold text-slate-600">
            <a href="#overview" className="transition-colors hover:text-[#2E7D32]">
              Overview
            </a>
            <a href="#capabilities" className="transition-colors hover:text-[#2E7D32]">
              Capabilities
            </a>
            <a href="#workflow" className="transition-colors hover:text-[#2E7D32]">
              Workflow
            </a>
            <a href="#outcomes" className="transition-colors hover:text-[#2E7D32]">
              Outcomes
            </a>
          </nav>

          {/* Primary CTA */}
          <div className="flex items-center gap-3">
            <Link
              to="/"
              className="flex items-center gap-2 rounded-xl bg-[#2E7D32] px-4 py-2.5 text-xs font-extrabold text-white shadow-xs transition-all hover:bg-[#1B5E20] hover:shadow-md active:scale-98"
            >
              <span>Access Portal</span>
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
              src={officerHeroBg}
              alt="Lush agricultural landscape"
              className="h-full w-full object-cover object-center"
            />
            {/* Multi-layered Vignette & Dark Emerald Overlay for maximum readability */}
            <div className="absolute inset-0 bg-gradient-to-r from-slate-950/95 via-slate-900/85 to-slate-950/65" />
            <div className="absolute inset-0 bg-radial-at-t from-transparent via-slate-950/40 to-slate-950/90" />
          </div>

          <div className="relative z-10 mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
            <div className="max-w-3xl space-y-6">
              {/* Eyebrow Badge */}
              <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3.5 py-1.5 backdrop-blur-md">
                <Sparkles className="h-3.5 w-3.5 text-emerald-400" />
                <span className="text-xs font-extrabold tracking-wide uppercase text-emerald-300">
                  BHOOMI Agricultural Intelligence
                </span>
              </div>

              {/* Main Headline */}
              <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight text-white leading-[1.15]">
                Smarter Decisions for <span className="text-emerald-400">Stronger Agriculture.</span>
              </h1>

              {/* Supporting Description */}
              <p className="text-sm sm:text-base lg:text-lg text-slate-300 font-medium leading-relaxed max-w-2xl">
                A unified spatial intelligence platform empowering revenue officers and agricultural administrators to monitor regional farmlands, verify cadastral boundaries, evaluate crop health telemetry, and expedite official approvals.
              </p>

              {/* CTAs */}
              <div className="flex flex-wrap items-center gap-4 pt-2">
                <Link
                  to="/"
                  className="flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-3.5 text-sm font-extrabold text-slate-950 shadow-lg shadow-emerald-500/20 transition-all hover:bg-emerald-400 hover:shadow-emerald-500/30 active:scale-98"
                >
                  <span>Access Officer Portal</span>
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <a
                  href="#capabilities"
                  className="flex items-center gap-2 rounded-xl border border-white/20 bg-white/10 px-6 py-3.5 text-sm font-extrabold text-white backdrop-blur-md transition-all hover:bg-white/20 hover:border-white/30 active:scale-98"
                >
                  <span>Explore Platform</span>
                  <ChevronRight className="h-4 w-4 text-slate-300" />
                </a>
              </div>

              {/* Live Metric Strip */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 pt-8 border-t border-white/10">
                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                    <ShieldCheck className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-black text-white">100%</div>
                    <div className="text-[11px] text-slate-400 font-medium">Cadastral Audit Integrity</div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                    <Activity className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-black text-white">Real-Time</div>
                    <div className="text-[11px] text-slate-400 font-medium">Farm Health Telemetry</div>
                  </div>
                </div>

                <div className="flex items-center gap-3 col-span-2 sm:col-span-1">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                    <Clock className="h-5 w-5" />
                  </div>
                  <div>
                    <div className="text-lg font-black text-white">&lt;24 hrs</div>
                    <div className="text-[11px] text-slate-400 font-medium">Verification Turnaround</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 3. Platform Capabilities */}
        <section id="capabilities" className="py-20 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <div className="inline-flex items-center gap-1.5 rounded-full bg-[#2E7D32]/10 px-3 py-1 text-xs font-bold text-[#2E7D32]">
                <Cpu className="h-3.5 w-3.5" />
                <span>CORE CAPABILITIES</span>
              </div>
              <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
                Comprehensive Administration Engine
              </h2>
              <p className="mt-3 text-sm text-slate-600">
                Built specifically for district and taluk-level agricultural officers to streamline land review workflows and enhance field visibility.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {/* Capability 1 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <BarChart3 className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Regional Agricultural Insights
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Aggregated crop condition indices, weather trends, and drought susceptibility across taluks to guide administrative decisions.
                </p>
              </div>

              {/* Capability 2 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <MapPin className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Farmer &amp; Field Intelligence
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Interactive OpenStreetMap polygon overlays correlating self-reported survey numbers with official cadastral coordinates.
                </p>
              </div>

              {/* Capability 3 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <FileCheck2 className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Issue Monitoring &amp; Queue
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Centralized queue management for pending land records, area variance alerts, and historical approval archives.
                </p>
              </div>

              {/* Capability 4 */}
              <div className="rounded-2xl border border-slate-200/80 bg-slate-50/50 p-6 transition-all hover:bg-white hover:shadow-md hover:border-emerald-200 group">
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-[#2E7D32] transition-transform group-hover:scale-110">
                  <ShieldCheck className="h-6 w-6" />
                </div>
                <h3 className="mt-4 text-base font-extrabold text-slate-900">
                  Data-Driven Decision Support
                </h3>
                <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                  Cryptographically verified approval actions, note recording, and tamper-proof verification history for official records.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 4. How BHOOMI Supports Officers (Workflow) */}
        <section id="workflow" className="py-20 bg-slate-100/70 border-y border-slate-200">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <div className="inline-flex items-center gap-1.5 rounded-full bg-[#2E7D32]/10 px-3 py-1 text-xs font-bold text-[#2E7D32]">
                <Compass className="h-3.5 w-3.5" />
                <span>STRUCTURED WORKFLOW</span>
              </div>
              <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
                From Field Submission to Official Verification
              </h2>
              <p className="mt-3 text-sm text-slate-600">
                A seamless, automated 4-stage pipeline that removes bureaucratic friction and ensures absolute land integrity.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
              {/* Step 1 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">01</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <MapPin className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Field Data Submission</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    Farmer submits self-reported survey number, acreage, and GPS-drawn parcel boundary via the mobile app.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32] flex items-center gap-1">
                  <span>Farmer App</span>
                </div>
              </div>

              {/* Step 2 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">02</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <Cpu className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Intelligent Analysis</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    BHOOMI backend cross-references cadastral registry data, area geometry, and satellite boundary points.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32] flex items-center gap-1">
                  <span>Automated Validation</span>
                </div>
              </div>

              {/* Step 3 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">03</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <BarChart3 className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Actionable Review</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    Officer inspects high-resolution polygon overlays, variance metrics, and farmer identity records in the queue.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32] flex items-center gap-1">
                  <span>Officer Portal</span>
                </div>
              </div>

              {/* Step 4 */}
              <div className="relative rounded-2xl bg-white p-6 shadow-xs border border-slate-200 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-2xl font-black text-[#2E7D32]/30">04</span>
                    <div className="h-8 w-8 rounded-full bg-emerald-50 flex items-center justify-center text-[#2E7D32]">
                      <CheckCircle2 className="h-4 w-4" />
                    </div>
                  </div>
                  <h4 className="mt-4 text-sm font-extrabold text-slate-900">Official Approval</h4>
                  <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                    One-click cryptographic verification approves the parcel and instantly unlocks farmer scheme entitlements.
                  </p>
                </div>
                <div className="mt-6 pt-3 border-t border-slate-100 text-[11px] font-bold text-[#2E7D32] flex items-center gap-1">
                  <span>Verified Registry</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 5. Key Outcomes */}
        <section id="outcomes" className="py-20 bg-white">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-16">
              <div className="inline-flex items-center gap-1.5 rounded-full bg-[#2E7D32]/10 px-3 py-1 text-xs font-bold text-[#2E7D32]">
                <Activity className="h-3.5 w-3.5" />
                <span>MEASURABLE IMPACT</span>
              </div>
              <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl">
                Key Outcomes for Revenue Administration
              </h2>
              <p className="mt-3 text-sm text-slate-600">
                Delivering transparency, speed, and precision to agricultural governance.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">4x Faster</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Accelerated Verification</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Reduces verification turnaround from weeks to within 24 hours.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">100%</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Audit Traceability</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Every decision is tied to an officer ID and recorded with timestamped verification logs.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">0-Drift</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Geo-Precision</h4>
                <p className="mt-1 text-xs text-slate-500">
                  OpenStreetMap spatial snapping guarantees boundary precision down to the sub-acre level.
                </p>
              </div>

              <div className="rounded-2xl border border-slate-200 p-6 bg-slate-50/50">
                <div className="text-3xl font-black text-[#2E7D32]">Proactive</div>
                <h4 className="mt-2 text-sm font-bold text-slate-900">Regional Health</h4>
                <p className="mt-1 text-xs text-slate-500">
                  Immediate early warning alerts for pest breakouts, soil stress, and moisture anomalies.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* 6. Final Call to Action Section */}
        <section className="py-16 bg-[#1B5E20] text-white">
          <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center space-y-6">
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
              Ready to Modernize Agricultural Administration?
            </h2>
            <p className="text-sm sm:text-base text-emerald-100 max-w-2xl mx-auto">
              Access the BHOOMI Officer Portal to review pending land parcels, analyze regional crop metrics, and manage official verifications.
            </p>
            <div className="pt-2">
              <Link
                to="/"
                className="inline-flex items-center gap-2 rounded-xl bg-white px-8 py-3.5 text-sm font-extrabold text-[#1B5E20] shadow-lg transition-all hover:bg-emerald-50 hover:shadow-xl active:scale-98"
              >
                <span>Enter Officer Portal</span>
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
            <Layers className="h-4 w-4 text-[#2E7D32]" />
            <span className="font-bold text-slate-700">BHOOMI Agricultural Intelligence Platform</span>
            <span>&bull;</span>
            <span>SIH25076</span>
          </div>
          <p className="text-center sm:text-right text-slate-400">
            &copy; {new Date().getFullYear()} Government of Tamil Nadu &bull; Department of Agricultural Welfare
          </p>
        </div>
      </footer>
    </div>
  );
};
