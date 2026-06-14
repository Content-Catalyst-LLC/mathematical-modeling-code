-- Mathematical modeling in engineering governance schema.

DROP TABLE IF EXISTS engineering_domain_guide;
DROP TABLE IF EXISTS beam_design;
DROP TABLE IF EXISTS engineering_model_register;
DROP TABLE IF EXISTS engineering_model_role_type;

CREATE TABLE engineering_model_role_type (
    model_role TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE engineering_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    engineering_domain TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    design_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_role) REFERENCES engineering_model_role_type(model_role)
);

CREATE TABLE beam_design (
    design_key TEXT PRIMARY KEY,
    width_m REAL NOT NULL,
    height_m REAL NOT NULL,
    span_m REAL NOT NULL,
    load_n REAL NOT NULL,
    allowable_stress_pa REAL NOT NULL,
    material_density_kg_m3 REAL NOT NULL
);

CREATE TABLE engineering_domain_guide (
    engineering_field TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO engineering_model_role_type VALUES
('initial_design','Rough sizing and feasibility analysis.','Conceptual model is mistaken for validated design evidence.'),
('safety_review','Safety margins, constraints, and failure mode review.','Expected performance is checked without failure analysis.'),
('tradeoff_analysis','Objective and constraint comparison across design alternatives.','Optimization hides safety or value tradeoffs.'),
('uncertainty_review','Sensitivity, tolerance, and robustness assessment.','Baseline assumptions are treated as certain.'),
('validation','Testing and comparison with evidence.','Simulation is treated as field validation.');

INSERT INTO engineering_model_register(record_key, engineering_domain, model_role, model_family, design_question, status) VALUES
('sizing_model','structural_engineering','initial_design','algebraic_design_model','What beam dimensions are feasible under baseline load?','active'),
('safety_model','structural_engineering','safety_review','limit_state_model','Does the design maintain positive stress margin?','review'),
('optimization_model','engineering_design','tradeoff_analysis','constrained_optimization','Which design balances weight and safety margin?','review'),
('uncertainty_model','reliability_engineering','uncertainty_review','sensitivity_analysis','Which assumptions most affect safety margin?','review'),
('validation_model','engineering_testing','validation','test_comparison','What test evidence is needed before use?','review');

INSERT INTO beam_design VALUES
('light_design',0.08,0.16,3.0,4200.0,145000000.0,7850.0),
('balanced_design',0.10,0.18,3.0,4200.0,145000000.0,7850.0),
('stiff_design',0.12,0.22,3.0,4200.0,145000000.0,7850.0),
('overloaded_case',0.10,0.18,3.0,7000.0,145000000.0,7850.0);

INSERT INTO engineering_domain_guide VALUES
('civil_engineering','Structures soils water systems transportation and infrastructure risk','Structural models hydrologic models network models'),
('mechanical_engineering','Motion stress heat vibration machines and manufacturing','Dynamics finite element models thermal models'),
('electrical_engineering','Circuits signals power systems communication and control','Circuit models signal models network flow control systems'),
('chemical_engineering','Reaction systems transport process design and safety','Mass balance reaction kinetics process simulations'),
('aerospace_engineering','Flight propulsion aerodynamics structures and control','Fluid dynamics control models structural simulations'),
('environmental_engineering','Water waste air quality remediation and sustainability systems','Transport models fate models system simulations'),
('software_engineering','Performance reliability networks queues and architecture','Queueing models reliability models formal models'),
('systems_engineering','Complex system integration requirements risk and lifecycle design','Architecture models optimization simulation decision models');
