import React from 'react';
import { Zap, Smartphone, Shield, Clock, WifiOff, CheckCircle2, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';

export default function ProductV0Section() {
  return (
    <section className="py-24 bg-white">
      <div className="container mx-auto px-6 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Product v0 — Capture the moment of friction
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Deliberately narrow and brutal: imports, ports/ICDs/CFS/logistics parks, demurrage/detention + waiting.
            Built for drivers, yard staff, and warehouse gate teams who need to log incidents faster than WhatsApp.
          </p>
        </div>

        {/* Three Subcards */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          {/* Card 1: One-tap logging */}
          <Card className="border-2 border-gray-200 hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-7 h-7 text-blue-600" />
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                One-tap logging
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                When something goes wrong—stuck at port gate, CFS yard full, dock not ready, documents issue—drivers and yard staff log it in one tap. Tap → speak → done. No typing, no forms, no training.
              </p>
              
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <Clock className="w-4 h-4 text-blue-600" />
                  <span className="font-medium">Target: ≤ 5 seconds</span>
                </div>
                <p className="text-xs text-gray-600">
                  Faster than sending a WhatsApp voice note. If it takes longer, drivers won't use it.
                </p>
              </div>

              <div className="pt-2 border-t border-gray-200">
                <p className="text-sm font-semibold text-gray-900 mb-2">Auto-attaches:</p>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    GPS location
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    Device ID
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    Timestamp
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-green-600" />
                    Container/truck/warehouse context
                  </li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Card 2: Offline-first & low-end Android */}
          <Card className="border-2 border-gray-200 hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Smartphone className="w-7 h-7 text-blue-600" />
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                Offline-first & low-end Android
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                Built for the real world: low-end Android devices, bad network at port gates and warehouse yards, drivers who need it to work right now, not after a loading spinner.
              </p>
              
              <div className="bg-gray-50 p-4 rounded-lg space-y-3">
                <div className="flex items-start gap-2">
                  <WifiOff className="w-5 h-5 text-orange-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Offline-first capture</p>
                    <p className="text-xs text-gray-600 mt-1">
                      Log incidents even when network is down. Syncs automatically when connectivity improves.
                    </p>
                  </div>
                </div>
                
                <div className="flex items-start gap-2">
                  <Smartphone className="w-5 h-5 text-blue-600 mt-0.5" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">Low-end device optimized</p>
                    <p className="text-xs text-gray-600 mt-1">
                      Works smoothly on common Android devices used by drivers and yard staff. No lag, no crashes.
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-gray-200">
                <p className="text-sm text-gray-600">
                  <strong className="text-gray-900">No loading spinners</strong> when someone is angry and on the phone. Aggressive local caching and background sync handle poor connectivity.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Card 3: Always tamper-evident */}
          <Card className="border-2 border-gray-200 hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-7 h-7 text-blue-600" />
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                Always tamper-evident
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                Every event is time-stamped by the system at capture, bound to device ID and GPS. Any edit or deletion is stored as a new event with full history. Originals are never destroyed.
              </p>
              
              <div className="bg-gray-50 p-4 rounded-lg space-y-2">
                <p className="text-sm font-semibold text-gray-900">Temporal truth over narrative truth</p>
                <p className="text-xs text-gray-600">
                  Finance and ops teams can see "captured at" vs "edited at" at a glance. If you can't instantly see which events were reconstructed later, Ward hasn't earned its job.
                </p>
              </div>

              <div className="pt-2 border-t border-gray-200 space-y-2">
                <p className="text-sm font-semibold text-gray-900">Exportable dispute packets</p>
                <p className="text-sm text-gray-600">
                  Generate chronological timelines with timestamps, GPS, and attachments. Formatted for Indian D&D/detention dispute templates. Ready to submit to port authorities and courts.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-12 p-8 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-lg text-gray-700 mb-4">
            <strong className="text-gray-900">The rule:</strong> The first tap must be faster than a WhatsApp voice note. Everything else (structure, tagging, linkage) is invisible.
          </p>
          <p className="text-sm text-gray-600 mb-6">
            Habit is not assumed; it is earned by being less annoying and more protective than the WhatsApp groups people already use.
          </p>
          <Link to="/how-it-works">
            <Button size="lg" variant="outline" className="border-gray-300">
              See the full evidence flow <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}

