DROP TABLE IF EXISTS state_vector_assumption_registry;
DROP TABLE IF EXISTS state_vector_components;

CREATE TABLE state_vector_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO state_vector_assumption_registry VALUES
('component_definition','Component definition','Defines each entry in the vector.','Controls what the model treats as part of the system state.','Every component should have a name, unit, source, and interpretation.'),
('component_order','Component order','Specifies the position of each vector entry.','Maintains alignment with matrices, code arrays, and documentation.','Changing order without updating matrices or code invalidates results.'),
('units_and_scale','Units and scale','Defines how vector components are measured.','Controls valid comparison, distance, magnitude, and transformation.','Mixed units can make vector norms and distances misleading.'),
('normalization_rule','Normalization rule','Defines whether raw values are transformed before computation.','Shapes similarity, clustering, ranking, decomposition, and optimization.','Normalization improves comparability but changes interpretation.'),
('state_boundary','State boundary','Defines what is included or excluded from the represented state.','Controls the scope of system interpretation.','Important omitted components can make a vector appear more complete than it is.'),
('time_and_scenario_label','Time and scenario label','Identifies when or under what scenario the vector applies.','Supports state comparison and transition modeling.','Mixing time steps or scenarios can create invalid comparisons.');

CREATE TABLE state_vector_components (
    position INTEGER PRIMARY KEY,
    component_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    scale_type TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO state_vector_components VALUES
(1,'road_condition',72.0,'index_0_to_100','raw_index','Index values should not be treated as physical units.'),
(2,'bridge_condition',68.0,'index_0_to_100','raw_index','Comparable only if index construction is aligned.'),
(3,'water_reliability',0.91,'probability','proportion','Probability scale differs from condition index scale.'),
(4,'power_reliability',0.96,'probability','proportion','Do not directly add probability values to index scores.'),
(5,'transit_capacity',125000.0,'daily_passenger_capacity','raw_count','Raw count can dominate vector magnitude without scaling.');
