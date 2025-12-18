import React from 'react';
import { Mic, Clock, FileText, TrendingUp, ArrowRight, CheckCircle2 } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';

export default function FromChaosToPacketSection() {
  return (
    <section className="py-24 bg-gradient-to-b from-gray-50 to-white">
      <div className="container mx-auto px-6 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            From chaos to a dispute packet in 3 clicks
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Convert "we'll just pay it" invoices into structured disputes. Reconstruct timelines. Stop internal blame games.
          </p>
        </div>

        {/* 4-Step Visual Flow */}
        <div className="grid md:grid-cols-4 gap-6 mb-16">
          {/* Step 1: Capture */}
          <div className="relative">
            <Card className="h-full border-2 border-blue-200 bg-blue-50">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Mic className="w-8 h-8 text-white" />
                </div>
                <CardTitle className="text-xl font-bold text-gray-900">
                  1. Capture
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600 text-sm leading-relaxed">
                  Drivers and yard staff log incidents in one tap. Voice, GPS, timestamp, device ID—all captured automatically.
                </p>
              </CardContent>
            </Card>
            <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
              <ArrowRight className="w-6 h-6 text-blue-600" />
            </div>
          </div>

          {/* Step 2: Timeline */}
          <div className="relative">
            <Card className="h-full border-2 border-blue-200 bg-blue-50">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Clock className="w-8 h-8 text-white" />
                </div>
                <CardTitle className="text-xl font-bold text-gray-900">
                  2. Timeline
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600 text-sm leading-relaxed">
                  Finance uploads invoice. Ward finds the movement. Chronological timeline shows what actually happened, when, where.
                </p>
              </CardContent>
            </Card>
            <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
              <ArrowRight className="w-6 h-6 text-blue-600" />
            </div>
          </div>

          {/* Step 3: Packet */}
          <div className="relative">
            <Card className="h-full border-2 border-blue-200 bg-blue-50">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FileText className="w-8 h-8 text-white" />
                </div>
                <CardTitle className="text-xl font-bold text-gray-900">
                  3. Packet
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600 text-sm leading-relaxed">
                  Export dispute packet in one click. Formatted for JNPT, Mundra, Chennai. Includes timeline, GPS, attachments, timestamps.
                </p>
              </CardContent>
            </Card>
            <div className="hidden md:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
              <ArrowRight className="w-6 h-6 text-blue-600" />
            </div>
          </div>

          {/* Step 4: Outcome */}
          <div>
            <Card className="h-full border-2 border-green-200 bg-green-50">
              <CardHeader className="text-center">
                <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <CardTitle className="text-xl font-bold text-gray-900">
                  4. Outcome
                </CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-600 text-sm leading-relaxed">
                  More invoices contested. More waivers/discounts. Less time per dispute. Clear attribution stops blame games.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid md:grid-cols-3 gap-6">
          {/* Metric 1: % Invoices Contested */}
          <Card className="border-2 border-gray-200">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <CardTitle className="text-lg font-semibold text-gray-900">
                  % Invoices Contested
                </CardTitle>
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                47%
              </div>
              <p className="text-sm text-gray-600 mb-3">
                vs 12% historical baseline
              </p>
              <div className="flex items-center gap-2 text-sm text-green-600">
                <CheckCircle2 className="w-4 h-4" />
                <span className="font-medium">+35% uplift</span>
              </div>
              <p className="text-xs text-gray-500 mt-3">
                More invoices are now being contested instead of automatically paid.
              </p>
            </CardContent>
          </Card>

          {/* Metric 2: % Waivers/Discounts */}
          <Card className="border-2 border-gray-200">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <CardTitle className="text-lg font-semibold text-gray-900">
                  % Waivers/Discounts
                </CardTitle>
                <TrendingUp className="w-5 h-5 text-green-600" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                28%
              </div>
              <p className="text-sm text-gray-600 mb-3">
                vs 3% historical baseline
              </p>
              <div className="flex items-center gap-2 text-sm text-green-600">
                <CheckCircle2 className="w-4 h-4" />
                <span className="font-medium">+25% uplift</span>
              </div>
              <p className="text-xs text-gray-500 mt-3">
                Dispute packets with provable evidence lead to more waivers and discounts.
              </p>
            </CardContent>
          </Card>

          {/* Metric 3: Time Saved Per Dispute */}
          <Card className="border-2 border-gray-200">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <CardTitle className="text-lg font-semibold text-gray-900">
                  Time Saved Per Dispute
                </CardTitle>
                <Clock className="w-5 h-5 text-blue-600" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-gray-900 mb-2">
                4.2h
              </div>
              <p className="text-sm text-gray-600 mb-3">
                vs 6.5h historical average
              </p>
              <div className="flex items-center gap-2 text-sm text-green-600">
                <CheckCircle2 className="w-4 h-4" />
                <span className="font-medium">35% reduction</span>
              </div>
              <p className="text-xs text-gray-500 mt-3">
                Automated timeline reconstruction and packet generation saves ops/finance/legal time.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Bottom CTA */}
        <div className="mt-12 text-center">
          <p className="text-lg text-gray-700 mb-6">
            <strong className="text-gray-900">The monetizable wedge:</strong> Ward learns which combinations of ports, facilities, lanes, and actions correlate with paid vs waived charges. Over time, Ward becomes the default place to check "what happened" whenever a D&D, detention, or waiting invoice lands.
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-600 mb-6">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-green-600" />
              <span>Stop internal blame games</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-green-600" />
              <span>Clear delay attribution</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-green-600" />
              <span>Actionable monthly insights</span>
            </div>
          </div>
          <Link to="/register">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700 text-white">
              Start your Ward Pilot <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}

