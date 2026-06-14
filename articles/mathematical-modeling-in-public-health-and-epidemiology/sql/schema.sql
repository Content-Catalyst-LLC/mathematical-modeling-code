-- Mathematical modeling in public health and epidemiology governance schema.

DROP TABLE IF EXISTS public_health_domain_guide;
DROP TABLE IF EXISTS epidemic_scenario;
DROP TABLE IF EXISTS public_health_model_register;
DROP TABLE IF EXISTS public_health_model_role_type;

CREATE TABLE public_health_model_role_type (
    model_role TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE public_health_model_register (
    record_id INTEGER PRIMARY KEY,
    record_key TEXT NOT NULL,
    domain TEXT NOT NULL,
    model_role TEXT NOT NULL,
    model_family TEXT NOT NULL,
    public_health_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (model_role) REFERENCES public_health_model_role_type(model_role)
);

CREATE TABLE epidemic_scenario (
    scenario_key TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    population REAL NOT NULL,
    initial_infectious REAL NOT NULL,
    initial_recovered REAL NOT NULL,
    beta REAL NOT NULL,
    gamma REAL NOT NULL,
    days INTEGER NOT NULL,
    hospital_capacity REAL NOT NULL,
    hospitalization_rate REAL NOT NULL
);

CREATE TABLE public_health_domain_guide (
    area TEXT PRIMARY KEY,
    modeling_use TEXT NOT NULL,
    typical_model_forms TEXT NOT NULL
);

INSERT INTO public_health_model_role_type VALUES
('transmission_analysis','Represents disease spread under contact and intervention assumptions.','Transmission assumptions are hidden or treated as fixed.'),
('data_interpretation','Reviews surveillance data under delay, undercounting, and bias.','Reported cases are treated as true infections.'),
('capacity_review','Connects infection dynamics to hospital demand and operational constraints.','Nominal capacity is mistaken for usable capacity.'),
('distributional_review','Assesses unequal exposure, severity, detection, and access.','Aggregate performance hides subgroup harm.'),
('uncertainty_communication','Communicates scenarios, ranges, assumptions, and use limits.','Conditional model outputs are presented as certainty.');

INSERT INTO public_health_model_register(record_key, domain, model_role, model_family, public_health_question, status) VALUES
('transmission_model','infectious_disease','transmission_analysis','sir_compartmental_model','How does transmission change under different intervention assumptions?','active'),
('surveillance_model','public_health_surveillance','data_interpretation','nowcasting_and_reporting_delay_model','How should reported data be interpreted under delay and undercounting?','review'),
('capacity_model','health_system_planning','capacity_review','hospital_demand_model','Could projected severe cases exceed healthcare capacity?','review'),
('equity_model','health_equity','distributional_review','subgroup_risk_model','Which populations face unequal exposure severity or access?','review'),
('communication_model','public_communication','uncertainty_communication','scenario_summary_model','How should model uncertainty and use limits be communicated?','review');

INSERT INTO epidemic_scenario VALUES
('baseline','Baseline transmission',100000.0,120.0,4000.0,0.32,0.12,120,850.0,0.045),
('moderate_intervention','Moderate intervention',100000.0,120.0,4000.0,0.24,0.12,120,850.0,0.045),
('strong_intervention','Strong intervention',100000.0,120.0,4000.0,0.18,0.12,120,850.0,0.045),
('vaccination_plus_intervention','Vaccination plus intervention',100000.0,120.0,22000.0,0.20,0.12,120,850.0,0.030);

INSERT INTO public_health_domain_guide VALUES
('infectious_disease','Transmission dynamics intervention scenarios and epidemic forecasting','SIR SEIR network models agent-based models'),
('public_health_surveillance','Trend detection nowcasting reporting delay and signal interpretation','Statistical surveillance models nowcasting anomaly detection'),
('health_system_planning','Hospital demand staffing ICU bed and supply planning','Capacity models queueing models demand forecasts'),
('vaccination_planning','Coverage strategy prioritization and immunity effects','Compartmental models optimization models'),
('screening_and_prevention','Risk detection program design and prevention planning','Risk models decision trees cost-effectiveness models'),
('environmental_health','Exposure risk burden estimation and intervention planning','Exposure models spatial models dose-response models'),
('health_equity','Subgroup risk access and distributional consequences','Stratified models subgroup validation equity diagnostics'),
('emergency_response','Preparedness response logistics and crisis allocation','Scenario models optimization stress tests');
