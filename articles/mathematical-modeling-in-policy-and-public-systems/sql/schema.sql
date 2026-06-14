-- Mathematical modeling in policy and public systems governance schema.

DROP TABLE IF EXISTS policy_domain_guide;
DROP TABLE IF EXISTS policy_option;
DROP TABLE IF EXISTS policy_model_register;
DROP TABLE IF EXISTS policy_model_role_type;

CREATE TABLE policy_model_role_type (
    model_role TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE policy_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    policy_domain TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    public_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_role) REFERENCES policy_model_role_type(model_role)
);

CREATE TABLE policy_option (
    option_key TEXT PRIMARY KEY,
    option_name TEXT NOT NULL,
    projected_benefit REAL NOT NULL,
    total_cost REAL NOT NULL,
    implementation_feasibility REAL NOT NULL,
    equity_score REAL NOT NULL,
    uncertainty_width REAL NOT NULL,
    public_risk REAL NOT NULL
);

CREATE TABLE policy_domain_guide (
    policy_area TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO policy_model_role_type VALUES
('problem_framing','Clarifies public problem drivers, boundaries, and affected systems.','Boundary choices are hidden or treated as neutral.'),
('forecasting','Projects demand, risk, or pressure under future conditions.','Forecast is communicated as certainty.'),
('option_comparison','Compares policy alternatives under objectives and constraints.','Model-selected option is treated as automatically legitimate.'),
('distributional_review','Reviews benefits and burdens across groups or places.','Average outcomes hide inequity.'),
('model_governance','Documents ownership, approved use, update process, and challenge pathway.','Accountability shifts from institution to model.'),
('public_communication','Communicates model role, uncertainty, and use limits.','Public trust is damaged by opacity or false precision.');

INSERT INTO policy_model_register(record_key, policy_domain, model_role, model_family, public_question, status) VALUES
('problem_model','public_systems','problem_framing','systems_map','What drivers and boundaries define the public problem?','active'),
('forecast_model','public_planning','forecasting','scenario_forecast','What demand or risk is plausible under future conditions?','review'),
('allocation_model','resource_allocation','option_comparison','constrained_decision_model','Which option balances benefit cost feasibility and equity?','review'),
('equity_model','public_accountability','distributional_review','equity_diagnostic','How are benefits and burdens distributed across groups or places?','review'),
('governance_model','institutional_governance','model_governance','review_register','Who owns the model decision update process and public challenge pathway?','review');

INSERT INTO policy_option VALUES
('baseline','Maintain current services',42.0,18.0,0.86,0.52,18.0,0.42),
('targeted_prevention','Targeted prevention program',68.0,32.0,0.74,0.78,22.0,0.30),
('broad_expansion','Broad service expansion',81.0,49.0,0.58,0.69,28.0,0.34),
('adaptive_pathway','Adaptive pathway with monitoring triggers',73.0,38.0,0.70,0.82,16.0,0.24);

INSERT INTO policy_domain_guide VALUES
('public_health','Transmission demand resource allocation and intervention timing','Compartmental models forecasts optimization agent-based models'),
('infrastructure','Planning reliability maintenance and failure risk','Network models reliability models lifecycle simulations'),
('environmental_management','Risk adaptation emissions land water and ecosystem policy','Scenario models system dynamics spatial models'),
('housing_and_urban_policy','Need affordability mobility and land-use effects','Forecasting optimization spatial analysis'),
('transportation','Capacity ridership congestion access and safety','Network models simulation optimization'),
('social_programs','Eligibility demand service access and program impact','Impact evaluation queueing models allocation models'),
('emergency_management','Preparedness response capacity and cascading risk','Scenario models logistics models stress tests'),
('regulation','Risk thresholds compliance monitoring and public consequence','Risk models cost-benefit models decision analysis');
