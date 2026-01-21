# IS Curve Slope Classification - Quick Start Guide

## The Core Question

**Does the speaker express a belief about how sensitive output/growth is to monetary policy?**

This is about **policy transmission to output** - how much does changing interest rates affect real economic activity?

---

## Quick Decision Tree

```
1. Does the quote connect MONETARY POLICY to OUTPUT/GROWTH outcomes?
   NO  -> NULL
   YES -> Continue to #2

2. What does the speaker believe about policy effectiveness?
   - Policy is strongly working / clear effects -> FLAT
   - Policy has some/modest/limited effects -> MODERATE
   - Policy isn't working / resilient economy -> STEEP
   - No clear belief about effectiveness -> NULL
```

---

## Category Definitions

### FLAT
Output is **HIGHLY SENSITIVE** to monetary policy.

**Look for:**
- Causal language: "rate hikes are slowing", "policy is restraining"
- Traction language: "gaining traction", "working through", "biting"
- Concern about overtightening: "risk of slowing too much", "could tip into recession"
- Effectiveness affirmation: "policy is working", "already seeing impact"

**Examples:**
- "Our rate increases are clearly slowing interest-sensitive sectors"
- "Policy tightening is gaining traction and restraining demand"
- "Further rate hikes risk tipping the economy into recession"

### MODERATE
**QUALIFIED or PARTIAL** transmission from policy to output.

**Look for:**
- Hedging: "some", "modest", "incremental", "limited", "to some extent"
- Mixed channels: works in some sectors but not others
- Conditionality: "depends on", "in certain circumstances"
- Weakening transmission: "less than before", "diminished effect"

**Examples:**
- "An incremental prod towards activity in the real economy"
- "Policies contributed to mortgage and auto borrowing, but business investment remained weak"
- "We see limited passthrough from policy to spending"
- "Some transmission is occurring, but effects are modest"

### STEEP
Output is **RELATIVELY INSENSITIVE** to monetary policy.

**Look for:**
- Resilience despite policy: "despite tightening, growth continues"
- Impairment language: "transmission impaired", "pushing on a string"
- Skepticism: "less effect than expected", "not seeing impact"
- Other factors dominate: "fiscal policy driving growth", "structural factors"

**CRITICAL - "Despite/Even as" construction:**
- "even with several more rate increases, the economy should expand" -> STEEP
- "maintained solid momentum even as we reduce accommodation" -> STEEP

**Examples:**
- "Despite 300 basis points of tightening, growth remains above trend"
- "The economy has proven surprisingly resilient to higher rates"
- "A further 25 basis point cut will do nothing to change the outlook"

### NULL (Default)
No IS curve slope belief expressed.

**Use when:**
- Only mentions policy OR growth (not both connected)
- Describes data without interpreting policy transmission
- Discusses policy decisions without mechanism
- Forecasts growth without linking to policy
- Focuses on INFLATION effects only, not OUTPUT effects

---

## Critical Distinctions

### Inflation Channel vs. Output Channel

Only classify if discussing **OUTPUT** effects:

| Quote | Classification | Why |
|-------|---------------|-----|
| "Rate hikes will reduce inflation" | NULL | Inflation channel only |
| "Rate hikes will slow growth" | FLAT | Output channel |
| "Rate hikes will slow growth, reducing inflation" | FLAT | Output channel explicit |
| "Tightening will cool demand" | FLAT | Demand = output |

### "Resilient" and "Solid Growth" Language

| Context | Classification |
|---------|---------------|
| "solid growth DESPITE tightening" | STEEP |
| "solid growth BECAUSE of accommodation" | FLAT |
| "solid growth" (no policy connection) | NULL |

### Lag Discussions

| Statement | Classification | Why |
|-----------|---------------|-----|
| "Effects in 2-3 quarters" | FLAT | Normal transmission working |
| "Won't see effects for 2+ years" | STEEP | Very weak near-term transmission |
| "Long and variable lags" (without specifics) | NULL | Too vague |

---

## Policy Preference vs. Transmission Belief

**Important:** A member can believe the IS curve is flat and be either hawkish or dovish!

| Combination | Example |
|-------------|---------|
| Dovish + Flat | "We should cut because lower rates will meaningfully boost growth" |
| Hawkish + Flat | "We should pause because our hikes are already slowing the economy" |
| Dovish + Steep | "Cutting won't help much - the problems aren't monetary" |
| Hawkish + Steep | "We can keep tightening - the economy is resilient to rate increases" |

**Focus on the TRANSMISSION BELIEF, not the policy preference.**

---

## Common Mistakes to Avoid

### Mistake 1: Classifying Pure Policy Statements
- "We should raise rates by 25bp" -> **NULL** (no output mechanism)
- "We should raise rates to slow the economy" -> **FLAT** (mechanism stated)

### Mistake 2: Classifying Pure Forecasts
- "Growth will slow next year" -> **NULL** (no policy link)
- "Growth will slow because policy is restrictive" -> **FLAT**

### Mistake 3: Confusing Inflation and Output Channels
- "Rate hikes will bring down inflation" -> **NULL** (inflation channel)
- "Rate hikes will reduce demand" -> **FLAT** (output channel)

---

## Workflow Tips

1. **Save every 20-30 arguments** - Download your CSV regularly
2. **When in doubt, choose NULL** - It's the default for a reason
3. **Use the notes field** - Flag uncertain cases for later review
4. **Take breaks** - Fresh eyes catch more nuance
5. **Focus on output, not inflation** - This is about the IS curve

---

## Example Classifications

| Quote | Classification | Why |
|-------|---------------|-----|
| "Our rate increases are clearly slowing housing" | FLAT | Direct policy -> output link |
| "Some modest effects from our tightening" | MODERATE | Hedged/partial effect |
| "Limited passthrough to business investment" | MODERATE | Qualified transmission |
| "Despite 500bp of hikes, growth remains strong" | STEEP | Resilience to policy |
| "Even with more rate increases, economy should expand 3.5-4%" | STEEP | Despite/even as construction |
| "GDP grew 3% last quarter" | NULL | Just data, no policy link |
| "We should ease policy" | NULL | Preference, no mechanism |
| "Rate hikes will reduce inflation" | NULL | Inflation channel, not output |
