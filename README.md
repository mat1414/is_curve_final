# IS Curve Slope Classification Tool

Human validation tool for Claude's classifications of FOMC speaker beliefs about the IS curve slope - how sensitive output/growth is to monetary policy.

## Quick Links

- **Live Tool:** https://iscurvefinal-k7ypqt5ekvlfz4owfqglrs.streamlit.app/
- **GitHub Repo:** https://github.com/mat1414/is_curve_final

---

## Purpose

We used Claude to classify ~82,000 FOMC transcript quotes for beliefs about monetary policy transmission to output. This tool allows human coders to independently classify a stratified sample of 200 quotes, enabling us to measure Claude's accuracy.

**What we're measuring:**
- Does the speaker believe output is **highly sensitive** to monetary policy? (flat IS curve)
- Does the speaker believe transmission is **qualified/partial**? (moderate)
- Does the speaker believe output is **relatively insensitive** to monetary policy? (steep IS curve)
- Classification categories: FLAT, MODERATE, STEEP, NULL

---

## Folder Structure

```
is_curve/
├── README.md                              # This file
├── coding_interface.py                    # Streamlit app (deployed)
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Excludes large files from git
├── is_slope.txt                           # Claude's classification prompt
├── validation_samples/
│   └── production/
│       ├── coding_is_slope.csv            # 200 sampled arguments
│       └── stats_is_slope.json            # Sample statistics
└── sampler/                               # LOCAL ONLY (not deployed)
    └── is_slope_sampler.py                # Script to generate samples
```

**Note:** The `sampler/` folder and `.pkl` files are in `.gitignore` and not pushed to GitHub.

---

## For Coders

### Getting Started

1. Open the tool: https://iscurvefinal-k7ypqt5ekvlfz4owfqglrs.streamlit.app/
2. Enter your name
3. Select "Use default sample"
4. Start classifying quotes

### Classification Categories

| Category | Meaning |
|----------|---------|
| **FLAT** | Output is HIGHLY SENSITIVE to monetary policy. Look for: "policy is gaining traction," "rate hikes are slowing growth," "risk of overtightening." |
| **MODERATE** | Qualified/partial transmission from policy to output. Look for: "some effect," "modest transmission," "limited passthrough." |
| **STEEP** | Output is RELATIVELY INSENSITIVE to monetary policy. Look for: "despite tightening," "resilient to rate increases," "pushing on a string." |
| **NULL** | No IS curve slope belief expressed (default) |

### Key Concept: The IS Curve Slope

The IS curve describes the relationship between interest rates and real economic output. The "slope" refers to how sensitive output is to policy changes:

- **Flat IS curve:** Output responds strongly to interest rate changes. Rate hikes significantly slow growth; rate cuts significantly boost growth.
- **Steep IS curve:** Output is relatively insensitive to interest rate changes. The economy is "resilient" to policy moves.

### What to Look For

**Monetary Policy Indicators:**
- Interest rates, policy rate, fed funds rate
- Rate increases/hikes/tightening, rate cuts/easing
- Policy stance: tight/restrictive/easy/accommodative
- Real rates, monetary conditions

**Output/Growth Outcomes:**
- GDP, output, economic growth, real activity
- Aggregate demand, spending, consumption, investment
- Interest-sensitive sectors (housing, durables, capex)
- Economic slowdown, recession risk

**Causal Connection:**
- The speaker must connect policy to output
- Simply mentioning both is NOT sufficient

### Critical Pattern: "Despite/Even As" Construction

When speakers note that economic performance continues DESPITE or EVEN AS policy changes, this indicates **STEEP**:
- "even with several more rate increases, the economy should expand 3.5-4%"
- "maintained solid momentum even as we reduce policy accommodation"
- "growth seems solid and resilient and in less need of accommodation"

### Important

- **Save often!** Download your CSV every 20-30 arguments
- To resume: upload your saved CSV via "Resume Session"
- When in doubt, select NULL
- Focus on OUTPUT effects, not inflation effects
- Watch for the "despite/even as" construction - this typically indicates STEEP
- "Resilient" in the context of policy changes indicates STEEP

---

## Sample Details

- **Total sample:** 200 quotations
- **Stratification:** 50 FLAT, 50 MODERATE, 50 STEEP, 50 NULL
- **Source:** FOMC meeting transcripts via `combo_argument_panel.pkl`
- **Random seed:** 42 (for reproducibility)

Population statistics (will be updated after resampling):
| Category | Meaning | Sampled |
|----------|---------|---------|
| FLAT     | High sensitivity | 50      |
| MODERATE | Partial transmission | 50      |
| STEEP    | Low sensitivity | 50      |
| NULL     | No belief | 50      |

---

## For Project Leads

### Updating the Sample Data

If you need to regenerate the sample:

```bash
cd is_curve
python3 sampler/is_slope_sampler.py
```

This will:
1. Load `combo_argument_panel.pkl` (contains built-in classifications)
2. Deduplicate quotations
3. Create a stratified sample (50 per category)
4. Output to `validation_samples/production/coding_is_slope.csv`

Then commit and push:
```bash
git add validation_samples/
git commit -m "Regenerate sample data"
git push origin main
```

### Analyzing Results

When coders complete their work, they'll download a CSV with these columns:

| Column | Description |
|--------|-------------|
| `coding_id` | Unique ID (e.g., IS_0042) |
| `original_index` | Index in source data for joining |
| `coder_name` | Who coded this |
| `classification` | Human's classification |
| `claude_is_slope` | Claude's numeric value (1.0, 0.0, -1.0, NaN) |
| `claude_is_slope_category` | Claude's category (steep, moderate, flat, null) |
| `quotation` | The quote text |
| `notes` | Coder's notes (if any) |

**To calculate agreement:**
```python
import pandas as pd

df = pd.read_csv('coded_results.csv')
df['agree'] = df['classification'] == df['claude_is_slope_category']
print(f"Agreement rate: {df['agree'].mean():.1%}")
```

---

## Classification Mapping

| Claude Value | Category | Meaning |
|--------------|----------|---------|
| 1.0 | flat | Output highly sensitive to policy |
| 0.0 | moderate | Qualified/partial transmission |
| -1.0 | steep | Output relatively insensitive to policy |
| NaN | null | No belief expressed |

---

## Reference

This validation follows the framework described in Mullainathan et al. (2024) for validating LLM output through human coding.
