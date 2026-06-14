-- Mathematical modeling in an age of complexity governance schema.

DROP TABLE IF EXISTS complexity_domain_guide;
DROP TABLE IF EXISTS complexity_scenario;
DROP TABLE IF EXISTS complexity_model_register;
DROP TABLE IF EXISTS complexity_feature_type;

CREATE TABLE complexity_feature_type (
    complexity_feature TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    modeling_risk TEXT NOT NULL
);

CREATE TABLE complexity_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    complexity_feature TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (complexity_feature) REFERENCES complexity_feature_type(complexity_feature)
);

CREATE TABLE complexity_scenario (
    scenario_key TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    stress_level REAL NOT NULL,
    interdependence_level REAL NOT NULL,
    uncertainty_level REAL NOT NULL,
    resilience_score REAL NOT NULL,
    equity_score REAL NOT NULL,
    adaptability_score REAL NOT NULL
);

CREATE TABLE complexity_domain_guide (
    area TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO complexity_feature_type VALUES
('feedback_loops_and_delays','Outputs return as inputs over time.','Policy resistance and delayed consequences can be missed.'),
('cascading_dependency','Failure or stress can propagate through interdependent systems.','Local risk can become systemic risk.'),
('adaptive_behavior','Actors change behavior in response to conditions and information.','Parameters may not remain stable.'),
('uncertain_future_pathways','Multiple futures remain plausible.','One forecast can create false certainty.'),
('robustness_under_uncertainty','Strategies must remain acceptable across scenarios.','Optimizing one future can create fragility.');

INSERT INTO complexity_model_register(record_key, model_role, model_family, complexity_feature, decision_context, status) VALUES
('feedback_model','dynamic_explanation','system_dynamics','feedback_loops_and_delays','understanding nonlinear policy resistance','active'),
('network_model','interdependence_analysis','network_model','cascading_dependency','identifying systemic risk and fragile bridges','review'),
('agent_model','emergence_analysis','agent_based_model','adaptive_behavior','testing heterogeneous response and emergence','review'),
('scenario_model','deep_uncertainty_review','scenario_modeling','uncertain_future_pathways','comparing plausible futures','review'),
('robustness_model','decision_support','robust_decision_analysis','robustness_under_uncertainty','choosing strategies across uncertainty','review');

INSERT INTO complexity_scenario VALUES
('baseline','Baseline stress',0.35,0.45,0.40,0.72,0.68,0.65),
('compound_shock','Compound shock',0.78,0.70,0.72,0.48,0.52,0.55),
('cascading_failure','Cascading failure',0.88,0.86,0.75,0.32,0.40,0.42),
('adaptive_pathway','Adaptive pathway',0.65,0.68,0.70,0.66,0.70,0.82);

INSERT INTO complexity_domain_guide VALUES
('feedback_dynamics','Understand loops delays accumulation and policy resistance','System dynamics stock-flow models'),
('interdependence','Map dependencies and cascading risk','Network models multilayer graphs dependency maps'),
('emergence','Explore system-level patterns from local behavior','Agent-based models cellular automata simulations'),
('deep_uncertainty','Compare plausible futures without one forecast','Scenario models exploratory modeling'),
('robust_decisions','Find strategies that remain acceptable across futures','Robust decision analysis minimax regret adaptive pathways'),
('resilience','Assess absorption recovery adaptation and transformation','Stress tests resilience metrics recovery models'),
('participation','Incorporate stakeholder knowledge and legitimacy','Participatory modeling boundary critique scenario workshops'),
('governance','Assign ownership use limits monitoring and accountability','Model registers audit trails adaptive trigger records');
