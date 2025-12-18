import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FileText, 
  ShieldCheck, 
  Scale, 
  Clock, 
  Download, 
  Mic, 
  ArrowRight,
  Gavel,
  CheckCircle2,
  Handshake
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import HomepageHero from '../components/HomepageHero';
import WhoWardIsForSection from '../components/WhoWardIsForSection';
import ProductV0Section from '../components/ProductV0Section';
import FromChaosToPacketSection from '../components/FromChaosToPacketSection';

export default function Landing() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white border-b border-slate-200">
        <div className="container mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-slate-900 w-8 h-8 rounded-sm flex items-center justify-center text-white font-serif font-bold">W</div>
            <span className="text-xl font-bold tracking-tight text-slate-900">Ward</span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-medium text-slate-600">
            <Link to="/" className="hover:text-slate-900 transition-colors">Home</Link>
            <Link to="/how-it-works" className="hover:text-slate-900 transition-colors">How It Works</Link>
            <Link to="/why-ward" className="hover:text-slate-900 transition-colors">Why Ward</Link>
            <Link to="/contact" className="hover:text-slate-900 transition-colors">Contact</Link>
          </div>
          <div className="flex gap-4">
            <Link to="/login">
              <Button variant="ghost" className="text-slate-600 hover:text-slate-900">Log in</Button>
            </Link>
            <Link to="/register">
              <Button className="bg-slate-900 hover:bg-slate-800 text-white rounded-md px-6">
                Start Pilot
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section - Using new HomepageHero component */}
      <HomepageHero />

      {/* Who Ward is For Section */}
      <WhoWardIsForSection />

      {/* Product v0 Section */}
      <ProductV0Section />

      {/* From Chaos to Packet Section */}
      <FromChaosToPacketSection />

      {/* How It Works (Evidence Flow) - Simplified */}
      <section id="how-it-works" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              How it works
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Three steps from chaos to dispute packet
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-12 relative max-w-5xl mx-auto">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-slate-100 -z-10"></div>

            <StepCard 
              number="1"
              icon={Mic}
              title="Capture"
              description="Drivers speak in their own language. We record and translate the ground truth."
            />
            <StepCard 
              number="2"
              icon={Clock}
              title="Timeline"
              description="Every word is timestamped and geo-tagged against your free time limits."
            />
            <StepCard 
              number="3"
              icon={Gavel}
              title="Defend"
              description="Generate a dispute packet instantly to prove the delay wasn't your fault."
            />
          </div>
          <div className="text-center mt-12">
            <Link to="/how-it-works">
              <Button variant="outline" className="border-slate-300">
                See detailed workflow
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Dispute Export Section - Simplified */}
      <section id="dispute-export" className="py-24 bg-slate-50 border-y border-slate-200">
        <div className="container mx-auto px-6 max-w-4xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Click to Dispute
            </h2>
            <p className="text-lg text-slate-600 mb-8">
              Don't dig through emails. Generate a dispute packet instantly.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center p-6 bg-white rounded-lg border border-slate-200">
              <CheckCircle2 className="h-8 w-8 text-slate-900 mx-auto mb-3" />
              <p className="font-medium text-slate-900">Driver Audio & Translation</p>
            </div>
            <div className="text-center p-6 bg-white rounded-lg border border-slate-200">
              <CheckCircle2 className="h-8 w-8 text-slate-900 mx-auto mb-3" />
              <p className="font-medium text-slate-900">Document Audit</p>
            </div>
            <div className="text-center p-6 bg-white rounded-lg border border-slate-200">
              <CheckCircle2 className="h-8 w-8 text-slate-900 mx-auto mb-3" />
              <p className="font-medium text-slate-900">Certified Timestamp Log</p>
            </div>
          </div>
          <div className="text-center">
            <Link to="/how-it-works">
              <Button variant="outline" className="border-slate-300">
                See how dispute packets work
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Pricing Section (NEW) */}
      <section id="pricing" className="py-24 bg-white">
        <div className="container mx-auto px-6 max-w-4xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-slate-900 mb-6">
              We succeed when you save money.
            </h2>
            <p className="text-xl text-slate-600 max-w-2xl mx-auto">
              Monthly base covers the platform. We take a small percentage only on demurrage/detention charges we help you avoid or recover. 
              <span className="font-semibold text-slate-900 block mt-2">If we don't save you money, we don't earn.</span>
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Pilot */}
            <Card className="border-slate-200 bg-slate-50">
              <CardHeader>
                <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center mb-4 border border-slate-200 text-slate-900">
                  <Clock className="h-6 w-6" />
                </div>
                <CardTitle className="text-2xl font-bold text-slate-900">30-Day Pilot</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg text-slate-700 font-medium mb-2">Free.</p>
                <p className="text-slate-600">We prove savings in the first month or you walk away. No questions asked.</p>
              </CardContent>
            </Card>

            {/* Paid */}
            <Card className="border-slate-900 bg-slate-900 text-white shadow-xl">
              <CardHeader>
                <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center mb-4 text-white">
                  <Handshake className="h-6 w-6" />
                </div>
                <CardTitle className="text-2xl font-bold">Standard</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg text-slate-200 font-medium mb-2">Base fee + Success share</p>
                <p className="text-slate-400">Low monthly platform fee. Performance fee charged only on recovered claims.</p>
              </CardContent>
            </Card>
          </div>

          <div className="mt-12 text-center">
            <Link to="/register">
              <Button size="lg" className="h-16 px-12 rounded-md text-xl bg-blue-600 hover:bg-blue-700 shadow-lg transition-transform hover:scale-105">
                Book pilot discussion
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-slate-900 text-slate-400 text-sm">
        <div className="container mx-auto px-6 text-center md:text-left">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <span className="font-bold text-slate-100 text-lg">Ward</span>
              <p className="mt-1">Operational Evidence Platform</p>
            </div>
            <div className="flex gap-8">
              <Link to="/contact" className="hover:text-white transition-colors">Contact</Link>
              <Link to="/why-ward" className="hover:text-white transition-colors">Why Ward</Link>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-slate-800">
            &copy; 2025 Ward AI Inc.
          </div>
        </div>
      </footer>
    </div>
  );
}

function StepCard({ number, icon: Icon, title, description }) {
  return (
    <div className="bg-white p-8 rounded-lg border border-slate-200 shadow-sm relative z-10 text-center">
      <div className="w-10 h-10 bg-slate-900 text-white rounded-full flex items-center justify-center font-bold mb-6 mx-auto">
        {number}
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
      <p className="text-slate-600 leading-relaxed">
        {description}
      </p>
    </div>
  );
}
