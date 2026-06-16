DROP TABLE IF EXISTS condition_scope_governance_registry;
DROP TABLE IF EXISTS condition_scope_records;

CREATE TABLE condition_scope_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO condition_scope_governance_registry VALUES
('initial_condition','Initial condition','Specifies the model starting state.','Selects a trajectory or scenario from many possible paths.','Initial conditions should include unit, source, uncertainty, and baseline notes.'),
('boundary_condition','Boundary condition','Specifies behavior at the edge of a domain.','Controls flow, reflection, absorption, exchange, or constraint.','Boundary assumptions can dominate spatial model behavior.'),
('temporal_scope','Temporal scope','Defines the modeled time interval and horizon.','Limits how far a model can responsibly be projected.','Short-horizon models should not be treated as long-term forecasts.'),
('spatial_scope','Spatial scope','Defines the region, network, or domain included in the model.','Clarifies what is inside and outside the modeled system.','Excluded surroundings may still affect real-world behavior.'),
('parameter_scope','Parameter scope','Defines tested or plausible parameter ranges.','Prevents unsupported parameter extrapolation.','Using values outside tested ranges requires review.'),
('claim_boundary','Claim boundary','Defines what a model output can responsibly support.','Separates computation from interpretation and decision use.','Model results should not be used beyond documented scope.');

CREATE TABLE condition_scope_records (
    record_id TEXT PRIMARY KEY,
    record_type TEXT NOT NULL,
    record_name TEXT NOT NULL,
    value_or_domain TEXT NOT NULL,
    source_or_interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO condition_scope_records VALUES
('ic_population_stock','initial_condition','population_stock','10 state units','synthetic teaching baseline','baseline chosen for demonstration');
INSERT INTO condition_scope_records VALUES
('bc_left_edge','boundary_condition','left_edge','no_flux','material does not leave through the left boundary','no-flux boundaries may overstate retention if the real system is open');
INSERT INTO condition_scope_records VALUES
('scope_temporal','scope_record','temporal_scope','0 to 20 time units','short-horizon teaching simulation','do not interpret as long-term forecast');
