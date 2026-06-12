# Convergence and Stability Guide

## Convergence asks

- Do results stabilize as step size decreases?
- Do residuals shrink under solver iteration?
- Do alternative methods produce similar answers?
- Does the approximation improve against a known case?

## Stability asks

- Do small numerical errors grow?
- Does a method behave badly at larger step sizes?
- Are boundary or state constraints masking numerical overshoot?
- Are results sensitive to initialization or scaling?

## Principle

A numerical output should be accompanied by diagnostic evidence. A solver completion message is not the same as model credibility.
