# Modeling Attendance Retention Dynamics in Student Organizations

## Project Description

This project investigates whether a systematic attendance decay pattern exists in voluntary student organizations at Boston University. We focus on three major categories of clubs: cultural organizations, professional development organizations, and technical/academic clubs.

Voluntary organizations are commonly believed to experience an initial spike in attendance at the beginning of the semester followed by decline and eventual stabilization. However, it is unclear whether this pattern is consistent, statistically significant, and structurally meaningful across organizations.

The primary aim of this project is to empirically test whether attendance decay is a measurable and recurring phenomenon. If such a pattern exists, we will further examine how it varies across organization types and whether early-semester attendance behavior contains sufficient signal to predict longer-term engagement outcomes.

This project will follow the full data science lifecycle, including data collection, cleaning, feature extraction, visualization, modeling, and evaluation.

## Project Goals

### Primary Goal

Determine whether a statistically significant attendance decay pattern exists across voluntary student organizations over the course of a semester.

We will measure this using:

- Estimated weekly attendance slopes
- Decay coefficients from fitted models
- Statistical tests evaluating whether average attendance change is significantly negative
- Analysis of whether stabilization (plateau formation) occurs

> This establishes whether the Attendance Decay Curve (ADC) is empirically supported or merely anecdotal.

## Secondary Goals

- Estimate attendance decay rates for each organization and compare differences across cultural, professional development, and academic clubs.
- Classify organizations into attendance trajectory categories (e.g., stable plateau, steep decline, event volatility) using early semester attendance data.
- Analyze whether event attendance spikes significantly affect long-term plateau size.
- Evaluate whether Week 1–2 attendance data can meaningfully predict Week 6 average attendance.

Evaluation metrics for predictive modeling:

- Mean Absolute Error (MAE)
- R² score

All goals are specific, measurable, and tied to quantitative outcomes.

## Data Collection Plan

### Sampling Strategy

We will use stratified random sampling to select approximately 45–60 organizations across:
- Cultural clubs
- Professional development clubs
- Technical/academic clubs

### Data to Be Collected

For each organization:
- Weekly attendance counts (Weeks 1–6 or 1–8)
- Organization category
- Meeting frequency
- Whether attendance is fully voluntary
- Whether major events occurred during specific weeks

## Collection Method

Data will be collected via survey distributed to organization leaders. Follow-up reminders will be sent to improve response rates. Attendance data will be stored in structured CSV format for analysis and anonymized for privacy purposes.

### Modeling Plan (Preliminary)

We plan to explore:
- Linear regression for predicting plateau attendance
- Nonlinear regression to estimate decay parameters
- Logistic regression or decision trees for stability classification
- K-means clustering to identify attendance trajectory 

Final model selection will depend on data characteristics.

### Evaluation Strategy
- Train-test split across organizations (e.g., 80/20 split)
- Cross-validation where appropriate
- Comparison against simple baseline models
- Analysis of failure cases and limitations

## Project Timeline

### Weeks 1–2
- Finalize sampling plan
- Identify target organizations
- Design and distribute survey

### Weeks 3–4
- Collect attendance data
- Clean and preprocess data
- Conduct exploratory analysis

### Weeks 5–6
- Extract features
- Implement baseline models
- Evaluate predictive performance

### Weeks 7–8
- Refine models
- Generate final visualizations
- Prepare final report and presentation

### Challenges anticipated
- Some respondents may provide estimated rather than precise attendance data
- Some organizations may not formally track attendance
- Finding justification and contact info can be challenging at times