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
  CheckCircle2
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

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
            <a href="#home" className="hover:text-slate-900 transition-colors">Home</a>
            <a href="#how-it-works" className="hover:text-slate-900 transition-colors">How It Works</a>
            <a href="#pricing" className="hover:text-slate-900 transition-colors">Pricing</a>
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

      {/* Hero Section */}
      <section id="home" className="pt-24 pb-20 md:pt-32 md:pb-28 bg-white border-b border-slate-200">
        <div className="container mx-auto px-6 max-w-5xl text-center">
          <Badge variant="outline" className="mb-6 border-slate-300 text-slate-600 font-medium px-3 py-1 rounded-full uppercase tracking-wide text-xs">
            Operational Evidence Platform
          </Badge>
          
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight text-slate-900 mb-6 leading-tight">
            Stop paying for delays <br/> you didn't cause.
          </h1>
          
          <div className="max-w-2xl mx-auto">
            <p className="text-xl text-slate-600 mb-10 leading-relaxed font-light">
              Ward turns chaotic driver calls and WhatsApps into <strong>audit-grade evidence</strong>. 
              Prove exactly what happened, stop the meter, and win the dispute.
            </p>
            
            <div className="flex justify-center gap-4">
              <Link to="/register">
                <Button size="lg" className="h-14 px-8 rounded-md text-lg bg-slate-900 hover:bg-slate-800 shadow-xl transition-all hover:translate-y-[-2px]">
                  Start Defense Pilot
                </Button>
              </Link>
              <a href="#how-it-works">
                <Button size="lg" variant="outline" className="h-14 px-8 rounded-md text-lg border-slate-300 hover:bg-slate-50 text-slate-700">
                  How it works
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* The One Job Section */}
      <section className="py-20 bg-slate-100 border-b border-slate-200">
        <div className="container mx-auto px-6 max-w-4xl text-center">
          <h2 className="text-3xl font-bold text-slate-900 mb-6">The One Job Ward Does</h2>
          <p className="text-2xl md:text-3xl font-serif text-slate-700 leading-relaxed italic">
            "Give you proof fast enough to stop the charges and strong enough to win the argument."
          </p>
        </div>
      </section>

      {/* How It Works (Evidence Flow) */}
      <section id="how-it-works" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-3 gap-12 relative">
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
              description="Generate a PDF dossier instantly to prove the delay wasn't your fault."
            />
          </div>
        </div>
      </section>

      {/* Dispute Export Section */}
      <section id="dispute-export" className="py-24 bg-slate-50 border-y border-slate-200">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center gap-16">
          <div className="flex-1">
            <h2 className="text-3xl font-bold text-slate-900 mb-6">
              Click to Dispute.
            </h2>
            <p className="text-lg text-slate-600 mb-8 leading-relaxed">
              Don't dig through emails. Generate a <strong>Delay Statement</strong> instantly.
            </p>
            <ul className="space-y-4 mb-8">
              <li className="flex items-center gap-3 font-medium text-slate-800">
                <CheckCircle2 className="h-5 w-5 text-slate-900" />
                Original Driver Audio & Translation
              </li>
              <li className="flex items-center gap-3 font-medium text-slate-800">
                <CheckCircle2 className="h-5 w-5 text-slate-900" />
                Document Mismatch Audit
              </li>
              <li className="flex items-center gap-3 font-medium text-slate-800">
                <CheckCircle2 className="h-5 w-5 text-slate-900" />
                Certified Timestamp Log
              </li>
            </ul>
          </div>
          <div className="flex-1 w-full bg-white p-8 rounded-lg shadow-sm border border-slate-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-4">
              <div className="flex items-center gap-3">
                <FileText className="h-10 w-10 text-red-700" />
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">Dispute_Claim_#123.pdf</h3>
                  <p className="text-xs text-slate-500">Ready to send</p>
                </div>
              </div>
              <Button size="sm" variant="outline">Download</Button>
            </div>
            <div className="space-y-2 opacity-50">
              <div className="h-2 bg-slate-200 rounded w-full"></div>
              <div className="h-2 bg-slate-200 rounded w-5/6"></div>
              <div className="h-2 bg-slate-200 rounded w-4/6"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">
              Pricing based on protection.
            </h2>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <PricingCard 
              title="Standard Defense"
              price="$499"
              period="/mo"
              description="For regional teams fighting local disputes."
              features={[
                "50 Active Cases",
                "Voice-to-Evidence",
                "PDF Dispute Exports",
                "30-day retention"
              ]}
              buttonText="Start Pilot"
              highlighted={false}
            />
            <PricingCard 
              title="Enterprise Audit"
              price="Custom"
              period=""
              description="For global shippers requiring full compliance."
              features={[
                "Unlimited Cases",
                "ERP Integration",
                "Claims Specialist",
                "7-year retention"
              ]}
              buttonText="Contact Sales"
              highlighted={true}
            />
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
              <a href="#" className="hover:text-white transition-colors">Contact</a>
              <a href="#" className="hover:text-white transition-colors">Legal</a>
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

function PricingCard({ title, price, period, description, features, buttonText, highlighted }) {
  return (
    <Card className={`flex flex-col ${highlighted ? 'border-slate-900 shadow-xl' : 'border-slate-200'}`}>
      <CardHeader className="text-center pb-2 bg-slate-50 border-b border-slate-100">
        <CardTitle className="text-xl font-bold text-slate-900">{title}</CardTitle>
        <p className="text-sm text-slate-500 mt-2">{description}</p>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col pt-8">
        <div className="text-center mb-8">
          <span className="text-4xl font-extrabold text-slate-900">{price}</span>
          {period && <span className="text-slate-500">{period}</span>}
        </div>
        <ul className="space-y-4 mb-8 flex-1 px-8">
          {features.map((feature, i) => (
            <li key={i} className="flex items-center gap-3 text-sm text-slate-700">
              <ShieldCheck className="h-4 w-4 text-slate-900 flex-shrink-0" />
              {feature}
            </li>
          ))}
        </ul>
        <Link to="/register" className="w-full mt-auto">
          <Button className={`w-full h-12 text-lg ${highlighted ? 'bg-slate-900 hover:bg-slate-800' : 'bg-white text-slate-900 border border-slate-300 hover:bg-slate-50'}`}>
            {buttonText}
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
}
