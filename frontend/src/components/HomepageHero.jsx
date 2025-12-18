import React from 'react';
import { ArrowRight, CheckCircle2, Shield, Clock } from 'lucide-react';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';

export default function HomepageHero() {
  return (
    <section className="relative min-h-[90vh] flex items-center bg-gradient-to-b from-gray-50 to-white">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5" style={{
        backgroundImage: 'radial-gradient(circle, #000 1px, transparent 1px)',
        backgroundSize: '24px 24px'
      }}></div>
      
      <div className="container mx-auto px-6 py-20 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          {/* Hero Headline */}
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Stop paying for delays you didn't cause
          </h1>
          
          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-gray-600 mb-8 leading-relaxed max-w-3xl mx-auto">
            Turn chaotic driver calls and WhatsApps into <strong className="text-gray-900">audit-grade evidence</strong>.<br />
            Prove exactly what happened, stop the meter, and win the dispute.
          </p>

          {/* One Job Statement */}
          <div className="mb-12 p-6 bg-blue-50 border-l-4 border-blue-600 rounded-r-lg max-w-3xl mx-auto">
            <p className="text-lg font-semibold text-gray-900 mb-2">Ward's one job:</p>
            <p className="text-xl text-gray-700 italic">
              "Give you proof fast enough to stop the charges and strong enough to win the argument."
            </p>
          </div>
          
          {/* Value Props - Simplified */}
          <div className="grid md:grid-cols-3 gap-6 mb-12 text-left max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Shield className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Audit-grade evidence</h3>
                  <p className="text-sm text-gray-600">
                    Time-stamped, tamper-evident proof that holds up in disputes with ports, courts, and authorities.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Stop the meter</h3>
                  <p className="text-sm text-gray-600">
                    Generate dispute packets in minutes, not hours. Contest charges before they pile up.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <CheckCircle2 className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Win more disputes</h3>
                  <p className="text-sm text-gray-600">
                    Clear timelines and attribution. More waivers, fewer "we'll just pay it" decisions.
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          {/* CTAs */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link to="/contact">
              <Button 
                size="lg" 
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-6 text-lg font-semibold shadow-lg hover:shadow-xl transition-all"
              >
                Talk to founder
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            
            <Link to="/how-it-works">
              <Button 
                size="lg" 
                variant="outline" 
                className="border-2 border-gray-300 hover:border-gray-400 px-8 py-6 text-lg font-semibold bg-white"
              >
                See how Ward works
              </Button>
            </Link>
          </div>
          
          {/* Trust Indicator */}
          <p className="mt-8 text-sm text-gray-500">
            Built for importers, forwarders, and transporters at JNPT, Mundra, Chennai, and major logistics parks.
          </p>
        </div>
      </div>
    </section>
  );
}

