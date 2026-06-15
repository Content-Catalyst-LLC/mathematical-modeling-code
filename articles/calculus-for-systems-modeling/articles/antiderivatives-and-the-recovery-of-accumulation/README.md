# Antiderivatives and the Recovery of Accumulation

Companion code and reproducible workflows for **Antiderivatives and the Recovery of Accumulation** in the **Calculus for Systems Modeling** series.

## Themes

- antiderivatives as rate-to-quantity recovery;
- constants of integration and baseline state;
- initial conditions;
- flow-to-stock reasoning;
- marginal-to-total reasoning;
- unit consistency;
- symbolic versus numerical recovery;
- trapezoidal accumulation;
- reconstruction from rate data;
- missing-flow warnings;
- generated Markdown/JSON audit reports.

## Run

```bash
make smoke
make advanced
make all
```

## Principle

An accumulated quantity recovered from a rate should state the rate definition, interval, integration variable, initial condition, units, numerical method, and missing-flow assumptions.
