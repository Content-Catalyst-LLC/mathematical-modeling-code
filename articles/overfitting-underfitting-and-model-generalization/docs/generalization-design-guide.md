# Generalization Design Guide

## Article

**Overfitting, Underfitting, and Model Generalization**

## Central claim

Generalization is earned through evidence beyond the fitting data. A model that fits known data may still fail under new evidence, external settings, future conditions, or decision-relevant scenarios.

## Required records

| Record | Purpose |
|---|---|
| training_validation_split | Documents how fitting and assessment evidence are separated |
| overfit_gap | Compares validation error against training error |
| underfit_check | Flags high error on both training and validation evidence |
| complexity_review | Assesses whether flexibility is justified |
| regularization_review | Documents constraints used to improve transfer |
| distribution_shift | Reviews whether use conditions differ from fitting conditions |
| decision_threshold | Connects performance to action boundaries |
| use_limits | States where generalization should not be assumed |
