# Boundary Register Specification

## Article

**Model Boundaries, Scale, and Scope**

## Central claim

A model boundary is not a neutral container. It determines what a model can see, what it excludes, what scale it represents, and what uses the model can support.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier for the boundary choice |
| boundary_type | physical, temporal, spatial, population, mechanism, data, or decision |
| included | What is inside the model |
| excluded | What is outside the model |
| risk_if_excluded | How exclusion could affect conclusions |
| review_question | Review prompt |
| status | active, review, revise, or archive |

## Review logic

High-priority boundary choices include those that:

- exclude likely feedback;
- omit affected groups;
- hide downstream consequences;
- rely on short time horizons;
- transfer across locations or regimes;
- create unsupported decision scope.
