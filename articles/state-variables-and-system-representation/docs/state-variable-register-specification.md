# State Variable Register Specification

## Article

**State Variables and System Representation**

## Central claim

State variables are not just model variables. They define what the system remembers, updates, observes, and uses to determine future behavior.

## Required fields

| Field | Purpose |
|---|---|
| key | Stable identifier |
| state_type | continuous stock, adaptive state, latent condition, derived output, etc. |
| unit | Unit or measurement scale |
| interpretation | Plain-language meaning |
| update_role | How the quantity changes or is derived |
| observability | directly observed, partially observed, proxy observed, hidden |
| review_question | Question for state adequacy review |
| status | active, review, revise, or archive |

## High-priority state records

High-priority records include latent states, proxy states, adaptive states, hidden condition variables, backlog variables, cumulative exposure, and any state that is necessary for feedback or control.
