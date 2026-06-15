DROP TABLE IF EXISTS change_of_variables_assumption_registry;
DROP TABLE IF EXISTS change_of_variables_cases;

CREATE TABLE change_of_variables_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO change_of_variables_assumption_registry VALUES
('transformation_map','Transformation map','Defines how new variables map into original variables.','Specifies how model states coordinates or parameters are translated.','A transformation cannot be audited if the map is unclear.'),
('domain_mapping','Domain mapping','Relates the transformed domain to the original region.','Determines what spatial or state-space region is included.','Incorrect domain mapping can omit or double-count parts of the system.'),
('jacobian_determinant','Jacobian determinant','Provides local area or volume scaling.','Preserves accumulated quantities under transformation.','Omitting the Jacobian factor usually changes the modeled total.'),
('measure_element','Measure element','Defines transformed area or volume scaling.','Connects coordinate geometry to physical accumulation.','Units can become invalid when measure is missing.'),
('invertibility','Invertibility','Determines whether parameter points map uniquely to original points.','Prevents double counting or ambiguous density transformation.','Non-invertible transformations require domain restrictions or special handling.'),
('density_conservation','Density conservation','Ensures transformed density preserves total mass probability or burden.','Supports meaningful comparison before and after transformation.','Density claims should include units and measure elements.');

CREATE TABLE change_of_variables_cases (
    scenario TEXT NOT NULL,
    radius REAL NOT NULL,
    radial_step REAL NOT NULL,
    angular_step REAL NOT NULL,
    polar_total REAL NOT NULL,
    cartesian_grid_total REAL NOT NULL,
    absolute_difference REAL NOT NULL,
    relative_difference REAL NOT NULL,
    jacobian_rule TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO change_of_variables_cases VALUES
('medium_polar_grid',3.0,0.5,0.1308996939,282.0,286.0,4.0,0.014184,'dA = r dr dtheta','Polar Jacobian factor r included; compare domain and resolution assumptions.'),
('fine_polar_grid',3.0,0.25,0.0654498469,281.0,283.0,2.0,0.007117,'dA = r dr dtheta','Polar Jacobian factor r included; compare domain and resolution assumptions.'),
('very_fine_polar_grid',3.0,0.125,0.0327249235,280.5,281.5,1.0,0.003565,'dA = r dr dtheta','Polar Jacobian factor r included; compare domain and resolution assumptions.');
