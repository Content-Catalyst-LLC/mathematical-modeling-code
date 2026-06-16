# Responsible Mathematical Modeling Audit

## Purpose Records
- **synthetic_logistic_growth** (teaching): supports illustrates growth, saturation, and carrying capacity; does not support empirical forecast for a real population. Synthetic teaching models should not be communicated as empirical evidence.
- **scenario_sweep** (exploratory): supports compares behavior across plausible parameter scenarios; does not support single-point prediction. Scenario outputs should not be confused with forecasts.
- **decision_support_model** (decision support): supports frames tradeoffs under documented assumptions; does not support replacement for judgment or accountability. Models inform decisions; they do not remove responsibility from decision makers.

## Assumption Records
- **continuous_growth** (mathematical): state changes continuously over modeled time. Evidence: teaching assumption. Risk if hidden: smooth model may hide shocks, thresholds, or discrete events.
- **fixed_parameter_values** (empirical): parameters remain fixed across the scenario. Evidence: synthetic assumption. Risk if hidden: output appears more certain than parameter evidence supports.
- **solver_configuration** (computational): numerical method and tolerance are adequate for the model. Evidence: requires diagnostic record. Risk if hidden: numerical artifact may appear as model insight.
- **objective_function_weights** (normative): optimization weights reflect a chosen priority structure. Evidence: requires stakeholder and governance review. Risk if hidden: value judgments are hidden inside mathematics.

## Claim Boundary Records
- **descriptive**: permitted: the model summarizes a specified structure or dataset; prohibited: the model proves a mechanism; status: active.
- **mechanistic**: permitted: the model represents a plausible process under stated assumptions; prohibited: the mechanism is proven solely by formal structure; status: review.
- **predictive**: permitted: the model forecasts within validated domain and time horizon; prohibited: the model predicts outside validation scope; status: review.
- **decision_support**: permitted: the model frames tradeoffs under documented assumptions; prohibited: the model replaces judgment or accountability; status: review.

Mathematical modeling is responsible only when purpose, assumptions, evidence, uncertainty, and claim boundaries are documented.
