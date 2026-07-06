DROP TABLE IF EXISTS linear_model_governance_registry;
DROP TABLE IF EXISTS linearity_distortion_audit_cases;

CREATE TABLE linear_model_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    modeling_role TEXT NOT NULL,
    distortion_risk TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO linear_model_governance_registry VALUES
('additivity','Additivity','Allows separate effects to be summed in one model.','Interactions or feedback can make combined effects different from the sum of individual effects.','Review interaction terms subgroup residuals and mechanism assumptions.'),
('proportionality','Proportionality','Assumes effects scale consistently with input magnitude.','Saturation thresholds scarcity or overload can change marginal effects.','Check whether the model is local global or extrapolated.'),
('coefficient_stability','Coefficient stability','Assumes relationships remain stable over the modeled range.','Regime shifts time variation policy changes or behavioral adaptation can change coefficients.','Validate across periods scenarios and operating regimes.'),
('local_approximation','Local approximation','Uses a linear model to approximate behavior near an operating point.','Local accuracy can be mistaken for global validity.','State the operating range and check approximation error.'),
('residual_diagnostics','Residual diagnostics','Uses unexplained structure as evidence about model adequacy.','Ignoring structured residuals can hide curvature thresholds or missing variables.','Inspect residual patterns before interpreting coefficients.'),
('aggregation','Aggregation and average effects','Summarizes broad structure through average relationships.','Averages can hide subgroup spatial temporal or network heterogeneity.','Review disaggregated behavior and subgroup errors.'),
('extrapolation','Extrapolation','Uses a fitted relationship outside the observed or validated range.','Predictions may cross thresholds constraints or regimes not represented in the model.','Flag out-of-range predictions and require additional validation.'),
('causal_interpretation','Causal interpretation','Interprets coefficients as effects of changing inputs.','Association can be mistaken for causal mechanism.','Separate prediction association mechanism and causal identification.');

CREATE TABLE linearity_distortion_audit_cases (
    workflow_name TEXT NOT NULL,
    model_purpose TEXT NOT NULL,
    fitted_intercept REAL NOT NULL,
    fitted_slope REAL NOT NULL,
    residual_sum_squares REAL NOT NULL,
    max_absolute_residual REAL NOT NULL,
    residual_sign_pattern TEXT NOT NULL,
    curvature_warning TEXT NOT NULL,
    extrapolation_warning TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO linearity_distortion_audit_cases VALUES
('linearity_distortion_audit','baseline_linear_approximation_for_system_behavior',0.3,2.1,0.98,0.7,'+--0+','Residuals show a structured sign pattern consistent with curvature.','Do not extrapolate beyond the observed operating range without additional validation.','Linear models clarify first-order structure but assumptions and distortion risk must be reviewed.');
