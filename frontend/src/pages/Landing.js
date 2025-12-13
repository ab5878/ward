import React from 'react';
import { Link } from 'react-router-dom';
import { Mic, Phone, MessageSquare, CheckCircle, XCircle, ArrowRight, Shield, Clock, FileText } from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Ward v0</h1>
            <p className="text-xs text-[hsl(var(--muted-foreground))]">
              Decision Support for Logistics Operations
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              to="/login"
              className="px-4 py-2 text-sm border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="px-4 py-2 text-sm bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-16 md:py-24">
        <div className="max-w-3xl">
          <div className="inline-block px-3 py-1 mb-6 text-xs font-medium bg-[hsl(var(--primary))]/10 text-[hsl(var(--primary))] rounded-full">
            India-First • Voice-Enabled
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
            Handle disruptions by voice.<br />
            Decide with clarity.<br />
            Leave an audit trail.
          </h2>
          <p className="text-xl text-[hsl(var(--muted-foreground))] mb-8 leading-relaxed">
            Built for India's phone- and WhatsApp-driven logistics reality, Ward's voice mode lets ops teams handle live disruptions hands-free—without sacrificing structure, accountability, or auditability.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/register"
              className="inline-flex items-center gap-2 px-6 py-3 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors font-medium"
            >
              Try Voice-First Decision Support
              <ArrowRight className="h-4 w-4" />
            </Link>
            <a
              href="#how-it-works"
              className="inline-flex items-center gap-2 px-6 py-3 border border-[hsl(var(--border))] rounded-md hover:bg-[hsl(var(--secondary))] transition-colors"
            >
              See How It Works
            </a>
          </div>
        </div>
      </section>

      {/* What Ward Is (and Is Not) */}
      <section className="bg-[hsl(var(--muted))]/30 border-y border-[hsl(var(--border))]">
        <div className="container mx-auto px-6 py-12">
          <div className="max-w-3xl mx-auto">
            <p className="text-base text-[hsl(var(--muted-foreground))] text-center leading-relaxed mb-6">
              <span className="font-semibold text-foreground">Ward is not a voice assistant and not an autonomous agent.</span><br />
              Ward is the calm person on the call who asks the right questions, writes everything down, and makes sure the decision is remembered.<br />
              <span className="font-semibold text-foreground">Voice is a capture + guidance layer, not a command layer.</span>
            </p>
            <p className="text-sm text-center text-[hsl(var(--muted-foreground))]">
              <span className="font-semibold text-foreground">Ward coordinates humans under uncertainty.</span> It preserves who knew what, when, and why — without telling anyone what to do autonomously.
            </p>
          </div>
        </div>
      </section>

      {/* Voice-First for Indian Ops Teams */}
      <section className="container mx-auto px-6 py-16 md:py-20">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Voice-First for Indian Ops Teams</h2>
          
          {/* Why Voice */}
          <div className="mb-12">
            <h3 className="text-xl font-semibold mb-4">Why Voice?</h3>
            <p className="text-[hsl(var(--muted-foreground))] leading-relaxed mb-4">
              Indian logistics disruptions are discovered via calls, WhatsApp, brokers, and CHAs. Operators are often multitasking, under time pressure, working late-night or early-morning shifts. Typing structured inputs during a disruption is slow and error-prone.
            </p>
            <p className="text-foreground font-medium">
              Voice solves access and speed — Ward preserves discipline.
            </p>
          </div>

          {/* India Reality Icons */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6">
              <Phone className="h-8 w-8 text-[hsl(var(--primary))] mb-3" />
              <h4 className="font-semibold mb-2">Phone-First Reality</h4>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                CHA calls, driver updates, port gate notifications—all verbal, all urgent
              </p>
            </div>
            <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6">
              <MessageSquare className="h-8 w-8 text-[hsl(var(--primary))] mb-3" />
              <h4 className="font-semibold mb-2">WhatsApp Updates</h4>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                Transporters, brokers, and field agents communicate via voice messages
              </p>
            </div>
            <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-6">
              <Clock className="h-8 w-8 text-[hsl(var(--primary))] mb-3" />
              <h4 className="font-semibold mb-2">Time Pressure</h4>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                3 a.m. customs hold, monsoon blockage, truck breakdown—need decisions fast
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How Voice Works */}
      <section id="how-it-works" className="bg-card border-y border-[hsl(var(--border))]">
        <div className="container mx-auto px-6 py-16 md:py-20">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How Voice Works in Ward</h2>
            <p className="text-[hsl(var(--muted-foreground))] mb-12">
              Ward's voice mode follows a strict 5-step protocol. At every step, you remain in control.
            </p>

            <div className="space-y-8">
              {/* Step 1 */}
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center font-bold text-lg">
                    1
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">Speak the Disruption (Any Indian Language)</h3>
                  <p className="text-[hsl(var(--muted-foreground))] mb-3">
                    Operators describe what just happened—in Hindi, English, or regional languages.
                  </p>
                  <div className="bg-[hsl(var(--muted))]/30 border border-[hsl(var(--border))] rounded-lg p-4">
                    <p className="text-sm font-mono">
                      <Mic className="h-4 w-4 inline mr-2 text-[hsl(var(--primary))]" />
                      "Ward, container XYZ is stuck at Mundra. CHA says assessment pending, exact reason not clear yet."
                    </p>
                  </div>
                  <p className="text-xs text-[hsl(var(--muted-foreground))] mt-2">
                    Powered by Sarvam AI's multilingual speech-to-text, optimized for Indian accents, noise, and code-mixing.
                  </p>
                </div>
              </div>

              {/* Step 2 */}
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center font-bold text-lg">
                    2
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">Ward Clarifies — It Does Not Decide</h3>
                  <p className="text-[hsl(var(--muted-foreground))] mb-3">
                    Ward asks only clarity-enforcing questions:
                  </p>
                  <ul className="space-y-2 mb-3">
                    <li className="text-sm text-[hsl(var(--muted-foreground))]">
                      • "Is this confirmed by a port notice or only a CHA call?"
                    </li>
                    <li className="text-sm text-[hsl(var(--muted-foreground))]">
                      • "Is the impact limited to this shipment or others?"
                    </li>
                    <li className="text-sm text-[hsl(var(--muted-foreground))]">
                      • "What is known vs still unknown?"
                    </li>
                  </ul>
                  <p className="text-sm font-medium">
                    No predictions. No recommendations yet.
                  </p>
                </div>
              </div>

              {/* Step 3 */}
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center font-bold text-lg">
                    3
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">Disruption Is Locked (Human-Approved)</h3>
                  <p className="text-[hsl(var(--muted-foreground))] mb-3">
                    Ward converts the voice interaction into a structured disruption record:
                  </p>
                  <div className="grid grid-cols-2 gap-2 mb-3">
                    <div className="text-sm">
                      <span className="font-medium">Disruption type</span>
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Scope</span> (shipment / corridor)
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Identifier</span>
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Time discovered</span> (IST)
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Source</span> (call, WhatsApp, CHA)
                    </div>
                    <div className="text-sm">
                      <span className="font-medium">Explicit unknowns</span>
                    </div>
                  </div>
                  <p className="text-sm font-medium bg-[hsl(var(--warning))]/10 border border-[hsl(var(--warning))]/20 rounded p-3">
                    The operator reviews and approves this disruption before any decision is created.
                  </p>
                </div>
              </div>

              {/* Step 4 */}
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center font-bold text-lg">
                    4
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">Voice-Guided Decision Protocol</h3>
                  <p className="text-[hsl(var(--muted-foreground))] mb-3">
                    Ward then verbally guides the operator through its fixed decision protocol:
                  </p>
                  <ul className="space-y-2 mb-3">
                    <li className="text-sm">1. What decision must be made now?</li>
                    <li className="text-sm">2. Known inputs</li>
                    <li className="text-sm">3. Assumptions</li>
                    <li className="text-sm">4. Alternatives (including "wait / do nothing")</li>
                    <li className="text-sm">5. Worst-case outcomes</li>
                  </ul>
                  <p className="text-sm font-medium">
                    Ward reads back worst-cases and failure signals out loud to reduce panic-driven decisions.
                  </p>
                </div>
              </div>

              {/* Step 5 */}
              <div className="flex gap-6">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 rounded-full bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] flex items-center justify-center font-bold text-lg">
                    5
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">Written Decision + Audit Trail</h3>
                  <p className="text-[hsl(var(--muted-foreground))] mb-3">
                    The final output is always:
                  </p>
                  <ul className="space-y-2 mb-3">
                    <li className="text-sm flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-[hsl(var(--success))]" />
                      A written, reviewable decision
                    </li>
                    <li className="text-sm flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-[hsl(var(--success))]" />
                      Explicit alternatives
                    </li>
                    <li className="text-sm flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-[hsl(var(--success))]" />
                      Logged approval or override
                    </li>
                    <li className="text-sm flex items-center gap-2">
                      <CheckCircle className="h-4 w-4 text-[hsl(var(--success))]" />
                      Full transcript + provenance
                    </li>
                  </ul>
                  <p className="text-sm font-medium bg-[hsl(var(--info))]/10 border border-[hsl(var(--info))]/20 rounded p-3">
                    Voice improves speed. Text preserves accountability.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Sarvam AI */}
      <section className="container mx-auto px-6 py-16">
        <div className="max-w-3xl mx-auto">
          <div className="bg-card border border-[hsl(var(--border))] rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-4">Why Sarvam AI Powers Ward's Voice Mode</h2>
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-[hsl(var(--success))] mt-0.5 flex-shrink-0" />
                <p className="text-[hsl(var(--muted-foreground))]">
                  <span className="font-medium text-foreground">Multilingual support</span> across Indian languages
                </p>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-[hsl(var(--success))] mt-0.5 flex-shrink-0" />
                <p className="text-[hsl(var(--muted-foreground))]">
                  <span className="font-medium text-foreground">High accuracy</span> in noisy, real-world environments (ports, trucks, yards)
                </p>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-[hsl(var(--success))] mt-0.5 flex-shrink-0" />
                <p className="text-[hsl(var(--muted-foreground))]">
                  <span className="font-medium text-foreground">Handles interruptions</span>, accents, and code-mixing
                </p>
              </div>
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-[hsl(var(--success))] mt-0.5 flex-shrink-0" />
                <p className="text-[hsl(var(--muted-foreground))]">
                  <span className="font-medium text-foreground">Sovereign, India-first AI stack</span> aligned with local data realities
                </p>
              </div>
            </div>
            <div className="mt-6 pt-6 border-t border-[hsl(var(--border))]">
              <p className="text-sm font-medium text-center">
                Sarvam powers speech. Ward controls decisions.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* What Ward Voice Will NEVER Do */}
      <section className="bg-[hsl(var(--destructive))]/5 border-y border-[hsl(var(--destructive))]/20">
        <div className="container mx-auto px-6 py-16">
          <div className="max-w-3xl mx-auto">
            <h2 className="text-2xl md:text-3xl font-bold mb-6 text-center">What Ward Voice Will NEVER Do</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center gap-3 bg-card p-4 rounded-lg border border-[hsl(var(--border))]">
                <XCircle className="h-5 w-5 text-[hsl(var(--destructive))] flex-shrink-0" />
                <span className="text-sm font-medium">Auto-execute actions</span>
              </div>
              <div className="flex items-center gap-3 bg-card p-4 rounded-lg border border-[hsl(var(--border))]">
                <XCircle className="h-5 w-5 text-[hsl(var(--destructive))] flex-shrink-0" />
                <span className="text-sm font-medium">Predict ETAs or outcomes</span>
              </div>
              <div className="flex items-center gap-3 bg-card p-4 rounded-lg border border-[hsl(var(--border))]">
                <XCircle className="h-5 w-5 text-[hsl(var(--destructive))] flex-shrink-0" />
                <span className="text-sm font-medium">Optimize routes or costs</span>
              </div>
              <div className="flex items-center gap-3 bg-card p-4 rounded-lg border border-[hsl(var(--border))]">
                <XCircle className="h-5 w-5 text-[hsl(var(--destructive))] flex-shrink-0" />
                <span className="text-sm font-medium">Decide without human approval</span>
              </div>
              <div className="flex items-center gap-3 bg-card p-4 rounded-lg border border-[hsl(var(--border))] md:col-span-2">
                <XCircle className="h-5 w-5 text-[hsl(var(--destructive))] flex-shrink-0" />
                <span className="text-sm font-medium">Hide uncertainty</span>
              </div>
            </div>
            <p className="text-center mt-6 font-semibold text-lg">
              Ward's voice mode is assistive, not autonomous.
            </p>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="container mx-auto px-6 py-16 md:py-20">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Handle chaos without losing clarity
          </h2>
          <p className="text-xl text-[hsl(var(--muted-foreground))] mb-8">
            Try Ward's voice-first decision support built for Indian logistics operations.
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link
              to="/register"
              className="inline-flex items-center gap-2 px-8 py-4 bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] rounded-md hover:bg-[hsl(var(--primary))]/90 transition-colors font-medium text-lg"
            >
              See How Ward Handles Live Disruptions
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
          <p className="text-sm text-[hsl(var(--muted-foreground))] mt-6">
            Voice is an interface. Decisions are always human-owned.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[hsl(var(--border))] bg-card">
        <div className="container mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
              <p className="text-sm text-[hsl(var(--muted-foreground))]">
                © 2024 Ward v0. Built for India-first logistics operations.
              </p>
            </div>
            <div className="flex gap-6">
              <Link to="/login" className="text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors">
                Sign In
              </Link>
              <Link to="/register" className="text-sm text-[hsl(var(--muted-foreground))] hover:text-foreground transition-colors">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
