# Modeling Assumptions

## Demonstration model

The core demonstration model is a bounded-growth system:

\[
\frac{dx}{dt}=rx\left(1-\frac{x}{K}\right)
\]

where:

- \(x(t)\) is the modeled state;
- \(r\) is the intrinsic growth rate;
- \(K\) is the carrying capacity.

## Assumptions

| Assumption | Role | Risk if false | Review action |
|---|---|---|---|
| State is nonnegative | Keeps model physically interpretable | Negative state values would be invalid | Enforce nonnegative bounds |
| Carrying capacity is fixed | Defines the upper system limit | Capacity may change over time | Add time-varying capacity scenario |
| Growth rate is constant in each scenario | Simplifies dynamics | Growth may depend on environment or policy | Add scenario or parameter uncertainty |
| System is homogeneous | Allows one aggregate state variable | Subgroup or spatial variation may matter | Extend to multi-state or spatial model |
| No external shocks | Keeps first model transparent | Shocks may dominate behavior | Add forcing terms or stochastic events |
| No observation error in simulation layer | Separates model dynamics from measurement | Calibration may be overconfident | Add measurement-error model |
