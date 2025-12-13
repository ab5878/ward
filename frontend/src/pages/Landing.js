import React from 'react';
import { Link } from 'react-router-dom';
import { Mic, Brain, Clock, CheckCircle, ArrowRight } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Ward v0</h1>
            <p className="text-xs text-muted-foreground">Disruption Intelligence for Indian Logistics</p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/login"
              className="px-4 py-2 text-sm border border-border rounded-md hover:bg-secondary transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="px-4 py-2 text-sm bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-block px-4 py-1.5 mb-6 text-xs font-semibold bg-primary/10 text-primary rounded-full">
            🇮🇳 11 Indian Languages • Voice-First • AI-Powered RCA
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            When containers get stuck,<br />
            <span className="text-primary">speak in your language.</span>
          </h2>
          
          <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto">
            Driver reports in Gujarati. Ward asks in Gujarati. Manager gets root cause + action plan. 
            <strong className="text-foreground"> 4 hours vs 24 hours.</strong>
          </p>
          
          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              to="/register"
              className="px-8 py-4 text-base font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2 shadow-lg"
            >
              Start 30-Day Pilot <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/login"
              className="px-8 py-4 text-base font-medium border-2 border-border rounded-lg hover:bg-secondary transition-colors"
            >
              See Demo
            </Link>
          </div>

          {/* Quick Stats */}
          <div className="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
            <div>
              <div className="text-3xl font-bold text-primary">4h</div>
              <div className="text-sm text-muted-foreground">Avg Resolution</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">11</div>
              <div className="text-sm text-muted-foreground">Indian Languages</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">84%</div>
              <div className="text-sm text-muted-foreground">Adoption Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem */}
      <section className="bg-muted/30 py-16">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold mb-8 text-center">
              Today: Chaos in 5 WhatsApp groups
            </h3>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-card border border-border rounded-lg p-6">
                <h4 className="font-semibold mb-4 text-destructive flex items-center gap-2">
                  <span className="text-2xl">❌</span> Without Ward
                </h4>
                <ul className="space-y-3 text-sm text-muted-foreground">
                  <li>• Driver calls manager: "Boss, problem hai"</li>
                  <li>• Manager creates WhatsApp group</li>
                  <li>• Context scattered across 10 calls</li>
                  <li>• New shift manager has zero context</li>
                  <li>• Can't analyze: "How often does this happen?"</li>
                  <li>• <strong className="text-foreground">Avg resolution: 24 hours</strong></li>
                </ul>
              </div>

              <div className="bg-card border-2 border-primary/20 rounded-lg p-6">
                <h4 className="font-semibold mb-4 text-primary flex items-center gap-2">
                  <CheckCircle className="w-5 h-5" /> With Ward
                </h4>
                <ul className="space-y-3 text-sm text-muted-foreground">
                  <li>• Driver speaks in Gujarati (voice note)</li>
                  <li>• Ward asks clarity questions in Gujarati</li>
                  <li>• AI performs root cause analysis</li>
                  <li>• Manager gets action plan with owners</li>
                  <li>• Complete audit trail preserved</li>
                  <li>• <strong className="text-primary">Avg resolution: 4 hours</strong></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <div className="max-w-4xl mx-auto">
            <h3 className="text-3xl font-bold mb-12 text-center">
              From disruption to resolution in 3 steps
            </h3>
            
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center">
                  <Mic className="w-8 h-8 text-primary" />
                </div>
                <h4 className="font-semibold mb-2">1. Voice Report</h4>
                <p className="text-sm text-muted-foreground">
                  Speak in any Indian language. Ward transcribes and structures it.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center">
                  <Brain className="w-8 h-8 text-primary" />
                </div>
                <h4 className="font-semibold mb-2">2. AI Root Cause</h4>
                <p className="text-sm text-muted-foreground">
                  AI analyzes timeline, identifies root cause, recommends actions.
                </p>
              </div>

              <div className="text-center">
                <div className="w-16 h-16 mx-auto mb-4 bg-primary/10 rounded-full flex items-center justify-center">
                  <Clock className="w-8 h-8 text-primary" />
                </div>
                <h4 className="font-semibold mb-2">3. Track to Resolve</h4>
                <p className="text-sm text-muted-foreground">
                  6-state lifecycle with ownership. Full audit trail for compliance.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ROI Section */}
      <section className="bg-muted/30 py-16">
        <div className="container mx-auto px-6">
          <div className="max-w-3xl mx-auto text-center">
            <h3 className="text-3xl font-bold mb-6">
              Real ROI for logistics teams
            </h3>
            <p className="text-lg text-muted-foreground mb-8">
              50 disruptions/month × 17 hours saved × ₹4,000/hour
            </p>
            
            <div className="bg-card border-2 border-primary/20 rounded-lg p-8">
              <div className="text-5xl font-bold text-primary mb-2">₹34 Lakhs</div>
              <div className="text-muted-foreground mb-6">saved per year</div>
              <div className="text-sm text-muted-foreground">
                Ward cost: ₹8 Lakhs/year • <strong className="text-foreground">ROI: 4.25x</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <div className="max-w-2xl mx-auto text-center">
            <h3 className="text-4xl font-bold mb-6">
              Start your 30-day pilot
            </h3>
            <p className="text-lg text-muted-foreground mb-8">
              5 managers. 20 drivers. Full features. No cost.
            </p>
            <Link
              to="/register"
              className="inline-flex items-center gap-2 px-10 py-5 text-lg font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors shadow-xl"
            >
              Get Started Free <ArrowRight className="w-6 h-6" />
            </Link>
            <p className="mt-6 text-sm text-muted-foreground">
              Setup in 1 week. WhatsApp integration included.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card py-8">
        <div className="container mx-auto px-6">
          <div className="flex justify-between items-center">
            <div className="text-sm text-muted-foreground">
              © 2024 Ward v0. Built for Indian Logistics.
            </div>
            <div className="text-sm text-muted-foreground">
              Powered by Sarvam AI • Google Gemini
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
