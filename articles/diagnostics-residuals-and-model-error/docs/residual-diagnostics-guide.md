# Residual Diagnostics Guide

## Article

**Diagnostics, Residuals, and Model Error**

## Central claim

Residuals are diagnostic evidence. They show how a model fails, where it fails, and whether those failures matter for interpretation or decision-making.

## Required diagnostic records

| Record | Purpose |
|---|---|
| residual_table | Preserves observed, predicted, residual, absolute error, and squared error |
| error_summary | Summarizes mean error, MAE, RMSE, median absolute error, and max error |
| bias_review | Assesses directional error |
| group_review | Assesses subgroup or scenario-specific error |
| threshold_review | Evaluates errors near decision thresholds |
| outlier_review | Flags extreme residuals |
| structural_error_review | Interprets residual patterns as possible model-form issues |
