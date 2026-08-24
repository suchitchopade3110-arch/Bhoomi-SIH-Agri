import React, { useState, useEffect } from 'react';
import { Sprout, Menu, X } from 'lucide-react';

export default function Navbar({ 
  onOpenOfficerPortal
}) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-md py-3' : 'bg-white/95 backdrop-blur-md py-4'
    }`}>
      <div className="container mx-auto px-6 flex items-center justify-between">
        
        {/* Brand */}
        <a href="#" className="flex items-center gap-2 group">
          <div className="text-[#1b8c47]">
            <Sprout className="w-8 h-8 fill-current" strokeWidth={1} />
          </div>
          <div className="leading-tight">
            <div className="text-xl font-bold tracking-tight text-slate-900">Bhoomi</div>
            <p className="text-[10px] font-medium text-slate-500 uppercase tracking-wider">Officer Portal</p>
          </div>
        </a>

        {/* Desktop Navigation */}
        <nav className="hidden lg:flex items-center gap-8 font-semibold text-slate-700 text-sm">
          <a href="#hero" className="text-[#1b8c47] border-b-2 border-[#1b8c47] pb-1">Home</a>
          <a href="#features" className="hover:text-[#1b8c47] transition-colors">Capabilities</a>
          <a href="#how-it-works" className="hover:text-[#1b8c47] transition-colors">Workflow</a>

        </nav>

        {/* Action Buttons */}
        <div className="hidden lg:flex items-center gap-4">
          <button 
            onClick={onOpenOfficerPortal}
            className="bg-[#1b8c47] hover:bg-green-700 text-white px-5 py-2.5 rounded-md font-bold transition-colors shadow-sm"
          >
            Login as Officer
          </button>
        </div>

        {/* Mobile menu trigger */}
        <button 
          className="lg:hidden p-2 text-slate-600 hover:text-green-700 bg-slate-50 rounded-lg"
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        >
          {isMobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>

      </div>

      {/* Mobile dropdown menu */}
      {isMobileMenuOpen && (
        <div className="lg:hidden bg-white border-b border-slate-200 px-6 py-6 space-y-4 shadow-xl">
          <nav className="flex flex-col space-y-3 font-semibold text-slate-800 text-base">
            <a href="#features" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-[#1b8c47]">Capabilities</a>
            <a href="#how-it-works" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-[#1b8c47]">Workflow</a>

            
            <button 
              onClick={() => {
                onOpenOfficerPortal();
                setIsMobileMenuOpen(false);
              }}
              className="mt-4 bg-[#1b8c47] text-white py-3 rounded-md font-bold text-center shadow-sm"
            >
              Login as Officer
            </button>
          </nav>
        </div>
      )}
    </header>
  );
}
