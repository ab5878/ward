import React from 'react';
import { Building2, Truck, Warehouse, AlertCircle, MessageSquare, Shield, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Link } from 'react-router-dom';

export default function WhoWardIsForSection() {
  return (
    <section className="py-24 bg-white">
      <div className="container mx-auto px-6 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Who Ward is for
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Anyone in the India freight + warehouse stack who currently loses money in arguments because "it's not written anywhere except in a chat."
          </p>
        </div>

        {/* Three Columns */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {/* Column 1: Importers & BCOs */}
          <Card className="border-2 border-gray-200 hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Building2 className="w-7 h-7 text-blue-600" />
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                Importers & BCOs
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                Large importers moving through major container ports (JNPT, Mundra, Chennai) with multi-lakh monthly D&D and detention exposure.
              </p>
              
              <div className="space-y-3 pt-2 border-t border-gray-200">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">The pain</p>
                    <p className="text-sm text-gray-600">
                      Multi-lakh monthly demurrage and detention charges. Stuck between port authorities, customs, carriers, and warehouses when delays hit. Invoices paid because reconstructing dispute packets is slow and demoralizing.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <MessageSquare className="w-5 h-5 text-orange-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">Current workaround</p>
                    <p className="text-sm text-gray-600">
                      WhatsApp groups, phone calls, and scattered PDFs across port desks, CHAs, and transporters. Manual dispute packet assembly from chat histories.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Shield className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">What Ward gives them</p>
                    <p className="text-sm text-gray-600">
                      Automated dispute packets in minutes. Clear delay attribution. Measurable uplift in % invoices contested and % waivers. Ward becomes the default place to check "what happened" when invoices arrive.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Column 2: Forwarders & 3PLs */}
          <Card className="border-2 border-gray-200 hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Truck className="w-7 h-7 text-blue-600" />
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                Forwarders & 3PLs
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                Freight forwarders and 3PLs coordinating customs, ICDs, CFS, and port legs, stuck between multiple parties when delays and storage charges hit.
              </p>
              
              <div className="space-y-3 pt-2 border-t border-gray-200">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">The pain</p>
                    <p className="text-sm text-gray-600">
                      Caught between custodians, customs, carriers, warehouses, and customers. Storage charges pile up. Internal blame games. "We don't know who to blame" escalations kill productivity.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <MessageSquare className="w-5 h-5 text-orange-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">Current workaround</p>
                    <p className="text-sm text-gray-600">
                      WhatsApp coordination across multiple groups (port desk, CHA, transporter, warehouse). TMS systems for the happy path, but disputes still run on chat histories and phone calls.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Shield className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">What Ward gives them</p>
                    <p className="text-sm text-gray-600">
                      Clear timeline reconstruction across ports, ICDs, CFSs, and warehouses. Automated cost allocation. Scorecards for facilities, carriers, and customers. Stops internal blame games.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Column 3: Fleet & Warehouse Operators */}
          <Card className="border-2 border-gray-200 hover:border-blue-500 transition-colors">
            <CardHeader>
              <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Warehouse className="w-7 h-7 text-blue-600" />
              </div>
              <CardTitle className="text-2xl font-bold text-gray-900">
                Fleet & Warehouse Operators
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-600 leading-relaxed">
                Drayage and trucking fleets, warehouse operators, and logistics park managers routinely hit with waiting/detention charges but unable to defend themselves.
              </p>
              
              <div className="space-y-3 pt-2 border-t border-gray-200">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">The pain</p>
                    <p className="text-sm text-gray-600">
                      Waiting/detention charges at ports, ICDs, and warehouses. Warehouse-side delays blamed on transporters. OTIF penalties and chargebacks. Unable to prove "it wasn't our fault."
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <MessageSquare className="w-5 h-5 text-orange-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">Current workaround</p>
                    <p className="text-sm text-gray-600">
                      WhatsApp groups and phone calls. WMS/PMS systems for bookings and inventory, but no neutral log of incidents and delays. Disputes die because there's no provable evidence.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <Shield className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-semibold text-gray-900 mb-1">What Ward gives them</p>
                    <p className="text-sm text-gray-600">
                      One-tap incident logging by drivers and yard staff. Tamper-evident proof of delays. Clear attribution (structural vs operational). Dispute packets that hold up with port authorities and customers.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Why Now (India) */}
        <div className="mt-16 p-8 bg-gray-50 rounded-lg border-2 border-gray-200">
          <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">
            Why now (India)
          </h3>
          <div className="max-w-3xl mx-auto space-y-4 text-gray-700 leading-relaxed">
            <p>
              India's freight management and transportation management markets are multi-billion and growing ~10-11% annually. The warehouse platform/PMS/WMS space is scaling with Grade A parks and marketplaces. But none of those layers currently own "truth under dispute"—they optimize bookings, inventory, and routes, but still rely on informal evidence when money is contested.
            </p>
            <p>
              At the same time, rising pressure from GST, e-way bills, banks, insurers, and auditors requires provable evidence. Major ports like JNPT, Mundra, and Chennai are in the global top tier for daily D&D charges, with tariffs that escalate quickly. Indian courts routinely uphold port and custodian rights to levy demurrage even when customs or agencies caused delay—which means importers and intermediaries need concrete, time-stamped proof to dispute charges.
            </p>
            <p className="font-semibold text-gray-900">
              The problem isn't lack of data. The problem is lack of provable evidence when money and blame are on the line. That's the whitespace Ward fills.
            </p>
          </div>
          <div className="text-center mt-6">
            <Link to="/why-ward">
              <Button variant="link" className="text-blue-600 hover:text-blue-700">
                Read our full philosophy <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

