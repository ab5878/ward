# Ward India Lighthouse Experiments: Founder Playbook

**Version:** 1.0  
**Date:** December 2024  
**Status:** Ready for Execution  
**Target:** 3-5 lighthouse customers in India

---

## 1. Hypothesis & Objectives

### 1.1 Core Hypothesis

**Primary Hypothesis:**
Ward can increase contest rates and waivers enough to comfortably pay for base SaaS + success fee within 3-6 months for Indian importers/forwarders/3PLs with significant D&D and detention/waiting exposure at major ports (JNPT, Mundra, Chennai) and associated ICDs/CFSs/logistics parks.

**Supporting Hypotheses:**
1. **Contest rate hypothesis:** Ward increases % invoices contested from baseline (10-15%) to 40-50% by making dispute packet generation fast and credible
2. **Waiver rate hypothesis:** Ward increases % waivers/discounts from baseline (2-5% of contested) to 20-30% by providing tamper-evident evidence that port authorities/courts accept
3. **Time savings hypothesis:** Ward reduces internal time per dispute from 4-8 hours to 1-2 hours by automating timeline reconstruction and packet generation
4. **Blame game hypothesis:** Ward reduces "we don't know who to blame" escalations by 60-80% through clear delay attribution

**Success Criteria:**
- Customer ROI positive within 3-6 months (savings > base fee + success fee)
- Measurable uplift in all 4 metrics above
- Customer willing to expand to more lanes/facilities
- Customer willing to be reference case (anonymized)

### 1.2 Objectives for First 3-5 Lighthouse Customers

**Objective 1: Prove Product-Market Fit**
- Demonstrate Ward increases contest rates and waivers measurably
- Show dispute packets are accepted by port authorities/facilities
- Validate that ops/finance teams actually use Ward (not just sign up)

**Objective 2: Generate Proof Points**
- Create 3-5 anonymized case studies with concrete before/after stories
- Generate data: "D&D + waiting billed vs waived/discounted" graphs
- Document dispute stories: WhatsApp chaos → invoice paid vs Ward packet → waiver

**Objective 3: Validate Pricing Model**
- Test different commercial structures (base + success fee variations)
- Find pricing that works for customers and is sustainable for Ward
- Establish baseline for future customers

**Objective 4: Learn & Iterate**
- Understand which dispute formats work at which ports/facilities
- Learn which features matter most (mobile capture, web console, dispute packets)
- Identify blockers and friction points

**Objective 5: Build Data Flywheel**
- Collect data on which combinations of ports, facilities, lanes, CHAs, actions correlate with paid vs waived charges
- Build knowledge base: "this format worked X times at JNPT/Mundra/Chennai"
- Create de facto standard for dispute formats in India

---

## 2. Experiment Design

### 2.1 Experiment Structure 1: Before/After on Same Corridors

**Design:**
- Measure baseline metrics for 1-2 months (before Ward)
- Deploy Ward on same corridors
- Measure metrics for 3-4 months (after Ward)
- Compare before vs after

**Duration:**
- Baseline period: 1-2 months
- Intervention period: 3-4 months
- Total: 4-6 months

**Sample Size:**
- Minimum: 50 invoices per corridor per month
- Target: 100+ invoices per corridor per month
- Total: 200-400 invoices per customer over experiment period

**Required Data:**
- Historical invoices (last 6-12 months) for baseline
- Invoice details: amount, facility, charge type, date, outcome (paid/contested/waived)
- Internal time logs: hours spent per dispute (if available)
- Escalation logs: count of "we don't know who to blame" escalations

**Metrics:**
1. **% Invoices Contested**
   - Baseline: Historical % of invoices that were contested
   - After: % of invoices with Ward logs that are contested
   - Target: 3-5x increase (e.g., 15% → 45%)

2. **% Waivers/Discounts**
   - Baseline: Historical % of contested invoices that resulted in waiver/discount
   - After: % of contested invoices with Ward packets that result in waiver/discount
   - Target: 5-10x increase (e.g., 3% → 25%)

3. **Average Time Per Dispute**
   - Baseline: Hours spent per dispute (gathering evidence, assembling packet)
   - After: Hours spent per dispute with Ward
   - Target: 50-70% reduction (e.g., 6 hours → 2 hours)

4. **"We Don't Know Who to Blame" Escalations**
   - Baseline: Count of escalations where delay attribution was unclear
   - After: Count of escalations with Ward timelines
   - Target: 60-80% reduction

**Qualitative Signals:**
- Finance team willingness to contest invoices (survey: 1-10 scale)
- Ops team confidence in delay attribution (survey: 1-10 scale)
- Legal team confidence in dispute packets (survey: 1-10 scale)
- Customer willingness to expand to more lanes/facilities

**Pros:**
- Simple to understand and execute
- Clear before/after comparison
- Works well for single customer, single corridor

**Cons:**
- No control group (can't rule out external factors)
- Seasonal variations might affect results
- Takes longer (need baseline period)

**When to Use:**
- First lighthouse customer
- Single corridor focus
- When historical data is available

### 2.2 Experiment Structure 2: Corridor A (Ward) vs Corridor B (Control)

**Design:**
- Select 2 similar corridors (same port, similar volume, similar characteristics)
- Deploy Ward on Corridor A
- Keep Corridor B as control (no Ward, continue with WhatsApp/current process)
- Measure metrics for both corridors simultaneously
- Compare Corridor A vs Corridor B

**Duration:**
- 3-4 months (no baseline period needed)

**Sample Size:**
- Minimum: 50 invoices per corridor per month
- Target: 100+ invoices per corridor per month
- Total: 300-400 invoices per customer over experiment period

**Required Data:**
- Invoice data for both corridors (current and historical)
- Ability to track invoices by corridor (lane, facility, route)
- Similar characteristics: volume, facility types, charge types

**Metrics:**
Same as Experiment 1, but compare:
- Corridor A (Ward) vs Corridor B (Control)
- Statistical significance: p < 0.05

**Qualitative Signals:**
- Ops team preference: Which corridor is easier to manage?
- Finance team preference: Which corridor disputes are easier to handle?
- Customer willingness to expand Ward to Corridor B

**Pros:**
- Controls for external factors (seasonality, market conditions)
- Faster (no baseline period)
- More convincing proof (A/B test)

**Cons:**
- Requires 2 similar corridors (may not always be available)
- Customer may want Ward on both corridors (ethical consideration)
- More complex to execute

**When to Use:**
- Customer has multiple similar corridors
- Need faster results
- Want more rigorous proof

### 2.3 Experiment Structure 3: "Ops-Only" vs "Ops + Finance/Legal" Usage

**Design:**
- Deploy Ward to ops team only (mobile capture, timeline viewing)
- Measure metrics for 1-2 months
- Then enable finance/legal features (dispute packet generation, export)
- Measure metrics for 1-2 months
- Compare ops-only vs full usage

**Duration:**
- Ops-only period: 1-2 months
- Full usage period: 1-2 months
- Total: 2-4 months

**Sample Size:**
- Minimum: 50 invoices per period
- Target: 100+ invoices per period

**Required Data:**
- Usage logs: Who used Ward, what features, when
- Invoice outcomes: Tracked by usage type (ops-only vs full)

**Metrics:**
1. **Feature Adoption**
   - Ops-only: % of incidents captured via mobile
   - Full: % of incidents captured + % of invoices with dispute packets generated

2. **Contest Rate**
   - Ops-only: % invoices contested (may be lower, ops can see timeline but finance may not use it)
   - Full: % invoices contested (should be higher, finance can generate packets easily)

3. **Waiver Rate**
   - Ops-only: % waivers (may be lower, packets may not be generated)
   - Full: % waivers (should be higher, packets are generated and submitted)

4. **Time Savings**
   - Ops-only: Time saved in timeline reconstruction
   - Full: Time saved in timeline + packet generation

**Qualitative Signals:**
- Which features drive most value? (mobile capture vs dispute packets)
- What's the adoption curve? (ops adopts faster vs finance/legal)
- What are the blockers? (training, permissions, workflow integration)

**Pros:**
- Understands feature value (which features matter most)
- Phased rollout reduces risk
- Identifies adoption blockers early

**Cons:**
- Takes longer (phased approach)
- May not show full potential (if finance/legal don't adopt)
- More complex to analyze

**When to Use:**
- Want to understand feature value
- Phased rollout preferred
- Testing different user personas

---

## 3. ICP & Corridor Selection

### 3.1 Lighthouse Customer Criteria

**Must-Have Criteria:**

1. **Significant D&D Exposure**
   - Multi-lakh monthly D&D and detention/waiting charges (minimum ₹5-10 lakh/month)
   - Exposure at 1-2 major ports (JNPT, Mundra, Chennai) and associated ICDs/CFSs/logistics parks
   - Clear pain point: "we're paying too much, can't dispute effectively"

2. **WhatsApp Central to Ops**
   - WhatsApp currently central to ops and dispute recollection for target corridors
   - Evidence of WhatsApp chaos: "we can't find the message", "screenshot doesn't work"
   - Willingness to try alternative (not completely resistant to change)

3. **Willingness to Experiment**
   - Willing to run structured before/after experiments
   - Willing to share data (invoices, outcomes, time logs)
   - Willing to be reference case (anonymized)
   - Decision-maker accessible (founder/CEO/COO, not just ops manager)

4. **Right Size**
   - Large enough: 50+ invoices per month in target corridors
   - Small enough: Can get decision-maker attention, not too bureaucratic
   - Sweet spot: ₹50-500 crore revenue, 100-1000 employees

**Nice-to-Have Criteria:**

1. **Multiple Corridors**
   - Has multiple corridors (allows A/B testing)
   - Plans to expand (good for expansion within customer)

2. **Tech-Forward**
   - Already uses TMS/WMS systems
   - Comfortable with SaaS tools
   - Has internal tech/ops team

3. **Reference Potential**
   - Well-known in industry (good for references)
   - Willing to speak at events (if successful)
   - Has network (can introduce other customers)

**Red Flags:**

1. **Too Small**
   - < ₹5 lakh/month D&D exposure (may not justify cost)
   - < 20 invoices/month (sample size too small)

2. **Too Large/Bureaucratic**
   - > ₹5000 crore revenue (too slow, too many stakeholders)
   - Requires 6+ month procurement process

3. **Resistant to Change**
   - "We've always done it this way"
   - Unwilling to share data
   - Unwilling to experiment

4. **Wrong Problem**
   - D&D exposure is low (not core problem)
   - Already has effective dispute process (no pain point)

### 3.2 Corridor Selection Criteria

**Must-Have Criteria:**

1. **High D&D Exposure**
   - Corridor has significant D&D/detention/waiting charges
   - Minimum: ₹2-3 lakh/month per corridor
   - Clear pain point: "this corridor costs us the most"

2. **WhatsApp Reliance**
   - WhatsApp currently used for ops coordination on this corridor
   - Evidence of disputes/invoices from this corridor
   - Ops team familiar with this corridor

3. **Facility Coverage**
   - Corridor includes 1-2 major ports (JNPT, Mundra, Chennai)
   - Includes associated ICDs/CFSs/logistics parks
   - Facilities are accessible (can deploy Ward mobile app to drivers/yard staff)

4. **Volume**
   - Minimum: 20-30 invoices per month
   - Target: 50+ invoices per month
   - Enough volume for statistical significance

**Nice-to-Have Criteria:**

1. **Similar Corridors Available**
   - Has similar corridor for A/B testing
   - Same port, similar volume, similar characteristics

2. **Clear Boundaries**
   - Corridor is well-defined (specific route, specific facilities)
   - Easy to track invoices by corridor

3. **Growth Potential**
   - Corridor is growing (good for expansion)
   - Customer plans to expand this corridor

**Corridor Examples:**

1. **JNPT → Delhi (via ICD)**
   - Port: JNPT
   - ICD: Dadri ICD, Tughlakabad ICD
   - Logistics parks: Multiple along route
   - High volume, high D&D exposure

2. **Mundra → Ahmedabad (via CFS)**
   - Port: Mundra
   - CFS: Multiple CFSs in Ahmedabad
   - High volume, high detention charges

3. **Chennai → Bangalore (via logistics parks)**
   - Port: Chennai
   - Logistics parks: Multiple Grade A parks
   - High waiting charges

---

## 4. Offer Structures

### 4.1 Offer Structure 1: Base Fee Waived + Success Fee Only

**Structure:**
- Base SaaS fee: ₹0 for first 3 months, then ₹X per site/corridor
- Success fee: Y% of recovered/avoided D&D and detention/waiting charges
- Minimum commitment: 3 months
- Success fee cap: None (or very high cap)

**Example:**
- Base fee: ₹0 for months 1-3, then ₹50,000/month per corridor
- Success fee: 15% of recovered/avoided charges
- Customer saves ₹10 lakh in months 1-3 → Ward earns ₹1.5 lakh

**Pros:**
- Low risk for customer (no upfront cost)
- Aligns incentives (Ward only earns if customer saves)
- Easy to sell ("try it, if it works you pay")

**Cons:**
- Ward bears all risk (no revenue if customer doesn't save)
- May attract tire-kickers (customers who won't actually use it)
- Hard to scale (need success to earn revenue)

**When to Use:**
- First lighthouse customer (need proof, willing to take risk)
- Customer is skeptical (need to prove value first)
- High confidence in success (based on customer profile)

### 4.2 Offer Structure 2: Low Base + Capped Success Fee

**Structure:**
- Base SaaS fee: ₹X per site/corridor (discounted, e.g., 50% of standard)
- Success fee: Y% of recovered/avoided charges, capped at Z× base fee
- Minimum commitment: 6 months
- Success fee cap: 2-3× base fee

**Example:**
- Base fee: ₹25,000/month per corridor (50% discount)
- Success fee: 20% of recovered/avoided charges, capped at ₹75,000/month (3× base)
- Customer saves ₹10 lakh/month → Ward earns ₹25,000 (base) + ₹75,000 (capped success) = ₹1 lakh/month

**Pros:**
- Balanced risk (Ward gets base revenue, customer gets capped success fee)
- Predictable revenue for Ward
- Predictable cost for customer (capped success fee)

**Cons:**
- Less incentive alignment (Ward gets base even if no success)
- Customer may feel capped success fee limits upside
- More complex to explain

**When to Use:**
- Customer wants predictable costs
- Ward wants predictable revenue
- Standard offer for lighthouse customers

### 4.3 Offer Structure 3: Standard Base + Success % with Strong ROI Guarantee

**Structure:**
- Base SaaS fee: ₹X per site/corridor (standard pricing)
- Success fee: Y% of recovered/avoided charges
- ROI guarantee: If customer doesn't save at least 2× (base + success fee) in 6 months, refund base fee
- Minimum commitment: 6 months

**Example:**
- Base fee: ₹50,000/month per corridor
- Success fee: 15% of recovered/avoided charges
- ROI guarantee: If customer doesn't save ₹6 lakh in 6 months (2× ₹3 lakh base), refund base fee
- Customer saves ₹10 lakh in 6 months → Ward earns ₹3 lakh (base) + ₹1.5 lakh (success) = ₹4.5 lakh

**Pros:**
- Strong value proposition (ROI guarantee)
- Aligns incentives (Ward only keeps base if customer succeeds)
- Professional (shows confidence)

**Cons:**
- Ward bears risk (may need to refund base)
- Requires strong confidence in success
- May set high expectations

**When to Use:**
- Customer wants strong guarantee
- Ward has high confidence (based on customer profile, corridor)
- Want to differentiate from competitors

### 4.4 Founder's Perspective: Which Offer to Use

**First Lighthouse Customer:**
- Use Offer 1 (Base Fee Waived + Success Fee Only)
- Rationale: Need proof, willing to take risk, need to prove value

**Second/Third Lighthouse Customer:**
- Use Offer 2 (Low Base + Capped Success Fee)
- Rationale: Have some proof, want balanced risk, standardize pricing

**Fourth/Fifth Lighthouse Customer:**
- Use Offer 3 (Standard Base + ROI Guarantee) or Offer 2
- Rationale: Have proof, can offer guarantee, or standardize on Offer 2

**General Rule:**
- Start with riskier offers (Offer 1) to get proof
- Move to balanced offers (Offer 2) as you get proof
- Use guarantees (Offer 3) when you have strong proof and confidence

---

## 5. Decision Rules

### 5.1 When to Expand Within a Customer

**Expand to More Lanes/Facilities If:**

1. **Metrics Are Positive**
   - Contest rate increased by 2× or more
   - Waiver rate increased by 3× or more
   - Time savings of 40% or more
   - Customer ROI positive (savings > base + success fee)

2. **Customer Is Engaged**
   - Ops team actively using mobile app (70%+ adoption)
   - Finance team generating dispute packets (5+ packets per month)
   - Customer asking to expand ("can we add more corridors?")

3. **Data Quality Is Good**
   - 90%+ of incidents have GPS, device ID, timestamp, voice recording
   - Dispute packets are being submitted and accepted
   - No major data quality issues

4. **Customer Is Willing**
   - Customer willing to pay for expansion (base fee for new corridors)
   - Customer willing to commit to longer term (6+ months)
   - Customer willing to be reference case

**Do NOT Expand If:**

1. **Metrics Are Negative**
   - No increase in contest rate or waiver rate
   - No time savings
   - Customer ROI negative

2. **Customer Is Not Engaged**
   - Low adoption (< 30% of incidents captured)
   - Finance team not using dispute packets
   - Customer not asking to expand

3. **Data Quality Is Poor**
   - < 70% of incidents have required metadata
   - Dispute packets being rejected
   - Major data quality issues

4. **Customer Is Unwilling**
   - Customer not willing to pay for expansion
   - Customer not willing to commit
   - Customer not willing to be reference

**Expansion Process:**

1. **Review Metrics** (monthly)
   - Check all 4 metrics (contest rate, waiver rate, time savings, escalations)
   - Check customer engagement (usage logs, feature adoption)
   - Check data quality (metadata completeness, packet acceptance)

2. **Customer Conversation** (month 2-3)
   - Discuss expansion opportunity
   - Understand customer interest
   - Negotiate pricing for expansion

3. **Expansion Decision** (month 3-4)
   - If metrics positive + customer engaged + customer willing → expand
   - If not → continue current corridors, reassess in 1-2 months

### 5.2 When to Standardize Pricing

**Standardize Pricing If:**

1. **Have 3+ Successful Lighthouse Customers**
   - At least 3 customers with positive ROI
   - At least 3 customers with measurable uplift in metrics
   - At least 3 customers willing to expand

2. **Pricing Model Is Validated**
   - Base + success fee model works
   - Pricing levels are sustainable (customer can pay, Ward can earn)
   - No major pricing issues

3. **Have Reference Cases**
   - Have 3+ anonymized case studies
   - Have concrete before/after stories
   - Have data graphs ("billed vs waived")

**Standardized Pricing (After Validation):**

- **Base Fee:** ₹50,000-75,000/month per corridor (depending on volume)
- **Success Fee:** 15-20% of recovered/avoided charges
- **Minimum Commitment:** 6 months
- **ROI Guarantee:** Optional (if customer wants it)

**Do NOT Standardize If:**

1. **Don't Have Enough Proof**
   - < 3 successful customers
   - Metrics are inconsistent
   - No reference cases

2. **Pricing Model Not Validated**
   - Pricing levels are unclear
   - Customer feedback is mixed
   - Need more experimentation

### 5.3 When to Stop Investing in a Lane/Customer

**Stop Investing (Reduce Support, Don't Renew) If:**

1. **Metrics Are Consistently Negative** (After 3+ Months)
   - No increase in contest rate or waiver rate (after 3 months)
   - No time savings (after 3 months)
   - Customer ROI negative (after 6 months)

2. **Customer Is Not Engaged** (After 2+ Months)
   - Low adoption (< 30% of incidents captured, after 2 months)
   - Finance team not using dispute packets (after 2 months)
   - Customer not responding to support requests

3. **Data Quality Is Poor** (After 1+ Month)
   - < 70% of incidents have required metadata (after 1 month)
   - Dispute packets being rejected (after 2 months)
   - Major data quality issues that can't be fixed

4. **Customer Is Unwilling to Pay**
   - Customer not willing to pay base fee (after trial period)
   - Customer not willing to pay success fee (disputing outcomes)
   - Customer not willing to commit to longer term

**Stop Investing Process:**

1. **Warning Period** (Month 2-3)
   - Discuss metrics with customer
   - Identify blockers and friction points
   - Offer additional support/training

2. **Decision Point** (Month 3-4)
   - If metrics still negative + customer not engaged → reduce support
   - If metrics improve + customer engaged → continue

3. **Exit Decision** (Month 6)
   - If metrics still negative + customer not engaged + customer not willing to pay → don't renew
   - If metrics improve → renew with standard pricing

**Do NOT Stop Investing If:**

1. **Early Stage** (< 3 months)
   - Too early to judge (need 3-6 months for results)
   - May need more time for adoption

2. **External Factors**
   - Market conditions changed (not Ward's fault)
   - Customer had internal issues (not Ward's fault)
   - One-time events (can recover)

3. **Customer Is Engaged But Metrics Not There Yet**
   - Customer is using Ward actively
   - Customer is willing to continue
   - May need more time or different approach

### 5.4 Decision Framework Summary

**Monthly Review Checklist:**

1. **Metrics Review**
   - [ ] Contest rate: Target 3-5× increase
   - [ ] Waiver rate: Target 5-10× increase
   - [ ] Time savings: Target 50-70% reduction
   - [ ] Escalations: Target 60-80% reduction

2. **Engagement Review**
   - [ ] Mobile app adoption: Target 70%+ of incidents captured
   - [ ] Dispute packet generation: Target 5+ packets per month
   - [ ] Customer feedback: Target positive (survey 7+/10)

3. **Data Quality Review**
   - [ ] Metadata completeness: Target 90%+ of incidents
   - [ ] Dispute packet acceptance: Target 80%+ acceptance rate
   - [ ] No major data quality issues

4. **Customer Willingness Review**
   - [ ] Customer willing to expand: Yes/No
   - [ ] Customer willing to pay: Yes/No
   - [ ] Customer willing to be reference: Yes/No

**Decision Matrix:**

| Metrics | Engagement | Data Quality | Customer Willing | Action |
|---------|-----------|--------------|------------------|--------|
| ✅ Positive | ✅ High | ✅ Good | ✅ Yes | **Expand** |
| ✅ Positive | ✅ High | ✅ Good | ⚠️ Maybe | **Continue, reassess** |
| ✅ Positive | ⚠️ Medium | ✅ Good | ✅ Yes | **Continue, improve engagement** |
| ⚠️ Mixed | ✅ High | ✅ Good | ✅ Yes | **Continue, improve metrics** |
| ❌ Negative | ❌ Low | ❌ Poor | ❌ No | **Stop investing** |

---

## 6. Success Metrics Dashboard

### 6.1 Customer-Level Metrics

**Per Customer, Per Month:**
- Total invoices received
- % invoices contested (vs baseline)
- % waivers/discounts (vs baseline)
- Total dispute value (₹)
- Total waived/saved (₹)
- Average time per dispute (hours)
- "We don't know who to blame" escalations (count)
- Customer ROI (savings - base fee - success fee)

### 6.2 Product Metrics

**Per Customer, Per Month:**
- Mobile app adoption (% incidents captured)
- Dispute packet generation (count)
- Dispute packet acceptance rate (%)
- Feature usage (which features used most)
- Data quality (% incidents with required metadata)

### 6.3 Business Metrics

**Per Customer:**
- Customer acquisition cost (CAC)
- Customer lifetime value (LTV)
- Time to ROI (months)
- Expansion rate (% customers that expand)
- Churn rate (% customers that don't renew)

---

## 7. Execution Timeline

### Month 0: Customer Selection & Onboarding
- Identify 3-5 lighthouse customers
- Select corridors
- Negotiate offer structure
- Sign agreements

### Month 1: Baseline Measurement
- Collect historical data (invoices, outcomes, time logs)
- Measure baseline metrics
- Set up Ward (mobile app deployment, web console access)
- Train ops team (mobile capture)

### Month 2-3: Intervention Period (Early)
- Ops team using mobile app
- Measure early metrics
- Identify blockers and friction points
- Iterate on product/process

### Month 4-5: Intervention Period (Full)
- Finance/legal team using web console
- Dispute packets being generated and submitted
- Measure full metrics
- Collect qualitative feedback

### Month 6: Review & Decision
- Review all metrics (before/after comparison)
- Calculate customer ROI
- Decision: Expand, continue, or stop investing
- Generate case study (if successful)

---

## 8. Risk Mitigation

### 8.1 Customer Risks

**Risk:** Customer doesn't adopt Ward (low usage)
- **Mitigation:** Strong onboarding, training, support, check-ins

**Risk:** Customer doesn't see value (metrics don't improve)
- **Mitigation:** Set expectations, focus on right corridors, iterate on product

**Risk:** Customer doesn't pay (disputes success fee)
- **Mitigation:** Clear success fee definition, transparent reporting, regular reviews

### 8.2 Product Risks

**Risk:** Mobile app doesn't work well (technical issues)
- **Mitigation:** Test on target devices, offline-first, robust error handling

**Risk:** Dispute packets not accepted (format issues)
- **Mitigation:** Research port requirements, iterate on formats, learn from outcomes

**Risk:** Data quality is poor (missing metadata)
- **Mitigation:** Validation, required fields, data quality monitoring

### 8.3 Market Risks

**Risk:** Port authorities don't accept dispute packets
- **Mitigation:** Research requirements, iterate on formats, build relationships

**Risk:** Market conditions change (D&D charges decrease)
- **Mitigation:** Diversify corridors, focus on allocation/standardization value

---

**Document Status:** Ready for Sales & Product Execution  
**Next Steps:** Customer outreach, corridor selection, experiment setup

