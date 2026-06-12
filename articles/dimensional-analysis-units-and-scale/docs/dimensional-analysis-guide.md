# Dimensional Analysis Guide

## Core checks

- Do both sides of every equation share the same dimensions?
- Are stocks and flows connected through a time step?
- Are rates expressed per correct time unit?
- Are probabilities in [0, 1]?
- Are logarithms and exponentials dimensionless?
- Are units documented in data, code, tables, figures, and outputs?

## Common failures

- adding a flow directly to a stock;
- using annual rates in daily models;
- mixing meters and kilometers;
- confusing percentage and proportion;
- taking logs of dimensional quantities without normalization;
- interpreting normalized coefficients as original-unit effects.
