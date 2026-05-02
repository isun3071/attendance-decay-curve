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

Alternatively you can open `adc.ipynb` separately in Jupyter or Google Colab and run all cells from top to bottom to get the same results.

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

**Primary:** Do voluntary student organizations, or VSOs, at BU exhibit a measurable attendance decay pattern over the course of a semester?

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
├── bu_org_emails.txt          # the 302 orgs scraped off of Terrier Central
├── data/
│   └── responses.csv          # Qualtrics export
├── orgsscraper.py             # CampusLabs API scraper
├── randomsample.py            # Random org sampler
├── survey_link.txt            # link to the qualtrics survey used
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


> Hello,
> 
> My name is Ian Sun, and I’m a BU student conducting a research project on attendance patterns in voluntary student organizations this semester.
> 
> Your organization is included in this study, and we’d greatly appreciate your participation.
> 
> The survey takes about 5–8 minutes and asks for high-level weekly attendance counts for the early part of the semester. No sensitive information is collected, and responses will be anonymized for analysis.
> 
> Survey link:
https://bostonu.qualtrics.com/jfe/form/SV_5cZk4dw6C5mEh9A
> 
> Thank you for your time.
>
> Best, 
> 
> Ian Sun 
> 
> Boston University


**Stage 2 (Activation):** Follow-up emails sent after spring break in the same thread as the original outreach. Survey link repeated for accessibility. Follow-up timing was staggered by cohort maturation.

Additional outreach was conducted via Instagram DMs to organizations with active social media presence where personal acquaintance enabled warmer contact.

Institutional amplification via SLIC (student leadership and impact center) was attempted but declined due to university policy. All responses therefore reflect direct grassroots outreach without institutional backing.

The email sent for activation reads as follows:

> Hi,
> 
> Just following up on my earlier email about attendance patterns in student orgs at BU - I wanted to resurface this in case it got buried.
> 
> The survey takes about 5 minutes and your org's data would genuinely help the analysis.
> 
> Link is here for reference: https://bostonu.qualtrics.com/jfe/form/SV_5cZk4dw6C5mEh9A
> 
> Thanks so much, 
> 
> Ian Sun

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
5. Fill missing org names with `(anonymous org)` for responses before the first name fix
6. Retain duplicate Pre-Health Professionals Club responses as distinct meeting types (GBM vs speaker events)
7. Flag Russian Speaking Society event spike at meeting 2 (120 attendees, Valentine's Day event) and exclude from intermediate curve fitting

### Intermediate Attendance Parsing

Six organizations provided Q9 intermediate attendance data in inconsistent formats. Rather than a fragile regex parser, sequences were parsed manually into a hardcoded dictionary. With only six organizations providing this data, manual parsing provides complete auditability and eliminates the risk of silent parsing errors. As this dataset gets larger, however, a regex or NLP parser may be needed, with the help of an LLM if necessary.

### Handling Missing and Noisy Data

Confidence levels (Q13) were collected for every response: exact sign-in logs, estimated but close, rough estimate, or very rough estimate. These drive uncertainty bands in Visualization 1 and enable sensitivity analysis. The decision to collect confidence levels was motivated by the fact that VSO leaders (eboard) may not be 100% sure of their attendance; they may only be estimating based on spotty headcount, not collect or fully trust attendance collection via QR codes, and as a result, Q13 was added to account for estimation error on the eboard's part.

---

## Feature Extraction

### Primary Feature: Attendance Slope

```python
attendance_slope = (Q8 - Q7) / Q6
```

Where Q7 = first meeting attendance, Q8 = most recent meeting attendance, Q6 = number of meetings held. A negative slope indicates decay. A positive slope indicates growth.

### Additional Features

| Feature | Column | Description |
|---|---|---|
| First attendance | Q7 | Baseline org size signal |
| Meeting count | Q6 | Controls for time in semester |
| Org category | Q2 | SAO classification |
| Voluntariness | Q12 | Structural commitment modifier |
| Confidence level | Q13 | Data quality weight and uncertainty band source |
| Percent change | derived | (Q8-Q7)/Q7 × 100, scale-invariant decay measure |
| Slope envelope | derived | Worst-case slope bounds from Q13 confidence band |
| Band fraction | derived | Numeric uncertainty fraction per org from Q13 |

Percent change is used alongside raw slope because it is scale-invariant. A club going from 100 to 50 and a club going from 10 to 5 both show -50% regardless of absolute size.

The confidence band fraction is derived from Q13 and propagates through every downstream visualization and statistical test as an uncertainty envelope:

| Q13 Response | Band Fraction |
|---|---|
| Exact counts from sign-in logs | ±0% |
| Estimated but close | ±10% |
| Rough estimate | ±20% |
| Very rough estimate | ±30% |

These fractions were chosen to reflect realistic estimation error: exact sign-in logs carry no assumed error, while a rough headcount estimate in a large room plausibly varies by ±20%.

---

## Visualizations

### Visualization 1: Attendance Trajectories

Individual attendance trajectories for all 15 VSOs with recurring meetings. Solid lines connect actual observed weekly data. Dashed lines connect only first and most recent meeting, honestly representing the limit of what those organizations reported. Shaded bands encode estimation uncertainty from Q13 confidence levels. The same confidence bands defined above apply here as visual envelopes around each trajectory.

### Visualization 2: Attendance Slope by Organization

Horizontal bar chart sorted most-negative to most-positive slope. Red bars indicate decay, green indicate growth. Whisker-style error bars on each bar show the worst-case slope envelope under each org's Q13 confidence band. Sign test result annotated directly on the plot.

### Visualization 3: Percent Change by Organization Category

Dot plot grouping organizations by SAO category. Individual dots shown rather than means to make thin category sample sizes visually honest. Horizontal error bars show asymmetric percent-change envelope under each org's Q13 band. Overall mean percent change (-28.7%) shown as dashed reference line. Category-level average bars are shown without error calibration due to thin subgroup N.

### Visualization 4: Trajectory Shapes (Intermediate Data)

Four-subplot grid showing week-by-week attendance for organizations with intermediate data. Shaded bands propagate the same Q13 confidence envelopes as Visualization 1. Reveals three trajectory archetypes: steep cliff then plateau (Pre-Health Professionals Club), smooth exponential decay (Data Science Association, Alzheimer's Buddies at BU), and event-driven volatility (Russian Speaking Society, whose meeting 2 spike of 120 reflects a Valentine's Day event excluded from curve fitting).

---

## Modeling

### Primary Model: Binomial Sign Test

**Question answered:** Does attendance decay more often than chance predicts?

Under the null hypothesis that ADC does not exist, positive and negative slopes are equally likely (p = 0.5). We test whether the observed proportion of negative slopes significantly exceeds 0.5 using a one-sided binomial sign test. The sign test is nonparametric, makes no assumptions about slope distribution, and directly tests the primary hypothesis. With N=15 and non-normal data from VSO leaders, it is the most appropriate primary test.

```python
from scipy.stats import binomtest
result = binomtest(n_negative, n_total, 0.5, alternative='greater')
```

A **confidence-aware variant** was also run as a robustness check. An org is classified as "confidently decaying" only if the upper bound of its slope envelope (from Q13 band) is still below zero, and "confidently growing" only if the lower bound is still above zero. Orgs whose slope envelope straddles zero are treated as directionally ambiguous. The sign test is then re-run on only the unambiguous orgs.

### Secondary Model: Linear Regression with LOO Cross-Validation

**Question answered:** Can first-meeting attendance and meeting count predict recent attendance?

**Features:** first attendance (Q7), meeting count (Q6)
**Target:** most recent attendance (Q8)

Linear regression was chosen because it matches the complexity the data can support. Conventional rules of thumb require 10-15 observations per predictor before more flexible methods are justified. With N=15 and two predictors we are at the floor. A random forest or gradient boosting model would overfit before generalizing. Logistic regression predicts class probability rather than a continuous attendance count, making it a poor fit for this outcome variable.

**Why LOO over train-test split:** An 80/20 split yields 3 test organizations, too few for reliable evaluation. LOO trains on 14 and predicts the 15th, repeated 15 times, producing a single honest MAE from 15 held-out predictions. Every observation contributes to both training and evaluation.

Three regression variants were run as robustness checks:

1. **Unweighted LOO regression** on point-estimate attendance values
2. **Confidence-weighted LOO regression** using inverse-precision weights derived from Q13 band fractions (weight = 1 / (band_frac + 0.05)), upweighting high-confidence responses
3. **Monte Carlo bootstrap** (N=1000) resampling Q7 and Q8 uniformly within each org's Q13 confidence band, refitting the full LOO regression each iteration, producing 95% bootstrap intervals on MAE and coefficients

---

## Results

```
=== Sign Test ===
Total orgs:                                15
Negative slopes (decay):                   12
Positive slopes (growth):                   3
Proportion decaying:                     80.0%
Point-estimate sign test p-value:        0.0176  ← significant at α = 0.05

Confidence-aware sign test:
  Confidently decaying (envelope below 0):   10
  Confidently growing  (envelope above 0):    2
  Directionally ambiguous:                    3
  Sign test on 12 unambiguous orgs:  p = 0.0193  ← still significant at α = 0.05

=== Descriptive Statistics ===
Mean slope:                       -2.37 attendees/meeting
Median slope:                     -1.43 attendees/meeting
Mean percent change:                        -28.7%

=== Linear Regression ===
LOO MAE (unweighted):             13.47 attendees
LOO MAE (confidence-weighted):    13.51 attendees
LOO MAE (predict-mean baseline):  14.31 attendees
Improvement over baseline:              +5.9%

Bootstrap (N=1000) 95% intervals:
  LOO MAE:                        11.68 – 15.19 attendees
  First attendance coefficient:   +0.321 – +0.471
  Meeting count coefficient:      +0.004 – +1.373
```

**Interpretation:** 12 of 15 VSOs showed attendance decay over the semester. The sign test confirms this imbalance is statistically significant (p = 0.0176), and the result holds when restricted to the 10 organizations whose decay direction is unambiguous within their reported confidence bands (p = 0.0193). On average, organizations lost 28.7% of their first-meeting attendance by mid-semester.

The linear regression barely beats a predict-mean baseline (+5.9%). This is the honest expected result given N=15: the model is underpowered by construction, not by design failure. The more informative output is the coefficient interpretation. The first-attendance coefficient sits well below 1.0 across all three regression variants and across all 1000 bootstrap samples (+0.321 to +0.471), confirming the decay signal in regression form: organizations retain only a fraction of their starting attendance. The positive meeting-count coefficient reflects a cross-sectional confound where more institutionally established organizations appear in later weeks, not a contradiction of the hypothesis.

The three growing organizations all have documented explanations for artificially suppressed first-meeting baselines: Zoom-only first meeting (Environmental Student Organization), room booking disruptions causing short-notice announcements (SciBU), and rough estimate confidence on gentle growth (Society of Asian Scientists and Engineers). ADC is not universal, but it is systematic.

---

## Limitations

### Response Bias and Survivor Bias

The responding sample is subject to systematic nonresponse bias across four mechanisms:

1. **Performance-related avoidance:** organizations experiencing significant attendance decline may be less likely to participate due to the social and emotional costs of documenting perceived leadership failure
2. **Effort bias:** organizations with formal attendance tracking can answer the survey more easily, skewing the sample toward more organized orgs
3. **Engagement bias:** active organizations monitor inboxes more reliably than declining ones
4. **Identity/pride bias:** thriving organizations may be more motivated to share positive data

This creates a **survivor bias** where the responding sample skews toward organizationally healthier orgs. Observed decay rates likely **underestimate** true population-level decay. Finding statistically significant decay even in this optimistic sample suggests the true population effect is stronger, not weaker.

### Sample Size

N=15 limits generalizability and statistical power. Category-level comparisons are based on 1-3 organizations per group and should be treated as descriptive hypotheses for future research rather than tested findings.

### Instrument Changes Mid-Collection

Three instrument changes were made during active data collection. This represents a deliberate tradeoff between measurement validity and consistency inherent to iterative survey design in live deployment. Responses collected under earlier instrument versions are noted in the cleaning documentation.

### Selection Bias in Sampling

While primary sampling was random, some organizations were selected purposively for category coverage and a small number based on prior familiarity, introducing potential bias toward larger or more active organizations.

### Confidence Band Assumptions

The ±10%, ±20%, ±30% uncertainty band widths assigned to Q13 confidence tiers are principled estimates rather than empirically validated measurement error parameters. Sensitivity analyses show findings hold across reasonable alternative assumptions, but the exact band widths affect the width of uncertainty envelopes in all visualizations.

---

## What Comes Next

With institutional backing and a SLIC partnership this study could scale significantly:

- Longitudinal tracking built into Terrier Central attendance infrastructure
- Full population coverage of all 302 eligible organizations
- Multi-semester data enabling true decay curve fitting and half-life estimation
- Controlled intervention studies testing whether specific org practices reduce decay
- Formal stratified sampling with pre-registered hypotheses

The pipeline built here handles that scale. What this project demonstrates is that the signal exists and is worth chasing.

---

## Environment

- Python 3.9+
- pandas, numpy, matplotlib, scipy, scikit-learn, jupyter, nbconvert
- Tested on macOS and Ubuntu 24

## Contributing

Issues and suggestions welcome via GitHub Issues.

## Testing

```bash
make test
```

GitHub Actions workflow runs on every push. Tests verify CSV loading, slope computation, sign test reproducibility, and intermediate data dictionary integrity.