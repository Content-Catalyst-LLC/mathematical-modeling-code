DROP TABLE IF EXISTS energy_balance_governance_registry;
DROP TABLE IF EXISTS energy_parameter_records;
DROP TABLE IF EXISTS energy_scenario_records;
DROP TABLE IF EXISTS energy_diagnostic_records;

CREATE TABLE energy_balance_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO energy_balance_governance_registry VALUES
('boundary_record','Boundary record','Defines the control volume, system state, spatial scale, and time scale.','Prevents energy inputs and outputs from being interpreted without a system boundary.','Energy balance conclusions are not meaningful without a defined boundary.'),
('flow_record','Flow record','Documents incoming energy, outgoing energy, radiation, conduction, convection, latent heat, storage, and exchange.','Connects system change to energy flows.','Omitted flows can change the interpretation of imbalance.'),
('storage_record','Storage record','Documents heat capacity, thermal mass, reservoir depth, and adjustment time scale.','Connects energy imbalance to delayed temperature response.','Equilibrium should not be confused with immediate response.'),
('forcing_record','Forcing record','Documents external drivers of energy imbalance.','Separates external disturbance from internal system response.','Forcing assumptions should be documented as historical, scenario-based, or experimental.'),
('feedback_record','Feedback record','Documents restoring or amplifying responses to temperature or state change.','Connects equilibrium response to system processes.','Feedback terms can hide multiple physical processes.'),
('calibration_record','Calibration record','Documents observations, data sources, measurement definitions, fitted parameters, and validation scope.','Separates model fit from physical explanation.','A model can fit temperature while misrepresenting mechanism.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, scenario comparison, design analysis, climate interpretation, or decision support.','Prevents overclaiming and scope drift.','Energy balance conclusions should not exceed boundary definitions, data evidence, uncertainty, domain review, and tested scope.');

CREATE TABLE energy_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO energy_parameter_records VALUES
('C',10.0,'W yr m^-2 K^-1','effective heat capacity','Heat capacity must match the modeled reservoir.'),
('F',3.7,'W m^-2','external forcing','Forcing assumptions should be documented as historical, scenario-based, or experimental.'),
('lambda',1.2,'W m^-2 K^-1','feedback parameter','Feedback terms can hide multiple physical processes.'),
('alpha',0.30,'fraction','albedo','Albedo can vary with clouds, ice, land cover, and surface condition.'),
('kappa',0.7,'W m^-2 K^-1','upper-deep layer exchange','Layer exchange controls delayed response and hidden heat uptake.'),
('S0',1361.0,'W m^-2','solar constant','Solar input requires geometric averaging and boundary definition.');

CREATE TABLE energy_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    final_temperature REAL NOT NULL,
    equilibrium_temperature REAL NOT NULL,
    adjustment_time REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO energy_scenario_records VALUES
('baseline_one_layer','one_layer',3.08,3.0833,8.3333,'one-layer model approaches equilibrium according to heat capacity and feedback','Baseline depends on forcing feedback and heat capacity.'),
('stronger_feedback','one_layer',2.055,2.0556,5.5556,'stronger feedback reduces equilibrium response and shortens adjustment time','Feedback strength changes equilibrium response.'),
('larger_heat_capacity','one_layer',3.05,3.0833,33.3333,'larger heat capacity slows transient response','Heat capacity controls transient response.'),
('two_layer_heat_uptake','two_layer',2.55,3.0833,8.3333,'two-layer model stores heat in a slower reservoir','Layered structure changes transient response.');

CREATE TABLE energy_diagnostic_records (
    diagnostic_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO energy_diagnostic_records VALUES
('absorbed_solar_example',238.175,'W m^-2','absorbed solar radiation with geometric averaging','Solar input requires albedo and geometry assumptions.'),
('surface_storage_residual_example',40.0,'W m^-2','storage residual after sensible latent and ground heat terms','Omitted surface energy terms change storage interpretation.'),
('building_temperature_step_example',20.11,'degrees','one-step building thermal balance','Building thermal balance requires occupancy weather controls and material assumptions.');
