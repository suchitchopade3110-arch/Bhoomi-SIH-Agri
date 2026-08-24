import React from 'react';
import { 
  Sprout, 
  Facebook, 
  Instagram, 
  Youtube, 
  Twitter 
} from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#062415] text-slate-400 py-16 text-sm">
      <div className="container mx-auto px-6">
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10 pb-12 border-b border-slate-800">
          
          {/* Col 1 & 2: Branding & Mission */}
          <div className="lg:col-span-2 space-y-4">
            <div className="flex items-center gap-2">
              <div className="text-[#1b8c47]">
                <Sprout className="w-8 h-8 fill-current text-green-500" strokeWidth={1} />
              </div>
              <div className="leading-tight">
                <div className="text-xl font-bold tracking-tight text-white">Bhoomi</div>
                <p className="text-[10px] font-medium text-slate-400">AI Farm Companion</p>
              </div>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed max-w-sm mt-4">
              Empowering farmers with knowledge, technology and trust.
            </p>
          </div>

          {/* Col 3: Quick Links */}
          <div className="space-y-4">
            <h4 className="font-bold text-white">Quick Links</h4>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><a href="#hero" className="hover:text-green-400 transition-colors">Home</a></li>
              <li><a href="#features" className="hover:text-green-400 transition-colors">Features</a></li>
              <li><a href="#how-it-works" className="hover:text-green-400 transition-colors">How It Works</a></li>
            </ul>
          </div>

          {/* Col 4: Resources */}
          <div className="space-y-4">
            <h4 className="font-bold text-white">Resources</h4>
            <ul className="space-y-2 text-sm text-slate-400">
              <li><a href="#" className="hover:text-green-400 transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Help Center</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Privacy Policy</a></li>
            </ul>
          </div>

          {/* Col 5: Company & Socials */}
          <div className="space-y-4">
            <h4 className="font-bold text-white">Company</h4>
            <ul className="space-y-2 text-sm text-slate-400 mb-6">
              <li><a href="#" className="hover:text-green-400 transition-colors">About Us</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Contact Us</a></li>
              <li><a href="#" className="hover:text-green-400 transition-colors">Careers</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom copyright and social */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <p>© 2024 Bhoomi. All rights reserved.</p>
          
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <span className="font-bold text-white hidden sm:block">Stay Connected</span>
            <div className="flex items-center gap-4 text-slate-400">
              <a href="#" className="hover:text-blue-500 transition-colors"><Facebook size={18} /></a>
              <a href="#" className="hover:text-pink-500 transition-colors"><Instagram size={18} /></a>
              <a href="#" className="hover:text-red-500 transition-colors"><Youtube size={18} /></a>
              <a href="#" className="hover:text-blue-400 transition-colors"><Twitter size={18} /></a>
            </div>
          </div>
        </div>

      </div>
    </footer>
  );
}
