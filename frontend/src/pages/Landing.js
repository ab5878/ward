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
            <a href="#dispute-export" className="hover:text-slate-900 transition-colors">Dispute Export</a>
            <a href="#pricing" className="hover:text-slate-900 transition-colors">Pricing</a>
            <a href="#contact" className="hover:text-slate-900 transition-colors">Contact</a>
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
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-slate-900 mb-8 leading-tight">
            Ward prevents demurrage and detention losses by turning chaotic field conversations into audit-grade operational evidence.
          </h1>
          
          <div className="max-w-3xl mx-auto">
            <p className="text-lg md:text-xl text-slate-600 mb-10 leading-relaxed font-serif">
              When a shipment gets delayed, everyone scrambles on WhatsApp and calls. Later, finance asks: 
              <span className="italic font-medium text-slate-800"> ‘Who caused this and can we recover the money?’ </span> 
              And there’s no proof. Ward captures what drivers and agents say in their own language, timestamps it, structures it, and turns it into defensible evidence — so ops can fix issues faster and finance can stop or recover charges.
            </p>
            
            <div className="flex justify-center">
              <Link to="/register">
                <Button size="lg" className="h-14 px-8 rounded-md text-lg bg-slate-900 hover:bg-slate-800 shadow-md transition-all hover:translate-y-[-1px]">
                  Start a 30-day demurrage defense pilot
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* The One Job Section */}
      <section className="py-20 bg-slate-100 border-b border-slate-200">
        <div className="container mx-auto px-6 max-w-4xl text-center">
          <div className="inline-block p-3 bg-slate-200 rounded-full mb-6">
            <Scale className="h-8 w-8 text-slate-700" />
          </div>
          <h2 className="text-3xl font-bold text-slate-900 mb-6">The One Job Ward Does</h2>
          <p className="text-2xl md:text-3xl font-serif text-slate-700 leading-relaxed italic">
            "When something goes wrong in transit, give you proof fast enough to stop the meter and strong enough to win disputes."
          </p>
        </div>
      </section>

      {/* How It Works (Evidence Flow) */}
      <section id="how-it-works" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <Badge variant="outline" className="mb-4 text-slate-600 border-slate-300">Evidence Flow</Badge>
            <h2 className="text-3xl font-bold text-slate-900">
              From Chaos to Claim
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-12 relative">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-0.5 bg-slate-200 -z-10"></div>

            <StepCard 
              number="1"
              icon={Mic}
              title="Capture Ground Truth"
              description="Drivers speak in Hindi, Tamil, or Gujarati. Ward records, transcribes, and translates their exact testimony about WHY they are stuck (e.g. 'Gate closed', 'Official absent')."
            />
            <StepCard 
              number="2"
              icon={Clock}
              title="Establish Timeline"
              description="Every input is timestamped and geo-tagged. We map the delay against free time limits to calculate exact financial exposure in real-time."
            />
            <StepCard 
              number="3"
              icon={Gavel}
              title="Generate Defense"
              description="When the invoice arrives, you have a structured dossier proving the delay was not your fault (Force Majeure, Vendor Error)."
            />
          </div>
        </div>
      </section>

      {/* Dispute Export Section */}
      <section id="dispute-export" className="py-24 bg-slate-50 border-y border-slate-200">
        <div className="container mx-auto px-6 flex flex-col md:flex-row items-center gap-16">
          <div className="flex-1">
            <h2 className="text-3xl font-bold text-slate-900 mb-6">
              The "Dispute Export" Button
            </h2>
            <p className="text-lg text-slate-600 mb-8 leading-relaxed">
              Don't waste hours digging through emails. Click one button to generate a comprehensive <strong>Delay Statement PDF</strong> containing:
            </p>
            <ul className="space-y-4 mb-8">
              <li className="flex items-start gap-3">
                <CheckCircle2 className="h-6 w-6 text-slate-700 mt-0.5 flex-shrink-0" />
                <div>
                  <span className="font-bold text-slate-900">Driver Testimony:</span> Original audio + certified translation.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="h-6 w-6 text-slate-700 mt-0.5 flex-shrink-0" />
                <div>
                  <span className="font-bold text-slate-900">Document Audit:</span> Side-by-side comparison of Invoice vs BL mismatches.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <CheckCircle2 className="h-6 w-6 text-slate-700 mt-0.5 flex-shrink-0" />
                <div>
                  <span className="font-bold text-slate-900">Timeline of Negligence:</span> Detailed log showing exactly when you notified the other party.
                </div>
              </li>
            </ul>
            <Button variant="outline" className="border-slate-400 text-slate-700 hover:bg-slate-100 hover:text-slate-900">
              <Download className="mr-2 h-4 w-4" /> Download Sample Dispute PDF
            </Button>
          </div>
          <div className="flex-1 w-full bg-white p-8 rounded-lg shadow-sm border border-slate-200">
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-4">
                <div className="flex items-center gap-3">
                  <FileText className="h-8 w-8 text-red-700" />
                  <div>
                    <h3 className="font-bold text-slate-900">Detention Dispute Claim.pdf</h3>
                    <p className="text-xs text-slate-500">Generated: Dec 12, 2025</p>
                  </div>
                </div>
                <Badge variant="outline" className="text-red-700 border-red-200 bg-red-50">High Value</Badge>
              </div>
              <div className="space-y-3">
                <div className="h-2 bg-slate-100 rounded w-3/4"></div>
                <div className="h-2 bg-slate-100 rounded w-full"></div>
                <div className="h-2 bg-slate-100 rounded w-5/6"></div>
                <div className="h-32 bg-slate-50 rounded border border-slate-100 p-4 font-mono text-xs text-slate-500 leading-relaxed">
                  [10:30 AM] Driver Reported: "Gate entry denied." <br/>
                  [10:35 AM] Alert Sent to Terminal Ops. <br/>
                  [14:00 AM] Follow-up sent. No response. <br/>
                  ...
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-24 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">
              Invest in Defense
            </h2>
            <p className="text-lg text-slate-600">
              Pricing based on the value of evidence secured.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <PricingCard 
              title="Standard Defense"
              price="$499"
              period="/mo"
              description="For regional teams fighting local disputes."
              features={[
                "Up to 50 active cases/mo",
                "Voice-to-Evidence transcription",
                "PDF Dispute Exports",
                "30-day evidence retention"
              ]}
              buttonText="Start Pilot"
              highlighted={false}
            />
            <PricingCard 
              title="Enterprise Audit"
              price="Custom"
              period=""
              description="For global shippers requiring full audit compliance."
              features={[
                "Unlimited cases",
                "ERP/TMS Integration",
                "Dedicated Claims Specialist",
                "7-year evidence retention (Tax/Legal)"
              ]}
              buttonText="Contact Sales"
              highlighted={true}
            />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-slate-900 text-slate-400 text-sm">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <span className="font-bold text-slate-100 text-lg">Ward</span>
              <p className="mt-1">Operational Evidence Platform</p>
            </div>
            <div className="flex gap-8">
              <a href="#contact" className="hover:text-white transition-colors">Contact</a>
              <a href="#" className="hover:text-white transition-colors">Legal</a>
              <a href="#" className="hover:text-white transition-colors">Privacy</a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-slate-800 text-center md:text-left">
            &copy; 2025 Ward AI Inc. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}

function StepCard({ number, icon: Icon, title, description }) {
  return (
    <div className="bg-white p-8 rounded-lg border border-slate-200 shadow-sm relative z-10">
      <div className="w-12 h-12 bg-slate-900 text-white rounded-full flex items-center justify-center font-bold text-xl mb-6 mx-auto md:mx-0">
        {number}
      </div>
      <div className="mb-4 flex justify-center md:justify-start">
        <Icon className="h-8 w-8 text-slate-700" />
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3 text-center md:text-left">{title}</h3>
      <p className="text-slate-600 leading-relaxed text-center md:text-left">
        {description}
      </p>
    </div>
  );
}

function PricingCard({ title, price, period, description, features, buttonText, highlighted }) {
  return (
    <Card className={`flex flex-col ${highlighted ? 'border-slate-900 shadow-lg' : 'border-slate-200'}`}>
      <CardHeader className="text-center pb-2 bg-slate-50 border-b border-slate-100">
        <CardTitle className="text-xl font-bold text-slate-900">{title}</CardTitle>
        <p className="text-sm text-slate-500 mt-2">{description}</p>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col pt-8">
        <div className="text-center mb-8">
          <span className="text-4xl font-extrabold text-slate-900">{price}</span>
          {period && <span className="text-slate-500">{period}</span>}
        </div>
        <ul className="space-y-4 mb-8 flex-1 px-4">
          {features.map((feature, i) => (
            <li key={i} className="flex items-start gap-3 text-sm text-slate-700">
              <ShieldCheck className="h-5 w-5 text-slate-900 flex-shrink-0" />
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
