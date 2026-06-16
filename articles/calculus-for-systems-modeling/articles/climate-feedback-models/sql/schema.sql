DROP TABLE IF EXISTS climate_feedback_governance_registry;
DROP TABLE IF EXISTS climate_feedback_parameter_records;
DROP TABLE IF EXISTS climate_feedback_scenario_records;

CREATE TABLE climate_feedback_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO climate_feedback_governance_registry VALUES
('state_variables','State variables','Defines temperature anomaly, carbon stock, ocean heat content, albedo state, or regional field.','Makes the modeled climate response explicit.','Climate feedback outputs cannot be interpreted responsibly if state variables are unclear.'),
('forcing_record','Forcing record','Documents greenhouse gas, aerosol, land-use, solar, volcanic, and scenario assumptions.','Separates physical forcing from feedback response.','Scenario assumptions should not be presented as predictions.'),
('feedback_record','Feedback record','Documents Planck, water vapor, lapse-rate, cloud, albedo, carbon-cycle, and ocean feedback assumptions.','Connects feedback parameters to mechanisms.','Net feedback values can hide component uncertainty.'),
('sign_convention','Sign convention','Documents whether feedbacks use restoring-positive or climate-feedback sign conventions.','Prevents interpretation errors.','Feedback signs must be stated before comparing parameters.'),
('time_scale_record','Time-scale record','Documents heat capacity, ocean uptake, transient response, and equilibrium response.','Distinguishes near-term response from long-term adjustment.','Equilibrium response should not be confused with near-term forecast.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, exploration, sensitivity analysis, scenario comparison, or decision support.','Prevents overclaiming and scope drift.','Climate feedback conclusions should not exceed evidence, assumptions, uncertainty, and tested scope.');

CREATE TABLE climate_feedback_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO climate_feedback_parameter_records VALUES
('F',3.7,'W m^-2','simplified forcing from doubled carbon dioxide','Forcing depends on forcing agent and scenario.');
INSERT INTO climate_feedback_parameter_records VALUES
('lambda',1.2,'W m^-2 K^-1','net restoring feedback strength using restoring-positive convention','Feedback sign convention must be documented.');
INSERT INTO climate_feedback_parameter_records VALUES
('C',8.0,'W yr m^-2 K^-1','effective surface heat capacity','Heat capacity summarizes ocean and atmosphere response.');
INSERT INTO climate_feedback_parameter_records VALUES
('kappa',0.7,'W m^-2 K^-1','surface-to-deep-ocean heat exchange','Ocean uptake controls transient response.');
INSERT INTO climate_feedback_parameter_records VALUES
('beta_carbon',0.15,'W m^-2 K^-1','simplified carbon-cycle feedback forcing per degree','Carbon-cycle feedback is process-dependent and uncertain.');

CREATE TABLE climate_feedback_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO climate_feedback_scenario_records VALUES
('one_box_baseline','one_box_energy_balance','baseline forcing-feedback adjustment','Simple model clarifies structure but is not a complete Earth-system model.');
INSERT INTO climate_feedback_scenario_records VALUES
('two_box_ocean_uptake','two_box_energy_balance','surface warming with deep-ocean heat uptake','Ocean uptake controls transient response.');
INSERT INTO climate_feedback_scenario_records VALUES
('carbon_cycle_feedback','carbon_feedback','additional forcing from warming-dependent carbon feedback','Carbon-cycle feedback is process-dependent and uncertain.');
INSERT INTO climate_feedback_scenario_records VALUES
('weak_feedback_high_sensitivity','feedback_sweep','weaker restoring feedback produces larger response','Feedback sign convention and uncertainty must be documented.');
INSERT INTO climate_feedback_scenario_records VALUES
('threshold_feedback_response','threshold_feedback','state-dependent weakening of feedback above threshold','Threshold values require process-specific evidence.');
