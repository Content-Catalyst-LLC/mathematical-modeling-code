# Numerical Method Register Specification

## Article

**Numerical Methods for Mathematical Models**

## Central claim

A numerical method is an algorithmic approximation whose credibility depends on method choice, step size, tolerance, discretization, implementation, convergence, stability, and validation.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier |
| component_type | time_step_method, discretization, solver_tolerance, convergence_diagnostic, stability_diagnostic, state_constraint, validation_diagnostic |
| numerical_structure | Formal or computational structure |
| interpretation | Plain-language meaning |
| review_question | Review question |
| status | active, review, revise, or archive |

## High-priority records

High-priority records include method family, solver tolerance, step size, grid resolution, convergence diagnostics, stability checks, residual checks, state constraints, and model-use limits.
