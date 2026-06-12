# Assumption Register Specification

## Article

**Assumptions, Simplification, and Model Design**

## Central claim

Assumptions are not afterthoughts. They are load-bearing elements of model architecture. A professional model should track assumptions, classify their role, identify risks if false, define sensitivity tests, and record review status.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier for the assumption |
| statement | Plain-language assumption |
| assumption_type | Boundary, scale, functional, parameter, uncertainty, computational, or interpretive |
| role | Why the assumption exists |
| risk_if_false | What could break if the assumption fails |
| sensitivity_test | How the assumption should be tested |
| review_status | active, review, revise, or archive |

## Review logic

High-priority assumptions include those that:

- strongly affect outputs;
- are weakly supported by evidence;
- hide important mechanisms;
- affect safety, equity, or public decisions;
- cannot be validated with current data;
- are used outside their original domain.
