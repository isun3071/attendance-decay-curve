# Attendance Decay Curve (ADC) in Voluntary Student Organizations

**CS506: Data Science Tools and Applications | Boston University | Spring 2026**

> 📺 [Video Presentation](YOUR_YOUTUBE_LINK_HERE)

---

## How to Reproduce Results

```bash
git clone https://github.com/YOUR_REPO_HERE
cd attendance-decay-curve
make install
make run
```

### Requirements
- Python 3.9+
- See `requirements.txt` for full dependency list

### Makefile targets

| Target | Description |
|---|---|
| `make install` | Install all dependencies |
| `make run` | Execute notebook end to end |
| `make test` | Run test suite |
| `make all` | Install and run |

Results are fully reproducible by running `adc.ipynb` from top to bottom against the raw Qualtrics CSV export.

---

## Project Description

If you have ever been to a student organization's first meeting where the room was packed, then watched it slowly empty out over the semester, this project is about that feeling.

The **Attendance Decay Curve (ADC)** is the hypothesis that voluntary student organizations (VSOs) experience a recognizable pattern of high attendance early in the semester that declines over time. This project empirically tests whether that pattern is real, measurable, and statistically significant across BU's VSOs.

This project differs from most CS506 final projects in one important way: all data was collected from scratch. No Kaggle dataset was downloaded. No CSV existed before this project began. Every row in the dataset represents a real BU organization whose leader personally decided to respond to a survey after receiving a cold outreach email. That layer of work, the sampling, instrument and survey design, outreach campaign, and response bias reasoning, is documented in full below.

---

## Research Questions

**Primary:** Do VSOs at BU exhibit a measurable attendance decay pattern over the course of a semester?

**Secondary:**
- Does decay differ across org types (academic, cultural, community, recreational)?
- What trajectory archetypes exist (steep cliff, gradual decay, stable, growth)?
- Can early-semester attendance predict later attendance?

---

## Repository Structure

```
attendance-decay-curve/
├── README.md                  # This file — the final report
├── Makefile                   # Reproducibility commands
├── requirements.txt           # Python dependencies
├── adc.ipynb                  # Main analysis notebook
├── data/
│   └── responses.csv          # Anonymized Qualtrics export
├── orgsscraper.py             # CampusLabs API scraper
├── randomsample.py            # Random org sampler
└── .github/
    └── workflows/
        └── test.yml           # GitHub Actions CI
```

---

## Data Collection

### Population and Sampling Frame

BU's student organizations are catalogued through the CampusLabs / Terrier Central platform. Using a Python scraper (`orgsscraper.py`) against the platform's public-facing JSON API endpoints, we built a sampling frame of **302 organizations** filtered to four SAO categories:

- Academic and Pre-Professional
- Community, Peace and Justice
- Cultural
- Recreation

Political + religious organizations, as well as fraternities, were excluded as their participation dynamics are driven by different mechanisms than voluntary engagement.

### Sampling Strategy

Initial outreach batches were selected via random sampling from the 302-org frame using `randomsample.py`. Subsequent batches incorporated purposive selection to ensure adequate representation across all four SAO categories, particularly for cultural and community engagement organizations underrepresented in early random draws. A small number of organizations were selected based on prior familiarity, a known but minor source of selection bias acknowledged in the limitations section.

**About 172 of 302 organizations (57%) were contacted.**

### Survey Instrument

A Qualtrics survey (BU-hosted) was designed and deployed to organization leaders. The survey used branching logic to route respondents into one of two paths:

**Path A (recurring meeting orgs):** collected first meeting attendance, most recent meeting attendance, number of meetings held, optional intermediate weekly data, voluntariness level, and confidence in numbers.

**Path B (event-based orgs):** collected equivalent data for periodic events rather than recurring meetings.

The minimum viable recurring-meeting response, org name, first attendance, recent attendance, and meeting count, is sufficient to compute an attendance slope even without intermediate data.

### Instrument Evolution

The survey instrument was refined three times during active data collection, a deliberate tradeoff between measurement validity and consistency:

| Date | Change | Reason |
|---|---|---|
| Early March | Org name field made required | First real response revealed operational deduplication problem |
| 3/18/2026 | Q3 wording clarified | Event orgs misrouting into recurring meeting path |
| 3/30/2026 | Anonymization statement revised | Required org name contradicted anonymity framing |

### Outreach Campaign

Outreach followed a deliberate strategy of two stages:

**Stage 1 (Planting):** Initial emails sent to create awareness. No immediate conversion expected. Spring break timing was used strategically as a pre-positioning window.

The email sent for planting reads as follows:

>>>
Hello,

My name is Ian Sun, and I’m a BU student conducting a research project on attendance patterns in voluntary student organizations this semester.

Your organization is included in this study, and we’d greatly appreciate your participation.

The survey takes about 5–8 minutes and asks for high-level weekly attendance counts for the early part of the semester. No sensitive information is collected, and responses will be anonymized for analysis.

Survey link:
https://bostonu.qualtrics.com/jfe/form/SV_5cZk4dw6C5mEh9A

Thank you for your time.

Best,
Ian Sun
Boston University
>>>

**Stage 2 (Activation):** Follow-up emails sent after spring break in the same thread as the original outreach. Survey link repeated for accessibility. Follow-up timing was staggered by cohort maturation.

Additional outreach was conducted via Instagram DMs to organizations with active social media presence where personal acquaintance enabled warmer contact.

Institutional amplification via SLIC (student leadership and impact center) was attempted but declined due to university policy. All responses therefore reflect direct grassroots outreach without institutional backing.

**Outreach timeline:**

| Wave | Date | Orgs contacted |
|---|---|---|
| Probe wave | Early March | ~8 |
| Wave 2 | 3/2 to 3/4 | 18 |
| Spring break batch | 3/14 | ~100 |
| Additional batch | 3/17 | 20 |
| Follow-up wave 1 | 3/17 to 3/18 | ~100 |
| Follow-up wave 2 | 3/24 to 3/25 | ~72 |
| **Total** | | **172** |

### Response Rate

19 completed survey responses were received. 15 provided usable data for slope analysis. This represents an 8.7% usable response rate, consistent with cold survey outreach literature for academic research without incentives.

---

## Data Cleaning

### Cleaning Steps

1. Skip Qualtrics metadata rows (rows 2 and 3 of raw export)
2. Filter to `Finished == True` responses only
3. Separate recurring meeting path (`Q3 == Yes`) from event-based path (`Q3 == No`)
4. Require complete Q6 (meeting count), Q7 (first attendance), Q8 (recent attendance)
5. Fill missing org names with `(anonymous org)` for pre-instrument-fix responses
6. Retain duplicate Pre-Health Professionals Club responses as distinct meeting types (GBM vs speaker events)
7. Flag Russian Speaking Society event spike at meeting 2 (120 attendees, Valentine's Day event) and exclude from intermediate curve fitting

### Intermediate Attendance Parsing

Six organizations provided Q9 intermediate attendance data in inconsistent formats. Rather than a fragile regex parser, sequences were parsed manually into a hardcoded dictionary. With only six organizations providing this data, manual parsing provides complete auditability and eliminates the risk of silent parsing errors. 

### Handling Missing and Noisy Data

Confidence levels (Q13) were collected for every response: exact sign-in logs, estimated but close, rough estimate, or very rough estimate. These drive uncertainty bands in Visualization 1 and enable sensitivity analysis. Conclusions hold when restricted to high-confidence responses only.

---

## Feature Extraction

### Primary Feature: Attendance Slope

```python
attendance_slope = (Q8 - Q7) / Q6
```

Where Q7 = first meeting attendance, Q8 = most recent meeting attendance, Q6 = number of meetings held. Negative slope indicates decay. Positive slope indicates growth.

### Additional Features

| Feature | Column | Description |
|---|---|---|
| First attendance | Q7 | Baseline org size signal |
| Meeting count | Q6 | Controls for time in semester |
| Org category | Q2 | SAO classification |
| Voluntariness | Q12 | Structural commitment modifier |
| Confidence level | Q13 | Data quality weight |
| Percent change | derived | (Q8-Q7)/Q7 × 100, scale-invariant decay measure |

Percent change is used alongside raw slope because it is scale-invariant. A club going from 100 to 50 and a club going from 10 to 5 both show -50% regardless of absolute size.

---

## Visualizations

### Visualization 1: Attendance Trajectories

Individual attendance trajectories for all 15 recurring-meeting organizations. Solid lines connect actual observed weekly data. Dashed lines connect only first and most recent meeting, honestly representing the limit of what those organizations reported. Shaded bands encode estimation uncertainty from Q13 confidence levels: ±0% for exact counts, ±10% for estimates, ±20% for rough estimates, ±30% for very rough estimates.

### Visualization 2: Attendance Slope by Organization

Horizontal bar chart sorted most-negative to most-positive slope. Sign test result annotated directly on the plot.

### Visualization 3: Percent Change by Category

Dot plot grouping organizations by SAO category. Individual dots shown rather than means to make thin category sample sizes visually honest. Overall mean percent change (-28.7%) shown as dashed reference line.

### Visualization 4: Trajectory Shapes

Four-subplot grid showing week-by-week attendance for organizations with intermediate data. Reveals three trajectory archetypes: steep cliff then plateau (Pre-Health), smooth exponential decay (Data Science Association, Alzheimer's Buddies), and event-driven volatility (Russian Speaking Society).

---

## Modeling

### Primary Model: Binomial Sign Test

**Question answered:** Does attendance decay more often than chance predicts?

Under the null hypothesis that ADC does not exist, positive and negative slopes are equally likely (p = 0.5). We test whether the observed proportion of negative slopes significantly exceeds 0.5 using a one-sided binomial sign test. The sign test is nonparametric, makes no assumptions about slope distribution, and directly tests the primary hypothesis. With N=15 and non-normal data, it is the most appropriate primary test.

```python
from scipy.stats import binomtest
result = binomtest(n_negative, n_total, 0.5, alternative='greater')
```

### Secondary Model: Linear Regression with LOO Cross-Validation

**Question answered:** Can first-meeting attendance and meeting count predict recent attendance?

**Features:** first attendance (Q7), meeting count (Q6)
**Target:** most recent attendance (Q8)

Linear regression was chosen because it matches the complexity the data can support. Conventional rules of thumb require 10-15 observations per predictor before more flexible methods are justified. With N=15 and two predictors we are at the floor. A random forest or gradient boosting model would overfit before generalizing. Logistic regression predicts class probability rather than a continuous attendance count, making it a poor fit for this outcome variable.

**Why LOO over train-test split:** An 80/20 split yields 3 test organizations, too few for reliable evaluation. LOO trains on 14 and predicts the 15th, repeated 15 times, producing a single honest MAE from 15 held-out predictions. Every observation contributes to both training and evaluation.

---

## Results

```
Total orgs:                      15
Negative slopes (decay):         12
Positive slopes (growth):         3
Proportion decaying:           80.0%
Sign test p-value:             0.0176
Significant at α = 0.05:         YES

Mean slope:             -2.37 attendees/meeting
Median slope:           -1.43 attendees/meeting
Mean percent change:           -28.7%

LOO MAE (linear regression):   13.47 attendees
LOO MAE (predict-mean):        14.31 attendees
Improvement over baseline:        +5.9%
```

**Interpretation:** 12 of 15 voluntary student organizations showed attendance decay over the semester. The sign test confirms this imbalance is statistically significant (p = 0.0176). On average organizations lost 28.7% of their first-meeting attendance by mid-semester.

The linear regression barely beats a predict-mean baseline (+5.9%). This is the honest expected result given N=15. The model is underpowered by construction, not by design failure. The more informative output is the coefficient interpretation: the first-attendance coefficient sitting well below 1.0 confirms the decay signal in regression form.

The three growing organizations all have documented explanations for artificially suppressed first-meeting baselines: Zoom-only first meeting, room booking disruptions, and rough estimate confidence. ADC is not universal but is systematic.

---

## Limitations

### Response Bias and Survivor Bias

The responding sample is subject to systematic nonresponse bias across four mechanisms:

1. **Performance-related avoidance:** declining orgs may avoid documenting perceived leadership failure
2. **Effort bias:** orgs with formal tracking can answer more easily, skewing toward organized orgs
3. **Engagement bias:** active orgs monitor inboxes more reliably
4. **Identity/pride bias:** thriving orgs may be more motivated to share positive data

This creates survivor bias where the sample skews toward healthier orgs. Observed decay rates likely **underestimate** true population-level decay. Finding significant decay even in this optimistic sample suggests the true effect is stronger.

### Sample Size

N=15 limits generalizability and statistical power. Category-level comparisons are based on 1-3 organizations per group and should be treated as descriptive hypotheses rather than tested findings.

### Instrument Changes Mid-Collection

Three instrument changes were made during active data collection. This represents a tradeoff between measurement validity and consistency inherent to iterative survey design in live deployment. Responses collected under earlier versions are noted in the cleaning documentation.

### Selection Bias

While primary sampling was random, some organizations were selected purposively for category coverage and a small number based on prior familiarity, introducing potential bias toward larger or more active organizations.

---

## What Comes Next

With institutional backing and a SLIC partnership this study could scale significantly:

- Longitudinal tracking built into Terrier Central
- Full population coverage of all 302 eligible organizations
- Multi-semester data enabling true decay curve fitting
- Controlled intervention studies testing whether specific org practices reduce decay

The pipeline built here handles that scale. What this project demonstrates is that the signal exists and is worth chasing.

---

## Environment

- Python 3.9+
- pandas, numpy, matplotlib, scipy, scikit-learn, jupyter
- Tested on macOS and Ubuntu 24

## Contributing

Issues and suggestions welcome via GitHub Issues.

## Testing

```bash
make test
```

GitHub Actions workflow runs on every push. Tests verify CSV loading, slope computation, and sign test reproducibility.