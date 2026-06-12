# Monte Carlo Model Register Specification

## Article

**Monte Carlo Simulation and Uncertainty Propagation**

## Central claim

A Monte Carlo model is an uncertainty propagation workflow whose credibility depends on input distributions, dependence assumptions, sampling design, random seeds, replications, output metrics, convergence diagnostics, validation, and communication of limits.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier |
| component_type | input_uncertainty, sampling_design, random_seed_protocol, output_distribution, risk_metric, convergence_diagnostic, sensitivity_diagnostic, validation_diagnostic |
| uncertainty_structure | Formal or computational uncertainty structure |
| interpretation | Plain-language meaning |
| review_question | Review question |
| status | active, review, revise, or archive |

## High-priority records

High-priority records include input distributions, joint-dependence assumptions, seed strategy, replication count, threshold metrics, output quantiles, convergence diagnostics, sensitivity diagnostics, and use-limit statements.
