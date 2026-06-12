# Model Selection Design Guide

## Article

**Model Comparison and Selection**

## Central claim

Model selection is not the discovery of a universally best model. It is a documented judgment about evidence, purpose, complexity, uncertainty, interpretability, robustness, and decision relevance.

## Required records

| Record | Purpose |
|---|---|
| candidate_set | Defines models and baselines being compared |
| selection_criteria | States fit, validation, complexity, uncertainty, and decision criteria |
| comparison_table | Preserves metrics and model rankings |
| overfit_gap | Compares validation error against calibration error |
| parsimony_review | Checks whether complexity is justified |
| robustness_review | Assesses stability across assumptions |
| interpretability_review | Assesses whether users can understand the model |
| selection_audit_card | Documents why one model was preferred for a purpose |
