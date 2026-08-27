import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  MapPin,
  Layers,
  FileCheck2,
  BarChart3,
  Archive,
  Compass,
  ChevronRight,
  Menu,
  X,
  Building2,
  Landmark,
  BadgeCheck,
  Map,
  Scale,
} from 'lucide-react';
import bhoomiLogo from '../../../assets/bhoomi_logo.png';
import officerHeroBg from '../../../assets/officer_hero_bg.jpg';
import { authStore } from '../../../core/auth/auth_store';

export const OfficerLandingPage: React.FC = () => {
  const officer = authStore.getCurrentOfficer();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 selection:bg-[#2E7D32] selection:text-white font-sans antialiased overflow-x-hidden">
      {/* ========================================================================= */}
      {/* 1. TOP INSTITUTIONAL NAVIGATION BAR (LIGHT DASHBOARD THEME) */}
      {/* ========================================================================= */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-200/80 bg-white/95 backdrop-blur-md shadow-xs">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Brand & Portal Identification */}
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
                    OFFICER PORTAL
                  </span>
                </div>
                <p className="text-[11px] text-slate-500 font-medium">
                  {officer.jurisdiction}
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
              Officer Capabilities
            </a>
            <a
              href="#workflow"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              Operational Workflow
            </a>
            <a
              href="#governance"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              Cadastral Governance
            </a>
            <a
              href="#jurisdiction"
              className="hover:text-[#2E7D32] transition-colors py-1"
            >
              District Jurisdiction
            </a>
          </nav>

          {/* Right Action: Enter Officer Workspace CTA */}
          <div className="hidden sm:flex items-center gap-4">
            <Link
              to="/queue"
              className="group inline-flex items-center gap-2 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] px-4 py-2 text-xs font-bold text-white shadow-xs transition-all duration-200 hover:shadow-sm"
            >
              <span>Officer Workspace</span>
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
              Officer Capabilities
            </a>
            <a
              href="#workflow"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              Operational Workflow
            </a>
            <a
              href="#governance"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              Cadastral Governance
            </a>
            <a
              href="#jurisdiction"
              onClick={() => setMobileMenuOpen(false)}
              className="block text-xs font-semibold text-slate-600 hover:text-[#2E7D32]"
            >
              District Jurisdiction
            </a>
            <div className="pt-2">
              <Link
                to="/queue"
                onClick={() => setMobileMenuOpen(false)}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] py-2.5 text-xs font-bold text-white shadow-xs"
              >
                <span>Enter Officer Workspace</span>
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
        {/* Agricultural Background Image with Light Tone Layer */}
        <div className="absolute inset-0 z-0">
          <img
            src={officerHeroBg}
            alt="Aerial Agricultural Farmland and Irrigation Canals"
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
                  Cadastral Land Verification & District Governance
                </span>
              </div>

              {/* Main Headline */}
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight text-slate-900 leading-[1.18]">
                Empowering Agricultural Officers with{' '}
                <span className="text-[#2E7D32]">
                  Spatial Land Verification & Program Oversight
                </span>
              </h1>

              {/* Sub-headline */}
              <p className="text-sm sm:text-base text-slate-600 leading-relaxed max-w-2xl font-normal">
                BHOOMI connects field officers, revenue administrators, and smallholder farmers.
                Inspect GeoJSON cadastral polygons against official revenue maps, authenticate farm acreage,
                prevent spatial overlaps, and unlock verified agricultural scheme benefits with complete audit integrity.
              </p>

              {/* CTA Group */}
              <div className="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5">
                <Link
                  to="/queue"
                  className="inline-flex items-center justify-center gap-2.5 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] px-6 py-3.5 text-sm font-bold text-white shadow-xs transition-all duration-200 hover:shadow-sm"
                >
                  <span>Access Land Verification Queue</span>
                  <ArrowRight className="h-4 w-4" />
                </Link>

                <a
                  href="#capabilities"
                  className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 px-5 py-3.5 text-sm font-bold text-slate-700 shadow-xs transition-all duration-200"
                >
                  <MapPin className="h-4 w-4 text-[#2E7D32]" />
                  <span>Explore Cadastral Tools</span>
                </a>
              </div>

              {/* Metric Highlights Strip */}
              <div className="pt-6 border-t border-slate-200/80 grid grid-cols-2 sm:grid-cols-3 gap-4 text-left">
                <div className="space-y-0.5">
                  <div className="text-xl font-black text-slate-900">±5% Tolerance</div>
                  <div className="text-[11px] text-slate-500">Automated Area Variance Check</div>
                </div>
                <div className="space-y-0.5">
                  <div className="text-xl font-black text-[#2E7D32]">100% GIS Audit</div>
                  <div className="text-[11px] text-slate-500">Zero Spatial Overlap Enforcement</div>
                </div>
                <div className="space-y-0.5 col-span-2 sm:col-span-1">
                  <div className="text-xl font-black text-slate-800">Signed Certificates</div>
                  <div className="text-[11px] text-slate-500">Cryptographic Officer Approvals</div>
                </div>
              </div>
            </div>

            {/* Right Column: Live Cadastral Review Card (Light Dashboard Style) */}
            <div className="lg:col-span-5">
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4 relative">
                {/* Accent Top Border */}
                <div className="absolute top-0 left-0 right-0 h-1 bg-[#2E7D32] rounded-t-2xl" />

                {/* Card Header */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-[#2E7D32]/10 text-[#2E7D32]">
                      <FileCheck2 className="h-4 w-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-slate-900">Parcel ID: LREC-ERD-142</span>
                      <p className="text-[10px] text-slate-500">Survey No. 142/3B &bull; Modakkurichi Taluk</p>
                    </div>
                  </div>
                  <span className="rounded-full bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 text-[10px] font-bold text-emerald-800">
                    Pending Verification
                  </span>
                </div>

                {/* Land Record Summary */}
                <div className="space-y-2.5 text-xs">
                  <div className="flex justify-between items-center rounded-xl bg-slate-50/80 p-3 border border-slate-200/60">
                    <span className="text-slate-500">Applicant Farmer:</span>
                    <span className="font-bold text-slate-800">Murugan K. (Tamil Nadu)</span>
                  </div>

                  <div className="flex justify-between items-center rounded-xl bg-slate-50/80 p-3 border border-slate-200/60">
                    <span className="text-slate-500">Claimed vs. Computed Area:</span>
                    <span className="font-bold text-[#2E7D32]">2.00 Ac Claimed &bull; 1.85 Ac FMB</span>
                  </div>

                  <div className="flex justify-between items-center rounded-xl bg-slate-50/80 p-3 border border-slate-200/60">
                    <span className="text-slate-500">Cadastral Boundary Status:</span>
                    <span className="font-bold text-slate-800">OpenStreetMap Polygon Aligned</span>
                  </div>

                  <div className="rounded-xl bg-emerald-50/60 border border-emerald-200/70 p-3 space-y-1.5">
                    <div className="flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32] uppercase tracking-wider">
                      <BadgeCheck className="h-3.5 w-3.5" />
                      <span>Program Eligibility Impact</span>
                    </div>
                    <p className="text-[11px] text-slate-600 leading-relaxed">
                      Officer approval unlocks PM-KISAN installment validation, fertilizer subsidies, and full farm advisory access.
                    </p>
                  </div>
                </div>

                {/* Card Action */}
                <div className="pt-2">
                  <Link
                    to="/queue"
                    className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-100 hover:bg-slate-200 border border-slate-200 py-2.5 text-xs font-bold text-slate-800 transition-colors"
                  >
                    <span>Inspect Parcel in Officer Queue</span>
                    <ChevronRight className="h-4 w-4 text-[#2E7D32]" />
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 3. OFFICER CAPABILITIES (LIGHT THEME GRID) */}
      {/* ========================================================================= */}
      <section id="capabilities" className="py-20 bg-white relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {/* Section Header */}
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
              <Compass className="h-3.5 w-3.5" />
              <span>Officer Capabilities</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              Spatial Cadastral & Administrative Decision Tools
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              Engineered specifically for Agricultural Officers, VAOs, and Revenue Administrators
              to streamline land authentication and agricultural governance.
            </p>
          </div>

          {/* Capabilities Grid */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Capability 1 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <Map className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Spatial Cadastral Verification
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Inspect farmer-submitted GeoJSON boundary polygons rendered directly on OpenStreetMap and satellite layers.
                Verify field shape, plot orientation, and revenue survey boundary alignment.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>GeoJSON Polygon Overlay</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 2 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <BadgeCheck className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Scheme Eligibility & Subsidy Gate
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Ensure agricultural subsidies, crop insurance claims, and PM-KISAN benefits are strictly channeled to legitimate, authenticated landholders with zero multi-claiming.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Targeted Scheme Delivery</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 3 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <BarChart3 className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                District Spatial Analytics & KPIs
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Track verification progress across Taluks (Erode, Bhavani, Gobichettipalayam, Modakkurichi).
                Evaluate total authenticated acreages, resolution throughput, and approval ratios.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Taluk Revenue Dashboards</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 4 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <Scale className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Discrepancy & Overlap Prevention
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Automated topological checks flag acreage deviations exceeding ±5% tolerance or encroaching boundaries, prompting officer review and preventing fraudulent claims.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Topological Conflict Shield</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 5 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <ShieldCheck className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Cryptographic Officer Signatures
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Every approved or rejected land parcel is permanently signed with the designated officer’s credentials and timestamp, generating an unalterable government audit trail.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Tamper-Proof Audit Trail</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>

            {/* Capability 6 */}
            <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-6 hover:bg-white hover:border-[#2E7D32]/40 hover:shadow-md transition-all duration-200 group">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#2E7D32]/10 border border-[#2E7D32]/20 text-[#2E7D32] group-hover:bg-[#2E7D32] group-hover:text-white transition-colors duration-200">
                <Archive className="h-5 w-5" />
              </div>
              <h3 className="mt-4 text-base font-bold text-slate-900 group-hover:text-[#2E7D32] transition-colors">
                Verified Cadastral Archive
              </h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Access a searchable repository of historical land parcel decisions. Filter by Survey Number, Farm ID, village, or approval status for transparent dispute resolution.
              </p>
              <div className="mt-4 flex items-center gap-1.5 text-[11px] font-bold text-[#2E7D32]">
                <span>Historical Parcel Index</span>
                <ChevronRight className="h-3 w-3" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 4. OPERATIONAL WORKFLOW (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section id="workflow" className="py-20 bg-slate-50 relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
              <Layers className="h-3.5 w-3.5" />
              <span>4-Step Verification Lifecycle</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              From Farmer Plot Registration to Official Certification
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              A transparent, high-integrity governance pipeline ensuring every acre is georeferenced, authenticated, and accounted for.
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
                  Field Capture
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Farmer Parcel Registration</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Farmer enters Survey Number, village, and outlines field boundaries via mobile GPS polygon mapping tools.
              </p>
            </div>

            {/* Step 2 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-700 font-black text-xs border border-amber-200">
                  02
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  Automated Checks
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Revenue & GIS Cross-Check</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                The platform computes polygon surface area, checks variance against stated acreage, and detects spatial overlaps with neighboring plots.
              </p>
            </div>

            {/* Step 3 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-blue-50 text-blue-700 font-black text-xs border border-blue-200">
                  03
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  Officer Review
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Officer Cadastral Audit</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Agricultural Officer inspects the boundary map, reviews FMB documentation, and signs official verification or rejection remarks.
              </p>
            </div>

            {/* Step 4 */}
            <div className="relative rounded-2xl border border-slate-200 bg-white p-6 space-y-3.5 shadow-xs">
              <div className="flex items-center justify-between">
                <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-purple-50 text-purple-700 font-black text-xs border border-purple-200">
                  04
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                  Program Unlock
                </span>
              </div>
              <h3 className="text-sm font-bold text-slate-900">Ecosystem Program Activation</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Verified farm status is propagated to the BHOOMI intelligence layer, unlocking tailored farm advisory, insurance claims, and subsidies.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 5. CADASTRAL GOVERNANCE & INTEGRITY MATRIX (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section id="governance" className="py-20 bg-white relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            <div className="lg:col-span-6 space-y-6">
              <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3.5 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
                <Building2 className="h-4 w-4" />
                <span>Institutional Governance Standards</span>
              </div>

              <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
                Modernizing Land Revenue Verification for the Digital Era
              </h2>

              <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                Traditional paper-based land audits suffer from delayed inspections, boundary ambiguities, and vulnerability to fraudulent duplicate claims.
                BHOOMI provides Agricultural Officers with high-precision GIS tools backed by cryptographic audit trails.
              </p>

              <div className="space-y-3 pt-2">
                <div className="flex items-start gap-3 rounded-2xl bg-slate-50 p-4 border border-slate-200/80">
                  <CheckCircle2 className="h-5 w-5 text-[#2E7D32] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Precise GeoJSON Spatial Anchors</h4>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Parcels are anchored with exact GPS coordinate vertices, preventing ambiguous boundary estimations.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-2xl bg-slate-50 p-4 border border-slate-200/80">
                  <CheckCircle2 className="h-5 w-5 text-[#2E7D32] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Immutable Decision History</h4>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Every approval, modification, and rejection record is permanently archived with officer identity tags.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-2xl bg-slate-50 p-4 border border-slate-200/80">
                  <CheckCircle2 className="h-5 w-5 text-[#2E7D32] shrink-0 mt-0.5" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Instant Scheme Qualification Validation</h4>
                    <p className="text-[11px] text-slate-500 mt-0.5">
                      Government agencies and financial institutions can instantly confirm land verification status via secure API endpoints.
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Comparison Matrix Table Card */}
            <div className="lg:col-span-6">
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs space-y-4">
                <div className="border-b border-slate-100 pb-3">
                  <h3 className="text-sm font-bold text-slate-900">Verification Modernization Matrix</h3>
                  <p className="text-[11px] text-slate-500">Legacy Manual Revenue Verification vs. BHOOMI Officer Portal</p>
                </div>

                <div className="space-y-2 text-xs">
                  {/* Row 1 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Boundary Mapping</div>
                    <div className="col-span-4 text-red-700 bg-red-50/80 px-2 py-0.5 rounded text-[10px] border border-red-100">Paper FMB Sketches</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>Interactive GeoJSON</span>
                    </div>
                  </div>

                  {/* Row 2 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Overlap Detection</div>
                    <div className="col-span-4 text-red-700 bg-red-50/80 px-2 py-0.5 rounded text-[10px] border border-red-100">Manual Visual Guess</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>Zero-Overlap Filter</span>
                    </div>
                  </div>

                  {/* Row 3 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Area Variance Check</div>
                    <div className="col-span-4 text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[10px]">Untracked Variance</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>Automated ±5% Check</span>
                    </div>
                  </div>

                  {/* Row 4 */}
                  <div className="grid grid-cols-12 gap-2 rounded-xl bg-slate-50 p-3 items-center border border-slate-200/60">
                    <div className="col-span-4 font-bold text-slate-800 text-[11px]">Scheme Integration</div>
                    <div className="col-span-4 text-slate-500 bg-slate-100 px-2 py-0.5 rounded text-[10px]">Physical Certificates</div>
                    <div className="col-span-4 text-[#2E7D32] bg-emerald-50 px-2 py-0.5 rounded font-bold text-[10px] border border-emerald-200 flex items-center gap-1">
                      <ShieldCheck className="h-3.5 w-3.5 shrink-0" />
                      <span>Instant Digital Link</span>
                    </div>
                  </div>
                </div>

                <div className="pt-2">
                  <div className="rounded-xl bg-[#2E7D32]/5 border border-[#2E7D32]/20 p-2.5 text-center">
                    <p className="text-[11px] text-[#2E7D32] font-semibold">
                      Enforced by BHOOMI Cadastral Governance Layer (SIH25076)
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ========================================================================= */}
      {/* 6. DISTRICT JURISDICTION COVERAGE (LIGHT THEME) */}
      {/* ========================================================================= */}
      <section id="jurisdiction" className="py-20 bg-slate-50 relative border-b border-slate-200/80">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto space-y-3">
            <div className="inline-flex items-center gap-2 rounded-full bg-[#2E7D32]/10 border border-[#2E7D32]/20 px-3 py-1 text-[11px] font-extrabold uppercase tracking-widest text-[#2E7D32]">
              <Landmark className="h-3.5 w-3.5" />
              <span>Administrative Jurisdiction</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              Taluk Revenue Divisions & Field Coverage
            </h2>
            <p className="text-sm text-slate-500 leading-relaxed">
              Monitoring agrarian parcel registration across district taluk circles with real-time verification status.
            </p>
          </div>

          {/* Taluk Cards */}
          <div className="mt-16 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Taluk Division</span>
              <h4 className="text-sm font-bold text-slate-900">Erode Taluk</h4>
              <p className="text-[11px] text-slate-500">
                Covers Perundurai, Modakkurichi, and Erode urban fringe agricultural parcels with 65% verification compliance.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Taluk Division</span>
              <h4 className="text-sm font-bold text-slate-900">Gobichettipalayam</h4>
              <p className="text-[11px] text-slate-500">
                Paddy and sugarcane canal-irrigated command areas (Alukuli, Kunderipallam) with 80% verification rate.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Taluk Division</span>
              <h4 className="text-sm font-bold text-slate-900">Bhavani Taluk</h4>
              <p className="text-[11px] text-slate-500">
                River basin parcels, turmeric clusters, and Anthiyur agrarian tracts with active spatial boundary auditing.
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 space-y-2 shadow-xs hover:border-[#2E7D32]/30 transition-colors">
              <span className="text-[10px] font-bold text-[#2E7D32] uppercase tracking-wider">Taluk Division</span>
              <h4 className="text-sm font-bold text-slate-900">Sathyamangalam</h4>
              <p className="text-[11px] text-slate-500">
                Horticultural orchards, banana plantations, and dryland pulses with zero-overlap spatial certification.
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
            <span className="flex h-2 w-2 rounded-full bg-[#2E7D32]" />
            <span className="text-xs font-bold uppercase tracking-widest text-[#2E7D32]">
              Active Officer Session: {officer.name} ({officer.verifierTag})
            </span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-slate-900 tracking-tight">
            Ready to Authenticate Pending Land Parcels?
          </h2>

          <p className="text-sm sm:text-base text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Logged in with official verification credentials for <strong className="text-slate-900 font-bold">{officer.jurisdiction}</strong>.
            Access the land review console to inspect pending survey numbers, resolve boundaries, and sign approvals.
          </p>

          <div className="pt-3 flex flex-col sm:flex-row items-center justify-center gap-3.5">
            <Link
              to="/queue"
              className="inline-flex w-full sm:w-auto items-center justify-center gap-2.5 rounded-xl bg-[#2E7D32] hover:bg-[#1B5E20] px-8 py-3.5 text-sm font-bold text-white shadow-xs transition-all duration-200 hover:shadow-sm"
            >
              <span>Launch Land Verification Queue</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              to="/analytics"
              className="inline-flex w-full sm:w-auto items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 px-7 py-3.5 text-sm font-bold text-slate-700 shadow-xs transition-colors"
            >
              <span>View District Spatial Analytics</span>
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
                  Officer Portal
                </span>
              </div>
              <p className="text-xs text-slate-500 max-w-md leading-relaxed">
                BHOOMI Smart Land Verification & District Agricultural Administration Platform.
                Developed for Agricultural Officers, Village Administrative Officers (VAOs), and Regional Administrators.
              </p>
            </div>

            {/* Quick Links Column */}
            <div className="space-y-2.5">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-800">
                Officer Console
              </span>
              <ul className="space-y-2 text-xs">
                <li>
                  <Link to="/queue" className="hover:text-[#2E7D32] transition-colors">
                    Land Verification Queue
                  </Link>
                </li>
                <li>
                  <Link to="/archive" className="hover:text-[#2E7D32] transition-colors">
                    Verified Land Archive
                  </Link>
                </li>
                <li>
                  <Link to="/analytics" className="hover:text-[#2E7D32] transition-colors">
                    District Spatial Analytics
                  </Link>
                </li>
                <li>
                  <Link to="/help" className="hover:text-[#2E7D32] transition-colors">
                    SOP & Guidelines
                  </Link>
                </li>
              </ul>
            </div>

            {/* Institution Column */}
            <div className="space-y-2.5">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-800">
                Revenue Administration
              </span>
              <ul className="space-y-2 text-xs">
                <li>
                  <Link to="/settings" className="hover:text-[#2E7D32] transition-colors">
                    Officer Credentials & Tag
                  </Link>
                </li>
                <li>
                  <a href="#governance" className="hover:text-[#2E7D32] transition-colors">
                    Cadastral Audit Standards
                  </a>
                </li>
                <li>
                  <a href="#jurisdiction" className="hover:text-[#2E7D32] transition-colors">
                    Taluk Revenue Boundaries
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-slate-500">
            <p>
              &copy; {new Date().getFullYear()} BHOOMI Land Verification System. All rights reserved.
            </p>
            <p className="font-mono text-[10px] text-slate-500">
              Officer Node: {officer.verifierTag} &bull; Smart India Hackathon SIH25076
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};
