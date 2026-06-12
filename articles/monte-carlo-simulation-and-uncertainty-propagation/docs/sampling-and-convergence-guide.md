# Sampling and Convergence Guide

## Sampling review

- Are input distributions justified?
- Are bounds plausible?
- Are correlations or dependence documented?
- Are random seeds recorded?
- Are enough replications used for the output metric?
- Are rare events or tails adequately sampled?
- Are sampled inputs checked against intended distributions?

## Convergence review

- Does the running mean stabilize?
- Do threshold probabilities stabilize?
- Do output quantiles stabilize?
- Do different seed streams produce similar conclusions?
- Is Monte Carlo error small enough for the decision context?

## Principle

A Monte Carlo estimate is only useful if the uncertainty model and sampling procedure are credible for the intended use.
