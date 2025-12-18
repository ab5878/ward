import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Scale, AlertTriangle, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';

export default function WhyWard() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
        <div className="container mx-auto px-6 h-16 flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2">
            <div className="bg-blue-600 w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold">W</div>
            <span className="text-xl font-bold tracking-tight text-gray-900">Ward</span>
          </Link>
          <Link to="/">
            <Button variant="ghost">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Home
            </Button>
          </Link>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-16 max-w-4xl">
        {/* Header */}
        <div className="mb-16 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Why Ward
          </h1>
          <p className="text-xl text-gray-600">
            Philosophy and operating doctrine
          </p>
        </div>

        {/* Section 1: Owning truth under conflict */}
        <section className="mb-20">
          <div className="flex items-center gap-3 mb-6">
            <Shield className="w-8 h-8 text-blue-600" />
            <h2 className="text-3xl font-bold text-gray-900">
              Owning truth under conflict
            </h2>
          </div>

          <div className="prose prose-lg max-w-none space-y-6 text-gray-700 leading-relaxed">
            <p>
              When something goes wrong in Indian freight—a container stuck at port gate, CFS yard full, dock not ready—the first response is WhatsApp. It's fast, familiar, and requires zero training. Drivers and yard staff send voice notes. Dispatchers forward screenshots. Finance teams dig through chat histories when invoices arrive.
            </p>

            <p>
              But WhatsApp screenshots don't hold up in disputes. Port authorities, courts, and custodians need provable, time-stamped evidence. When money and blame are on the line, "I sent a WhatsApp" isn't enough.
            </p>

            <div className="bg-blue-50 border-l-4 border-blue-600 p-6 my-8">
              <p className="text-xl font-semibold text-gray-900 mb-2">
                Belief under dispute is the product.
              </p>
              <p className="text-gray-700">
                WhatsApp wins at speed. Ward must win at settlement. If we can't prove what happened when it matters, we've failed.
              </p>
            </div>

            <p>
              The real product isn't the logging interface or the dispute packet format. It's the credibility that makes port authorities, courts, and custodians believe what we've recorded.
            </p>

            <p>
              This is why Ward exists: to make evidence exist in a form that survives scrutiny. Not faster than WhatsApp—that's table stakes. More credible than WhatsApp—that's the job.
            </p>

            <p>
              Ward is the evidence layer for freight and warehouse-linked delays. It sits above TMS, WMS, PMS, and marketplace systems. They know what should have happened. Ward preserves what actually got logged when things went wrong.
            </p>
          </div>
        </section>

        {/* Section 2: Our doctrine */}
        <section className="mb-20">
          <div className="flex items-center gap-3 mb-6">
            <Scale className="w-8 h-8 text-blue-600" />
            <h2 className="text-3xl font-bold text-gray-900">
              Our doctrine
            </h2>
          </div>

          <div className="space-y-8">
            {/* Principle 1 */}
            <Card className="border-2 border-gray-200">
              <CardContent className="pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  1. Neutrality over convenience
                </h3>
                <p className="text-gray-700 leading-relaxed mb-3">
                  Ward never fabricates or silently deletes events. When logs contradict a customer's preferred narrative, we surface that contradiction. We don't "help" by hiding it. If Ward's logs show your driver was late, we show it. If they show the port gate was actually open, we show that too.
                </p>
                <p className="text-gray-600 italic">
                  The cost of being believed is occasionally making your own customer look wrong. We accept that cost.
                </p>
              </CardContent>
            </Card>

            {/* Principle 2 */}
            <Card className="border-2 border-gray-200">
              <CardContent className="pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  2. Subpoena-ready from day one
                </h3>
                <p className="text-gray-700 leading-relaxed mb-3">
                  Ward is designed assuming its logs will be discoverable and subpoenaable in disputes with ports, custodians, customs, and other agencies. They will be used in internal investigations between shippers, forwarders, transporters, and warehouse operators.
                </p>
                <p className="text-gray-600 italic">
                  Every design decision asks: "Would this withstand external scrutiny?" If the answer is no, we don't ship it.
                </p>
              </CardContent>
            </Card>

            {/* Principle 3 */}
            <Card className="border-2 border-gray-200">
              <CardContent className="pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  3. Customers own the data, Ward preserves it
                </h3>
                <p className="text-gray-700 leading-relaxed mb-3">
                  Customers (shippers, forwarders, 3PLs, warehouse operators) are data controllers. Ward is a processor. Drivers and vendors log into customer-managed accounts. The terms explicitly state that logs may be used in internal and external disputes.
                </p>
                <p className="text-gray-600 italic">
                  But customers cannot overwrite history. All edits are additive and traceable. You can add context, but you cannot delete what was logged.
                </p>
              </CardContent>
            </Card>

            {/* Principle 4 */}
            <Card className="border-2 border-gray-200">
              <CardContent className="pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  4. No silent edits, ever
                </h3>
                <p className="text-gray-700 leading-relaxed mb-3">
                  If a feature enables silent history changes that would not withstand external scrutiny, it does not ship—even if a large customer asks and even if ARR is on the line.
                </p>
                <p className="text-gray-700 leading-relaxed">
                  Every edit creates a new event. Every deletion is logged. The full tamper trail is always visible. "Captured at" vs "edited at" is shown prominently. If you can't instantly see which events were reconstructed later, Ward hasn't earned its job.
                </p>
              </CardContent>
            </Card>

            {/* Principle 5 */}
            <Card className="border-2 border-gray-200">
              <CardContent className="pt-6">
                <h3 className="text-xl font-bold text-gray-900 mb-3">
                  5. Temporal truth over narrative truth
                </h3>
                <p className="text-gray-700 leading-relaxed mb-3">
                  Ward does not decide who is "right." It preserves what was logged, when, where, and how strongly it is corroborated. We record temporal truth—what actually got captured in the moment—not the narrative that emerges later.
                </p>
                <p className="text-gray-600 italic">
                  This is the operating doctrine: credibility over convenience, truth over comfort, evidence over expedience.
                </p>
              </CardContent>
            </Card>
          </div>
        </section>

        {/* Section 3: The red line */}
        <section className="mb-20">
          <div className="flex items-center gap-3 mb-6">
            <AlertTriangle className="w-8 h-8 text-red-600" />
            <h2 className="text-3xl font-bold text-gray-900">
              The red line
            </h2>
          </div>

          <div className="prose prose-lg max-w-none space-y-6 text-gray-700 leading-relaxed">
            <blockquote className="border-l-4 border-red-600 bg-red-50 p-6 my-8 text-lg font-semibold text-gray-900 italic">
              "If we ever let customers quietly edit history to 'help' win a dispute, we become WhatsApp with a UI. We do not cross that line."
            </blockquote>

            <p>
              This is the red line. Not a feature request we'll consider. Not a "maybe for enterprise." Not a negotiation.
            </p>

            <p>
              If Ward allows silent edits, we've destroyed the only thing that makes us different from WhatsApp. We've become a nice logistics feature, not a system of record. We've traded credibility for convenience, and in doing so, we've lost the right to claim we're solving the problem we set out to solve.
            </p>

            <div className="bg-gray-50 border-2 border-gray-200 p-6 my-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                Why this is the moat
              </h3>
              <p className="text-gray-700 leading-relaxed mb-3">
                The moat isn't the UI. It isn't the LLMs. It isn't the integration with TMS or WMS systems. Those are features. Features can be copied.
              </p>
              <p className="text-gray-700 leading-relaxed mb-3">
                The moat is outcome-labeled, port/ICD/CFS/warehouse/facility-specific causality data embedded in a tamper-evident system, plus an operating doctrine that consistently chooses credibility over convenience—even when that means proving your own customer wrong in a specific case.
              </p>
              <p className="text-gray-700 leading-relaxed">
                That doctrine—not technology—is what makes this a real system-of-record attempt, not "a nice logistics or warehouse feature."
              </p>
            </div>

            <p>
              When a port authority or court subpoenas Ward's logs, they need to trust that what they're seeing is what actually happened, not what the customer wanted them to see. That trust is earned by consistently choosing the harder path: showing the truth, even when it's inconvenient.
            </p>

            <p className="text-lg font-semibold text-gray-900">
              If we cross the red line, we lose that trust. And without trust, we're just WhatsApp with a UI.
            </p>

            <p className="text-lg font-bold text-red-600">
              We do not cross that line.
            </p>
          </div>
        </section>

        {/* Footer CTA */}
        <div className="mt-16 pt-8 border-t border-gray-200 text-center">
          <p className="text-gray-600 mb-4">
            Questions about our doctrine? Want to understand how Ward works?
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/contact">
              <Button variant="outline">Talk to founder</Button>
            </Link>
            <Link to="/how-it-works">
              <Button>See how Ward works</Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

