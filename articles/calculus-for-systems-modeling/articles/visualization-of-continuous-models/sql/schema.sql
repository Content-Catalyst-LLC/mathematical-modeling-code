DROP TABLE IF EXISTS continuous_model_visualization_registry;
DROP TABLE IF EXISTS visualization_audit_records;

CREATE TABLE continuous_model_visualization_registry (
    visualization_key TEXT PRIMARY KEY,
    visualization_name TEXT NOT NULL,
    visual_operation TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO continuous_model_visualization_registry VALUES
('trajectory_plot','Trajectory plot','Plot state value against time.','Shows growth, decline, oscillation, convergence, or collapse.','A smooth trajectory may hide uncertainty, solver error, or invalid assumptions.'),
('phase_portrait','Phase portrait','Plot motion through state space.','Shows equilibria, cycles, attraction, repulsion, and basins.','The visible state-space window can hide important behavior.'),
('vector_field','Vector field','Plot direction and magnitude across a domain.','Shows flow, gradient, force, or spatial movement.','Arrow scaling and normalization should be documented.'),
('contour_surface','Contour or surface plot','Visualize response over two inputs or spatial dimensions.','Shows gradients, thresholds, and interaction effects.','Color scale, interpolation, and grid resolution can distort interpretation.'),
('uncertainty_band','Uncertainty band','Plot ranges around modeled trajectories.','Shows sensitivity, scenario spread, or uncertainty.','The meaning of the band must be explained.'),
('diagnostic_plot','Diagnostic plot','Visualize error, residuals, solver steps, or constraints.','Helps distinguish model behavior from numerical artifact.','Diagnostics should accompany important model outputs.');

CREATE TABLE visualization_audit_records (
    figure_id TEXT PRIMARY KEY,
    visual_type TEXT NOT NULL,
    model_object TEXT NOT NULL,
    x_axis TEXT NOT NULL,
    y_axis TEXT NOT NULL,
    scale_note TEXT NOT NULL,
    uncertainty_note TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO visualization_audit_records VALUES
('logistic_growth_scenario_trajectories','trajectory_plot','logistic_solution','time','state value','Linear axes; time horizon 0 to 20.','Scenario lines are parameter contrasts, not probability intervals.','The figure shows model-implied trajectories under selected assumptions, not empirical forecasts.'),
('phase_portrait_review','phase_portrait','two_state_dynamic_system','state x','state y','State-space window should be documented.','Initial condition selection affects visible trajectories.','Phase portraits show local and geometric behavior, not automatic empirical validity.'),
('vector_field_review','vector_field','spatial_flow_field','x coordinate','y coordinate','Arrow scaling should be documented.','Magnitude and direction can be visually distorted by normalization.','Vector fields require unit and boundary interpretation.');
