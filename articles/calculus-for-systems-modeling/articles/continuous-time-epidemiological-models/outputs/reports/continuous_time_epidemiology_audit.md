# Continuous-Time Epidemiological Model Audit

## Scenario Records
- **baseline_sir** (SIR): peak infectious=32565.21, final recovered=95316.88, reproduction number=3.200. baseline SIR scenario with susceptible depletion.
- **reduced_transmission_sir** (SIR): peak infectious=18803.07, final recovered=84364.75, reproduction number=2.200. lower transmission reduces peak infectious burden.
- **latent_period_seir** (SEIR): peak infectious=21223.15, final recovered=95220.25, reproduction number=3.200. exposed compartment delays infectious growth.
- **vaccination_reduced_susceptible** (SIR_vaccination): peak infectious=22659.12, final recovered=93068.56, reproduction number=2.720. lower susceptible share reduces effective reproduction number.

## Threshold Records
- **baseline_thresholds**: R0=3.200; susceptible threshold=0.312; herd-immunity threshold=0.688; doubling time=3.15. Thresholds are model-dependent summaries and should be presented with assumptions and context.

Epidemiological model outputs depend on compartment definitions, population boundaries, transmission assumptions, reporting processes, initial conditions, intervention mechanisms, uncertainty, and claim boundaries.
