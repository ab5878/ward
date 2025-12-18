# Transport Operator Onboarding - Plug & Play Guide
**Target:** Transport operators in India (fleet owners, logistics companies)  
**Goal:** Get operational in <15 minutes

---

## 🎯 The Plug & Play Promise

**For Transport Operators:**
> "Connect your fleet to Ward in 15 minutes. Your drivers get a simple app. You get dispute-proof evidence. No IT team needed."

---

## 🚀 Quick Start (15 Minutes)

### Step 1: Sign Up (2 minutes)
1. Go to `ward-logic.vercel.app`
2. Click "Start Pilot"
3. Enter:
   - Company name
   - Email
   - Phone number
   - Fleet size (approximate)

### Step 2: Add Your Fleet (5 minutes)
**Option A: Manual Entry**
- Add vehicles one by one
- Enter: Vehicle number, driver name, phone

**Option B: Bulk Upload (CSV)**
- Download template
- Fill: Vehicle number, Driver name, Phone, Route
- Upload CSV

**Option C: API Integration**
- Get API key
- Send fleet data via API
- Real-time sync

### Step 3: Share Driver App (3 minutes)
**Magic Link Method:**
1. Generate driver links (one per driver)
2. Send via WhatsApp/SMS
3. Driver clicks link → Opens Ward app
4. No login required for drivers

**QR Code Method:**
1. Generate QR codes per vehicle
2. Print and stick in vehicle
3. Driver scans → Opens app for that vehicle

### Step 4: Start Using (5 minutes)
- Driver reports disruption via voice
- You see it on dashboard
- Evidence auto-collected
- Dispute packet ready when needed

---

## 📱 Driver Experience (Zero Training)

### What Drivers See
1. **One Big Button:** "Report Problem"
2. **Tap → Speak → Done**
   - No typing
   - Works in Hindi/English/Regional languages
   - Works offline (syncs later)

### What Happens Automatically
- GPS location captured
- Timestamp recorded
- Vehicle ID attached
- Voice transcribed
- Evidence score calculated

---

## 🔌 Integration Options

### Level 1: Standalone (No Integration)
- Use Ward web dashboard
- Drivers use mobile app
- Manual data entry
- **Best for:** Small operators (<50 vehicles)

### Level 2: API Integration
- Connect your TMS/ERP
- Real-time case sync
- Webhook notifications
- **Best for:** Medium operators (50-500 vehicles)

### Level 3: Embedded Integration
- Ward embedded in your app
- Single sign-on
- Custom branding
- **Best for:** Large operators (500+ vehicles)

---

## 🎯 Operator Dashboard Features

### Real-Time Visibility
- **Active Disruptions:** See all ongoing issues
- **Financial Impact:** Total demurrage risk (₹)
- **Evidence Status:** Which cases are dispute-ready
- **Driver Activity:** Who reported what, when

### Smart Filters
- By route (Mumbai-Delhi, etc.)
- By facility (JNPT, Mundra, etc.)
- By status (needs attention, resolved)
- By financial impact (high/medium/low)

### Quick Actions
- **Generate Dispute Packet:** One-click export
- **Assign Owner:** Route to operations manager
- **Contact Driver:** Direct WhatsApp/call
- **View Timeline:** See full evidence chain

---

## 📊 Operator-Specific Metrics

### Primary KPIs
1. **Time to Evidence (TTE):** How fast drivers report
2. **Evidence Completeness:** % of cases dispute-ready
3. **Dispute Win Rate:** % of disputes won
4. **Cost Avoided:** Total ₹ saved from disputes

### Operational Metrics
- Cases per route
- Cases per facility
- Cases per driver
- Average resolution time

---

## 🔗 API Integration Guide

### Authentication
```bash
# Get API Key from Settings
curl -X POST https://ward-logic.vercel.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "operator@company.com", "password": "password"}'
```

### Create Movement (Shipment)
```bash
curl -X POST https://ward-logic.vercel.app/api/v0/movements \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "SHIPMENT-12345",
    "container_id": "MSKU987654",
    "truck_id": "MH-12-AB-1234",
    "bill_of_lading": "BL-2024-001",
    "lane": "JNPT-Delhi",
    "planned_start_date": "2024-12-15T10:00:00Z",
    "planned_end_date": "2024-12-17T18:00:00Z"
  }'
```

### Webhook Notifications
```bash
# Configure webhook URL in Settings
POST https://your-system.com/ward-webhook
{
  "event": "disruption_reported",
  "movement_id": "uuid",
  "timestamp": "2024-12-15T10:30:00Z",
  "data": {
    "description": "Container stuck at gate",
    "financial_impact": 5000,
    "evidence_score": 45
  }
}
```

---

## 🎨 Customization Options

### Branding
- Add your company logo
- Custom colors
- Company name in app

### Workflows
- Custom statuses
- Custom fields
- Custom notifications

### Integrations
- WhatsApp Business API
- SMS gateway
- Email notifications
- Slack/Teams alerts

---

## 💰 Pricing for Operators

### Pilot (30 Days)
- **Free**
- Up to 100 vehicles
- Unlimited cases
- Full features

### Standard
- **Base Fee:** ₹5,000/month
- **Per Vehicle:** ₹50/month
- **Success Share:** 10% of recovered charges

### Enterprise
- **Custom pricing**
- Dedicated support
- Custom integrations
- SLA guarantees

---

## 📚 Operator Resources

### Documentation
- API reference
- Integration guides
- Video tutorials
- Best practices

### Support
- WhatsApp support: +91-XXXXX-XXXXX
- Email: support@ward.ai
- Office hours: 9 AM - 6 PM IST

### Community
- Operator forum
- Case studies
- Webinars
- Training sessions

---

## ✅ Success Checklist

### Week 1
- [ ] Account created
- [ ] Fleet added
- [ ] Drivers onboarded
- [ ] First case reported

### Week 2
- [ ] Dashboard configured
- [ ] Notifications set up
- [ ] Team trained
- [ ] First dispute packet generated

### Month 1
- [ ] 10+ cases logged
- [ ] Evidence score >70% on cases
- [ ] First dispute won
- [ ] ROI calculated

---

## 🎯 Next Steps

1. **Sign Up:** Start your 30-day free pilot
2. **Add Fleet:** Upload your vehicles
3. **Onboard Drivers:** Share magic links
4. **Start Using:** Report first disruption
5. **See Results:** Track evidence and disputes

**Ready to start?** Visit: `ward-logic.vercel.app/register`

---

**Last Updated:** December 2024

