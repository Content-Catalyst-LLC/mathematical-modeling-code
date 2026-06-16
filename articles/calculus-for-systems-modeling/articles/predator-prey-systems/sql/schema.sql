DROP TABLE IF EXISTS predator_prey_governance_registry;
DROP TABLE IF EXISTS predator_prey_parameter_records;
DROP TABLE IF EXISTS predator_prey_scenario_records;
DROP TABLE IF EXISTS predator_prey_nullcline_records;

CREATE TABLE predator_prey_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO predator_prey_governance_registry VALUES
('state_variables','State variables','Defines prey and predator populations, units, boundaries, and measurement status.','Makes the coupled system interpretable.','Predator-prey equations cannot be interpreted responsibly if population definitions are unclear.'),
('interaction_term','Interaction term','Documents whether predation is mass-action, saturating, spatial, seasonal, or behavior-dependent.','Connects mathematical coupling to mechanism.','The product xy is an assumption, not universal evidence of encounter dynamics.'),
('functional_response','Functional response','Documents Type I, Type II, Type III, or other predation response structure.','Determines how predation changes with prey abundance.','The wrong functional response can change stability and persistence conclusions.'),
('equilibrium_record','Equilibrium record','Documents coexistence, extinction, nullclines, Jacobian, and local stability.','Connects phase-plane analysis to interpretation.','Equilibrium is a mathematical condition, not a full ecological conclusion.'),
('calibration_record','Calibration record','Documents data source, fitting method, uncertainty, identifiability, and validation status.','Separates curve fit from mechanism.','A fitted cycle does not automatically prove predator-prey causality.'),
('claim_boundary','Claim boundary','Defines whether the predator-prey model supports teaching, exploration, mechanism, prediction, management, or decision support.','Prevents overclaiming and scope drift.','Predator-prey conclusions should not exceed evidence, assumptions, and tested scope.');

CREATE TABLE predator_prey_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO predator_prey_parameter_records VALUES
('alpha',0.6,'per year','prey intrinsic growth rate','Prey growth may be resource-limited rather than exponential.');
INSERT INTO predator_prey_parameter_records VALUES
('beta',0.02,'encounter coefficient','predation interaction coefficient','Mass-action encounters may overstate interaction in spatial systems.');
INSERT INTO predator_prey_parameter_records VALUES
('gamma',0.5,'per year','predator mortality rate','Mortality may vary by age, season, or environment.');
INSERT INTO predator_prey_parameter_records VALUES
('delta',0.01,'conversion coefficient','conversion from prey encounters to predator growth','Conversion efficiency should not be treated as mechanism without evidence.');
INSERT INTO predator_prey_parameter_records VALUES
('K',500.0,'prey units','prey carrying capacity','Carrying capacity is assumption-bearing and may change over time.');
INSERT INTO predator_prey_parameter_records VALUES
('h',0.08,'time per prey','handling time','Saturation claims require evidence for functional response.');

CREATE TABLE predator_prey_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO predator_prey_scenario_records VALUES
('classic_lotka_volterra','lotka_volterra','baseline mass-action predator-prey interaction','Modeled cycles depend on ideal assumptions.');
INSERT INTO predator_prey_scenario_records VALUES
('logistic_prey_limit','logistic_prey','prey growth limited by carrying capacity','Prey cannot grow indefinitely without predators.');
INSERT INTO predator_prey_scenario_records VALUES
('type_ii_functional_response','saturating_predation','predation saturates due to handling time','Functional response choice changes stability.');
INSERT INTO predator_prey_scenario_records VALUES
('harvesting_pressure','harvesting','external removal shifts dynamics and risk','Management terms require governance review.');
INSERT INTO predator_prey_scenario_records VALUES
('stochastic_lotka_volterra_path','stochastic','one stochastic path under environmental variability','A single stochastic path is not a distribution.');

CREATE TABLE predator_prey_nullcline_records (
    nullcline_name TEXT PRIMARY KEY,
    equation TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO predator_prey_nullcline_records VALUES
('prey_nullcline','dx/dt = 0 -> x = 0 or y = alpha / beta','Prey stop changing when predator abundance balances prey growth.','The nullcline depends on mass-action assumptions.');
INSERT INTO predator_prey_nullcline_records VALUES
('predator_nullcline','dy/dt = 0 -> y = 0 or x = gamma / delta','Predators stop changing when prey abundance balances mortality.','The nullcline depends on conversion and mortality assumptions.');
INSERT INTO predator_prey_nullcline_records VALUES
('coexistence_equilibrium','(x*, y*) = (gamma/delta, alpha/beta)','Coexistence occurs where both populations have zero instantaneous growth.','Equilibrium is a mathematical condition, not a full ecological conclusion.');
