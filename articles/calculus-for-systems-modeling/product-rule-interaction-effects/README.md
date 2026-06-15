# The Product Rule and Interaction Effects

Companion materials for the article **“The Product Rule and Interaction Effects”** in the **Calculus for Systems Modeling** series.

Article URL: https://sustainablecatalyst.com/the-product-rule-and-interaction-effects/

## Purpose

This folder supports product-rule decomposition, interaction-effect interpretation, finite-difference diagnostics, proportional growth decomposition, and responsible use of multiplicative structures in systems models.

## Core Formula

\[
\frac{d}{dt}(a(t)b(t)) = a'(t)b(t) + a(t)b'(t)
\]

## Structure

- `python/` — product-rule decomposition, finite differences, diagnostics, exports
- `r/` — contribution tables and summary diagnostics
- `julia/` — numerical derivative checks
- `sql/` — factor observations, model runs, and decomposition outputs
- `haskell/` — typed functional decomposition model
- `rust/`, `go/`, `c/`, `cpp/`, `fortran/` — systems and numerical scaffolds
- `java/`, `typescript/` — object-oriented and platform-facing examples
- `prolog/`, `racket/` — symbolic/procedural reasoning examples
- `docs/` — modeling notes, assumptions, governance, and interpretation
- `data/` — synthetic example inputs
- `outputs/` — generated tables and figures
- `canvas/` — Catalyst Canvas-ready cards and schemas
- `tests/` — smoke-test and validation scaffolds

## Responsible Use

Product-rule decomposition describes a model structure. It does not, by itself, prove causal interaction, assign institutional responsibility, or validate a multiplicative model.
