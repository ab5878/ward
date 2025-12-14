import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Mic, 
  Zap, 
  Code, 
  Workflow, 
  ArrowRight, 
  CheckCircle2, 
  Globe,
  Shield,
  Activity
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export default function Landing() {
  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans selection:bg-blue-100">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="container mx-auto px-6 h-16 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold">W</div>
            <span className="text-xl font-bold tracking-tight">Ward</span>
          </div>
          <div className="hidden md:flex gap-8 text-sm font-medium text-slate-600">
            <a href="#features" className="hover:text-blue-600 transition-colors">Platform</a>
            <a href="#solutions" className="hover:text-blue-600 transition-colors">Solutions</a>
            <a href="#developers" className="hover:text-blue-600 transition-colors">Developers</a>
            <a href="#pricing" className="hover:text-blue-600 transition-colors">Pricing</a>
          </div>
          <div className="flex gap-4">
            <Link to="/login">
              <Button variant="ghost" className="text-slate-600 hover:text-blue-600">Log in</Button>
            </Link>
            <Link to="/register">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white rounded-full px-6">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-24 pb-20 md:pt-32 md:pb-28 overflow-hidden relative">
        <div className="container mx-auto px-6 relative z-10 text-center">
          <Badge variant="secondary" className="mb-6 bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors px-4 py-1.5 rounded-full text-sm font-medium border border-blue-100">
            🚀 New: Enterprise Master Data & Financial Risk Analysis
          </Badge>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 mb-8 max-w-4xl mx-auto leading-tight">
            The AI Disruption Layer for <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Modern Logistics</span>
          </h1>
          
          <p className="text-xl text-slate-500 mb-10 max-w-2xl mx-auto leading-relaxed">
            Plug Ward into your TMS/ERP to automate disruption management. 
            From voice-based reporting to AI-coordinated resolution, in minutes.
          </p>
          
          <div className="flex flex-col md:flex-row gap-4 justify-center items-center mb-16">
            <Link to="/cases/voice">
              <Button size="lg" className="h-14 px-8 rounded-full text-lg bg-blue-600 hover:bg-blue-700 shadow-xl hover:shadow-2xl transition-all hover:-translate-y-1">
                Try Voice Demo <Mic className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link to="/dashboard">
              <Button size="lg" variant="outline" className="h-14 px-8 rounded-full text-lg border-slate-300 text-slate-700 hover:bg-slate-50">
                View Dashboard <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>

          {/* "Code" Snippet / Visual Proof */}
          <div className="relative max-w-4xl mx-auto rounded-xl shadow-2xl border border-slate-200 bg-slate-900 overflow-hidden text-left transform rotate-1 hover:rotate-0 transition-transform duration-500">
            <div className="flex items-center gap-2 px-4 py-3 bg-slate-800 border-b border-slate-700">
              <div className="w-3 h-3 rounded-full bg-red-500"/>
              <div className="w-3 h-3 rounded-full bg-yellow-500"/>
              <div className="w-3 h-3 rounded-full bg-green-500"/>
              <span className="ml-2 text-xs text-slate-400 font-mono">ward-integration.js</span>
            </div>
            <div className="p-6 overflow-x-auto">
              <pre className="font-mono text-sm text-blue-300">
                <span className="text-purple-400">const</span> ward = <span className="text-yellow-300">require</span>(<span className="text-green-300">'@ward-ai/sdk'</span>);{'\n\n'}
                <span className="text-slate-400">// 1. Listen for disruptions</span>{'\n'}
                ward.<span className="text-blue-400">on</span>(<span className="text-green-300">'disruption.detected'</span>, <span className="text-purple-400">async</span> (event) ={'>'} {'{'}{'\n'}
                {'  '}<span className="text-purple-400">const</span> rca = <span className="text-purple-400">await</span> ward.<span className="text-blue-400">analyze</span>(event);{'\n'}
                {'  '}<span className="text-purple-400">await</span> ward.<span className="text-blue-400">coordinate</span>(rca.action_plan);{'\n'}
                {'  '}console.<span className="text-yellow-300">log</span>(<span className="text-green-300">`Resolved in ${'{'}rca.resolution_time{'}'}`</span>);{'\n'}
                {'  '}
                {'}'});
              </pre>
            </div>
          </div>
        </div>
        
        {/* Background Elements */}
        <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
          <div className="absolute -top-40 -right-40 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-50"></div>
          <div className="absolute top-40 -left-40 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50"></div>
        </div>
      </section>

      {/* Social Proof (REMOVED as per user request) */}

      {/* Value Props */}
      <section id="features" className="py-24 bg-slate-50/50">
        <div className="container mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Everything you need to handle chaos
            </h2>
            <p className="text-lg text-slate-500">
              Ward isn't just a dashboard. It's an intelligent layer that sits between your ERP and the chaotic real world.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard 
              icon={Mic}
              title="Voice-First Ingestion"
              description="Drivers and field ops speak naturally in 10+ Indian languages. Ward transcribes, translates, and structures the data instantly."
            />
            <FeatureCard 
              icon={Workflow}
              title="Active Coordination"
              description="Ward doesn't just watch. It acts. Autonomous agents reach out to CHAs, ports, and transporters to unblock shipments."
            />
            <FeatureCard 
              icon={Shield}
              title="Financial Risk AI"
              description="Real-time calculation of detention, demurrage, and production loss risks. Prioritize what costs you money."
            />
            <FeatureCard 
              icon={Code}
              title="Developer API"
              description="Full REST API and Webhook support. Build custom workflows or integrate deeply into your SAP/Oracle OTM."
            />
            <FeatureCard 
              icon={Activity}
              title="Institutional Memory"
              description="Ward remembers every resolution. When problems recur, it suggests the fix that worked last time."
            />
            <FeatureCard 
              icon={Zap}
              title="Document Intelligence"
              description="Drag & drop invoices and BLs. Ward's Vision AI detects discrepancies automatically."
            />
          </div>
        </div>
      </section>

      {/* Integration Section */}
      <section className="py-24 bg-slate-900 text-white overflow-hidden relative">
        <div className="container mx-auto px-6 relative z-10">
          <div className="flex flex-col md:flex-row items-center gap-16">
            <div className="flex-1">
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Plug & Play with your existing stack
              </h2>
              <p className="text-lg text-slate-300 mb-8 leading-relaxed">
                You don't need to rip and replace. Ward works alongside your TMS. 
                Use our Webhooks to push "Resolved" statuses back to SAP, or pull shipment details via API.
              </p>
              <ul className="space-y-4 mb-8">
                {['Bi-directional sync with OTM/SAP', 'Webhooks for real-time alerts', 'Embeddable UI widgets'].map(item => (
                  <li key={item} className="flex items-center gap-3">
                    <CheckCircle2 className="h-5 w-5 text-green-400" />
                    <span className="text-slate-200">{item}</span>
                  </li>
                ))}
              </ul>
              <Button variant="outline" className="text-white border-slate-600 hover:bg-slate-800">
                Read API Documentation
              </Button>
            </div>
            <div className="flex-1 w-full">
              <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 shadow-2xl">
                <div className="flex items-center justify-between mb-6">
                  <span className="font-mono text-sm text-slate-400">Webhook Configuration</span>
                  <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                    <span className="text-xs text-green-400">Live</span>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-xs uppercase text-slate-500 font-bold">Callback URL</label>
                    <div className="bg-slate-900 p-3 rounded border border-slate-700 font-mono text-sm text-blue-300">
                      https://api.your-company.com/webhooks/ward
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="text-xs uppercase text-slate-500 font-bold">Events</label>
                    <div className="flex gap-2">
                      <Badge className="bg-blue-900 text-blue-200 hover:bg-blue-800">case.created</Badge>
                      <Badge className="bg-blue-900 text-blue-200 hover:bg-blue-800">rca.completed</Badge>
                      <Badge className="bg-blue-900 text-blue-200 hover:bg-blue-800">status.changed</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24">
        <div className="container mx-auto px-6 text-center max-w-3xl">
          <h2 className="text-4xl font-bold text-slate-900 mb-6">
            Ready to take control?
          </h2>
          <p className="text-xl text-slate-500 mb-10">
            Join 500+ logistics managers who use Ward to resolve disruptions 80% faster.
          </p>
          <Link to="/register">
            <Button size="lg" className="h-16 px-10 rounded-full text-xl bg-blue-600 hover:bg-blue-700 shadow-xl transition-transform hover:scale-105">
              Start Free Pilot
            </Button>
          </Link>
          <p className="mt-6 text-sm text-slate-400">
            No credit card required • SOC2 Compliant • Enterprise Ready
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 bg-white border-t border-slate-100">
        <div className="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center opacity-60 text-sm">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <div className="bg-slate-200 w-6 h-6 rounded flex items-center justify-center text-slate-600 font-bold text-xs">W</div>
            <span className="font-semibold text-slate-700">Ward v0</span>
          </div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-blue-600">Privacy</a>
            <a href="#" className="hover:text-blue-600">Terms</a>
            <a href="#" className="hover:text-blue-600">API Docs</a>
            <a href="#" className="hover:text-blue-600">Contact</a>
          </div>
          <div className="mt-4 md:mt-0">
            © 2025 Ward AI Inc.
          </div>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon: Icon, title, description }) {
  return (
    <div className="p-8 rounded-2xl bg-white border border-slate-100 hover:border-blue-100 hover:shadow-xl transition-all duration-300 group">
      <div className="w-12 h-12 bg-slate-50 rounded-xl shadow-sm border border-slate-100 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
        <Icon className="h-6 w-6 text-blue-600" />
      </div>
      <h3 className="text-xl font-bold text-slate-900 mb-3">{title}</h3>
      <p className="text-slate-500 leading-relaxed">
        {description}
      </p>
    </div>
  );
}
