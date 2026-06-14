-- Mathematical modeling in science governance schema.

DROP TABLE IF EXISTS scientific_domain_guide;
DROP TABLE IF EXISTS population_scenario;
DROP TABLE IF EXISTS scientific_model_register;
DROP TABLE IF EXISTS model_role_type;

CREATE TABLE model_role_type (
    model_role TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE scientific_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    scientific_domain TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    evidence_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_role) REFERENCES model_role_type(model_role)
);

CREATE TABLE population_scenario (
    scenario_key TEXT PRIMARY KEY,
    growth_rate REAL NOT NULL,
    carrying_capacity REAL NOT NULL,
    initial_population REAL NOT NULL,
    years INTEGER NOT NULL,
    observation_noise REAL NOT NULL
);

CREATE TABLE scientific_domain_guide (
    scientific_field TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO model_role_type VALUES
('explanation','Connects observed behavior to possible mechanism.','Mechanism is asserted without validation.'),
('prediction','Projects outcomes under specified conditions.','Forecast is communicated without uncertainty.'),
('observation','Connects measurements to model variables.','Measurement error is ignored.'),
('simulation','Explores behavior through computational runs.','Simulation is mistaken for direct observation.'),
('model_comparison','Compares plausible explanations or structures.','One model is treated as final without alternatives.'),
('uncertainty_quantification','Assesses uncertainty and sensitivity.','False precision hides uncertainty.');

INSERT INTO scientific_model_register(record_key, scientific_domain, model_role, model_family, evidence_question, status) VALUES
('mechanism_model','ecology','explanation','differential_equation','Can resource limitation explain observed slowing growth?','active'),
('forecast_model','population_science','prediction','dynamic_simulation','What range of population outcomes is plausible after ten years?','review'),
('measurement_model','field_science','observation','statistical_error_model','How does measurement noise affect interpretation?','review'),
('comparison_model','scientific_inference','model_comparison','evidence_table','Does a logistic model explain observations better than exponential growth?','review'),
('uncertainty_model','scientific_computing','uncertainty_quantification','sensitivity_analysis','Which assumptions most affect scientific conclusions?','review');

INSERT INTO population_scenario VALUES
('baseline',0.28,500.0,40.0,20,0.03),
('lower_growth',0.18,500.0,40.0,20,0.03),
('higher_growth',0.38,500.0,40.0,20,0.03),
('lower_capacity',0.28,350.0,40.0,20,0.03),
('higher_capacity',0.28,700.0,40.0,20,0.03);

INSERT INTO scientific_domain_guide VALUES
('physics','Represent laws forces energy fields and motion','Differential equations conservation laws field equations'),
('chemistry','Model reaction rates molecular interactions and equilibrium','Rate equations statistical mechanics quantum models'),
('biology','Represent growth regulation evolution and interaction','Population models gene regulation models stochastic processes'),
('ecology','Study populations food webs habitats and resilience','Dynamic systems network models spatial models'),
('earth_systems','Model climate oceans atmosphere geology and hydrology','Coupled simulations transport models geospatial models'),
('epidemiology','Represent transmission intervention and population risk','Compartmental models stochastic models agent-based models'),
('neuroscience','Model neurons networks signals and cognition','Dynamical systems network models statistical models'),
('astronomy','Infer structure motion age and composition from observations','Orbital models inverse models simulations');
