# Optimization Model Register Specification

## Article

**Optimization Models and Objective Functions**

## Central claim

An optimization model is a structured decision-support object: it defines what can be chosen, what is optimized, what must be constrained, and how solutions should be interpreted.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier |
| component_type | decision variable, objective function, constraint, parameter, feasible region, solver setting, validation diagnostic |
| expression | Mathematical or computational expression |
| interpretation | Plain-language meaning |
| review_question | Review question |
| status | active, review, revise, or archive |

## High-priority records

High-priority records include objective functions, ethical or operational constraints, feasibility assumptions, integer restrictions, solver settings, weights, and outputs used for decision support.
