# Model Purpose Register Specification

## Article

**Model Purpose: Explanation, Prediction, Control, and Decision Support**

## Central claim

A model’s purpose determines its appropriate design, validation standard, uncertainty format, communication strategy, and responsible-use limits.

## Required fields

| Field | Purpose |
|---|---|
| purpose | Explanation, prediction, control, decision support, simulation, or optimization |
| primary_question | The question the model is designed to answer |
| design_emphasis | The modeling features required by the purpose |
| validation_standard | What evidence supports this use |
| uncertainty_format | How uncertainty should be communicated |
| misuse_risk | How the model may drift or be misused |
| supported_use_status | supported, exploratory, review, revise, or prohibited |

## Review logic

High-priority purpose risks include:

- prediction interpreted as explanation;
- scenario exploration interpreted as forecast;
- decision support used as decision substitution;
- optimization objective treated as complete value system;
- control action used without monitoring or fail-safes;
- model used outside validation domain.
