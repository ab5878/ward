# Operator Quick Start Guide
**Get your fleet operational in 15 minutes**

---

## 🚀 Quick Start (15 Minutes)

### Step 1: Sign Up (2 minutes)
1. Go to `ward-logic.vercel.app`
2. Click **"Start Pilot"**
3. Enter:
   - Company name
   - Email
   - Phone number
   - Approximate fleet size

### Step 2: Add Your Fleet (5 minutes)

**Option A: Manual Entry**
1. Go to **Fleet Management**
2. Click **"Add Vehicle"**
3. Enter for each vehicle:
   - Vehicle number (e.g., MH-12-AB-1234)
   - Driver name
   - Driver phone
   - Route (e.g., JNPT-Delhi)

**Option B: Bulk Upload (CSV)**
1. Download CSV template
2. Fill in vehicle details:
   ```csv
   vehicle_number,driver_name,driver_phone,route,vehicle_type
   MH-12-AB-1234,Ramesh Kumar,+91-98765-43211,JNPT-Delhi,truck
   MH-12-AB-1235,Suresh Singh,+91-98765-43212,Mundra-Mumbai,truck
   ```
3. Upload CSV file

**Option C: API Integration**
1. Get API key from Settings
2. Use API to sync vehicles from your TMS/ERP
3. See `OPERATOR_API_DOCS.md` for details

### Step 3: Onboard Drivers (3 minutes)
1. Go to **Operator Dashboard** → **Drivers** tab
2. Click **"Generate Magic Links"**
3. Share links via WhatsApp/SMS:
   - Copy link for each vehicle
   - Send to driver via WhatsApp
   - Driver clicks link → Opens Ward app

**OR Generate QR Codes:**
1. Click **"Generate QR Codes"**
2. Print QR codes
3. Stick in vehicles
4. Driver scans → Opens app

### Step 4: Configure Settings (5 minutes)
1. Go to **Settings**
2. **Notifications:**
   - Enable email alerts
   - Enable WhatsApp (optional)
   - Enable SMS (optional)
3. **Webhooks:**
   - Add your webhook URL
   - Select events to subscribe
4. **Branding (Optional):**
   - Add company logo
   - Set primary color

---

## 📱 Driver Experience

### What Drivers See
1. **Click Magic Link** (from WhatsApp/SMS)
2. **See Vehicle Info** (auto-loaded)
3. **Tap "Report Problem"**
4. **Speak** (in any language)
5. **Done** (case created automatically)

**No login. No typing. No training.**

---

## 🎯 Daily Operations

### For Operators
1. **View Dashboard** - See all cases, metrics
2. **Manage Fleet** - Add/edit vehicles
3. **Generate Links** - Create driver access
4. **Track Performance** - Analytics, reports

### For Drivers
1. **Report Disruption** - Tap button, speak
2. **See Confirmation** - Case ID shown
3. **Continue Working** - No follow-up needed

---

## 📊 Dashboard Overview

### Key Metrics
- **Fleet Size** - Total vehicles
- **Active Cases** - Ongoing disruptions
- **Financial Impact** - Total ₹ at risk
- **Evidence Ready** - Cases ready for dispute

### Views
- **Overview** - Cases by route
- **Fleet** - All vehicles
- **Drivers** - Generate links
- **Routes** - Route performance

---

## 🔗 Integration Options

### Level 1: Standalone
- Use Ward web dashboard
- Drivers use mobile app
- Manual data entry
- **Best for:** Small operators (<50 vehicles)

### Level 2: API Integration
- Connect your TMS/ERP
- Real-time case sync
- Webhook notifications
- **Best for:** Medium operators (50-500 vehicles)

### Level 3: Embedded
- Ward embedded in your app
- Single sign-on
- Custom branding
- **Best for:** Large operators (500+ vehicles)

---

## 🆘 Troubleshooting

### Driver Can't Access App
- Check magic link is not expired (30 days)
- Verify link was sent correctly
- Generate new link if needed

### Cases Not Appearing
- Check driver reported correctly
- Verify vehicle is linked to operator
- Check dashboard filters

### Webhook Not Working
- Verify webhook URL is correct
- Check events are subscribed
- Test webhook endpoint manually

---

## 📞 Support

- **Email:** support@ward.ai
- **WhatsApp:** +91-XXXXX-XXXXX
- **Hours:** 9 AM - 6 PM IST

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

**Ready to start?** Visit: `ward-logic.vercel.app/register`

---

**Last Updated:** December 2024

