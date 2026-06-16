# Climate Feedback Model Audit

## Scenario Records
- **one_box_baseline** (one_box_energy_balance): final temperature at t=80.0 is 3.083. baseline forcing-feedback adjustment.
- **two_box_ocean_uptake** (two_box_energy_balance): final temperature at t=80.0 is 2.253. surface warming with deep ocean temperature 0.870.
- **carbon_cycle_feedback** (carbon_feedback): final temperature at t=80.0 is 3.469. simplified additional forcing from warming-dependent carbon feedback.
- **weak_feedback_high_sensitivity** (feedback_sweep): final temperature at t=80.0 is 4.111. weaker restoring feedback produces larger response.
- **strong_feedback_low_sensitivity** (feedback_sweep): final temperature at t=80.0 is 2.312. stronger restoring feedback produces smaller response.
- **threshold_feedback_response** (threshold_feedback): final temperature at t=80.0 is 3.895. illustrative state-dependent weakening of feedback above threshold.

## Sensitivity Records
- **equilibrium_sensitivity_to_lambda**: derivative=-2.5694. Sensitivity to feedback strength depends on sign convention and simplified model structure.

Sign convention: restoring-positive convention, C dT/dt = F - lambda T.
Climate feedback model outputs depend on forcing assumptions, feedback sign convention, heat uptake, carbon-cycle response, uncertainty, and claim boundaries.
