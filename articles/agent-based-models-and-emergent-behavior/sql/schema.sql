-- Agent-based models and emergent behavior governance schema.

DROP TABLE IF EXISTS abm_component_guide;
DROP TABLE IF EXISTS abm_scenario;
DROP TABLE IF EXISTS abm_model_register;
DROP TABLE IF EXISTS abm_component_type;

CREATE TABLE abm_component_type (
    component_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE abm_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    component_type TEXT NOT NULL,
    rule_or_structure TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (component_type) REFERENCES abm_component_type(component_type)
);

CREATE TABLE abm_scenario (
    scenario TEXT PRIMARY KEY,
    agent_count INTEGER NOT NULL CHECK (agent_count > 0),
    initial_adopters INTEGER NOT NULL CHECK (initial_adopters >= 0),
    adoption_threshold_low REAL NOT NULL CHECK (adoption_threshold_low >= 0),
    adoption_threshold_high REAL NOT NULL CHECK (adoption_threshold_high <= 1),
    steps INTEGER NOT NULL CHECK (steps > 0),
    replications INTEGER NOT NULL CHECK (replications > 0)
);

CREATE TABLE abm_component_guide (
    component_type TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    example TEXT NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO abm_component_type VALUES
('agent_state','Changing agent attribute.','Agent states are oversimplified or poorly defined.'),
('behavior_rule','Rule for agent action or update.','Behavior is arbitrary or unsupported.'),
('interaction_structure','Who affects whom.','Interactions do not match the system.'),
('environment','Spatial, institutional, or resource context.','Context is treated as a generic stage.'),
('schedule','Timing and update order.','Schedule effects are ignored.'),
('simulation_protocol','Run design and replication.','Single-run storytelling replaces ensemble evidence.'),
('validation_diagnostic','Credibility check.','Patterns are not validated.'),
('emergence_diagnostic','Macro pattern summary.','Emergence is overclaimed or unexplained.');

INSERT INTO abm_model_register(record_key, component_type, rule_or_structure, interpretation, review_question, status) VALUES
('agent_state','agent_state','adopted in {0,1}','Each agent is either non-adopted or adopted','Does a binary state oversimplify adoption?','review'),
('threshold_rule','behavior_rule','adopt if adopted_neighbors_share >= threshold','Agents adopt when local social exposure exceeds their threshold','Are thresholds empirically grounded or scenario assumptions?','review'),
('ring_network','interaction_structure','two_neighbors_each_side','Agents interact in a simple local network','Does this neighborhood represent the real interaction structure?','review'),
('synchronous_update','schedule','all_agents_update_from_prior_state','All non-adopters evaluate adoption from the same prior state','Does synchronous scheduling create artificial coordination?','review'),
('ensemble_replication','simulation_protocol','multiple_random_seeds','Results are summarized across repeated runs','Are enough replications used to characterize variability?','active'),
('pattern_validation','validation_diagnostic','compare_adoption_curve_patterns','Macro outcomes should be compared against observed or theoretical patterns','Which patterns are required for credibility?','review');

INSERT INTO abm_scenario VALUES
('baseline',100,8,0.25,0.55,30,40),
('low_threshold',100,8,0.10,0.35,30,40),
('high_threshold',100,8,0.45,0.75,30,40);

INSERT INTO abm_component_guide VALUES
('agent_state','Changing agent attribute','adopted in {0,1}','Does the state represent the phenomenon?'),
('behavior_rule','Rule for agent action or update','threshold adoption','What evidence supports the rule?'),
('interaction_structure','Who affects whom','ring network','Does the interaction structure match reality?'),
('environment','Spatial or institutional context','grid or policy setting','Does context shape behavior?'),
('schedule','Timing and update order','synchronous update','Does schedule affect outcomes?'),
('simulation_protocol','Run design and replication','multiple seeds','Are replications sufficient?'),
('validation_diagnostic','Credibility check','pattern validation','Are conclusions robust?'),
('emergence_diagnostic','Macro pattern summary','adoption curve','Can the pattern be traced to rules?');
