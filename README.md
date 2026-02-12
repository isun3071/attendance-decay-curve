# Modeling Attendance Retention Dynamics in Student Organizations

## Project Description

This project models attendance dynamics in voluntary student organizations at Boston University. We focus on three major categories of clubs: cultural organizations, professional development organizations, and technical/academic clubs.

Voluntary organizations often experience an initial spike in attendance at the beginning of the semester followed by decline and eventual stabilization. We aim to quantify this attendance decay pattern and determine whether early-semester attendance signals can predict longer-term engagement outcomes.

This project will practice the full data science lifecycle, including data collection, cleaning, feature extraction, visualization, modeling, and evaluation.

## Project Goals

### Primary Goal

Predict Week 6 average attendance of a student organization using only Week 1–2 attendance data and structural features.

Evaluation metrics:
- Mean Absolute Error (MAE)
- R² score

> This determines whether it is even possible to predict attendance rates based on early, limited data.

Secondary Goals
- Estimate attendance decay rates for each organization and compare differences across cultural, professional development, and academic clubs.
- Classify organizations into stability categories (e.g., stable plateau vs. steep decline) using early semester attendance data.
- Analyze whether event based attendance spikes significantly impact long-term plateau size.

All goals are specific, measurable, and can be tied to quantitative outcomes.

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