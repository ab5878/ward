import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Shield, Clock, CheckCircle2, FileText, Mic, Gavel, Zap } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export default function HowItWorks() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
        <div className="container mx-auto px-6 h-16 flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2">
            <div className="bg-blue-600 w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold">W</div>
            <span className="text-xl font-bold tracking-tight text-gray-900">Ward</span>
          </Link>
          <Link to="/">
            <Button variant="ghost">Back to Home</Button>
          </Link>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-16 max-w-5xl">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            How Ward works
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Evidence layer for freight and warehouse delays. WhatsApp wins at speed; Ward wins at settlement.
          </p>
        </div>

        {/* Core Concept */}
        <Card className="mb-12 bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                The Core Insight
              </h2>
              <p className="text-lg text-gray-700 italic mb-2">
                "Belief under dispute is the product."
              </p>
              <p className="text-gray-600">
                Ward doesn't decide who's right. We preserve what was logged, when, where, and how strongly it's corroborated.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* How It Works Steps */}
        <div className="space-y-8 mb-16">
          <div className="grid md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <Mic className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle>1. Capture</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Drivers speak in their own language. Voice reports, WhatsApp messages, and manual entries are captured with timestamps and geo-tags.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <Clock className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle>2. Timeline</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Every event is timestamped against your free time limits. Port gates, ICDs, CFSs, and warehouse nodes are tracked automatically.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                  <Shield className="w-6 h-6 text-blue-600" />
                </div>
                <CardTitle>3. Evidence</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Tamper-evident logs that hold up when money and blame are on the line. Courts and custodians can't dismiss WhatsApp screenshots.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* What Makes Ward Different */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
            What makes Ward different
          </h2>
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Zap className="w-6 h-6 text-blue-600" />
                  <CardTitle>Sits above your stack</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Works with TMS, WMS, PMS, and marketplace platforms. They track what should happen; Ward preserves what actually happened.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <FileText className="w-6 h-6 text-blue-600" />
                  <CardTitle>One-click dispute packets</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Generate PDF dossiers instantly with original audio, translations, document audits, and certified timestamp logs.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <Gavel className="w-6 h-6 text-blue-600" />
                  <CardTitle>Built for Indian context</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Designed for JNPT, Mundra, Chennai, and major logistics parks. Understands Indian courts, port authorities, and custodian rights.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-6 h-6 text-blue-600" />
                  <CardTitle>Neutral evidence layer</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  We don't decide who's right. We preserve what was logged, when, where, and how strongly it's corroborated.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA */}
        <Card className="bg-blue-600 text-white border-0">
          <CardContent className="pt-6 text-center">
            <h2 className="text-2xl font-bold mb-4">
              Ready to stop losing money in disputes?
            </h2>
            <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
              If you're paying multi-lakh monthly demurrage/detention charges, let's talk about how Ward can help.
            </p>
            <div className="flex gap-4 justify-center">
              <Link to="/contact">
                <Button size="lg" className="bg-white text-blue-600 hover:bg-gray-100">
                  Talk to founder
                </Button>
              </Link>
              <Link to="/register">
                <Button size="lg" variant="outline" className="border-white text-white hover:bg-blue-700">
                  Start Pilot
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

