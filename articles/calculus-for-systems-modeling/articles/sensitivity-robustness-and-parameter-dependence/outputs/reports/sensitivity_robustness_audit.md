# Sensitivity and Robustness Audit

## Parameter Records
- **growth_rate** = 0.35 per time unit; range: 0.2 to 0.5; source: synthetic teaching range
- **carrying_capacity** = 100.0 state units; range: 75.0 to 125.0; source: synthetic teaching range
- **initial_stock** = 10.0 state units; range: 5.0 to 20.0; source: synthetic teaching range

## Sensitivity Records
- **growth_rate**: sensitivity 47.035039; elasticity 0.165974; status: sensitive. Conclusion may depend strongly on this parameter.
- **carrying_capacity**: sensitivity 0.982894; elasticity 0.990960; status: sensitive. Conclusion may depend strongly on this parameter.
- **initial_stock**: sensitivity 0.089309; elasticity 0.009004; status: stable. Output variation is limited across this synthetic range.

Sensitivity analysis supports model review but does not prove model validity.
