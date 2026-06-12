# Formal Statement Register Specification

## Article

**Equations, Inequalities, and Model Logic**

## Central claim

Equations, inequalities, domains, feasible sets, and conditional logic are not merely notation. They define what the model claims must hold, what is bounded, what is feasible, and how the model reasons.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier |
| statement_type | equation, inequality, domain_rule, definition, conditional_logic, objective_rule, or transformation_rule |
| expression | Formal expression or logic rule |
| interpretation | Plain-language meaning |
| domain_or_condition | Domain, condition, regime, or validity rule |
| review_question | Question for formal review |
| status | active, review, revise, or archive |

## Review logic

High-priority statements include those that:

- enforce constraints;
- define thresholds;
- use max/min clipping;
- depend on transformations;
- hide policy logic;
- affect feasibility;
- shape optimization;
- determine final model outputs.
