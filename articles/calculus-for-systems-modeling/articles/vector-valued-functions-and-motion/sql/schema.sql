DROP TABLE IF EXISTS motion_assumption_registry;
DROP TABLE IF EXISTS trajectory_audit_cases;

CREATE TABLE motion_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO motion_assumption_registry VALUES
('parameter_meaning','Parameter meaning','Defines what the trajectory parameter represents.','Distinguishes time distance scenario stage and simulation step.','Velocity and speed interpretation depend on the parameter.'),
('component_units','Component units','Defines units for each coordinate or state component.','Supports meaningful velocity distance and state-space comparison.','Unclear units make trajectory diagnostics difficult to interpret.'),
('sampling_resolution','Sampling resolution','Defines the step size used to approximate the continuous path.','Shapes computed speed arc length acceleration and curvature.','Coarse sampling may miss turns or underestimate path length.'),
('path_domain','Path domain','Defines the interval where the vector-valued function applies.','Determines the modeled portion of motion or system evolution.','Changing the interval changes total distance and trajectory interpretation.'),
('state_space_scaling','State-space scaling','Defines how different state variables are compared or normalized.','Supports trajectory analysis outside physical space.','Unscaled variables can dominate state-space distance and curvature.');

CREATE TABLE trajectory_audit_cases (
    scenario TEXT NOT NULL,
    time_step REAL NOT NULL,
    point_count INTEGER NOT NULL,
    approximate_arc_length REAL NOT NULL,
    displacement_magnitude REAL NOT NULL,
    path_efficiency REAL NOT NULL,
    average_speed REAL NOT NULL,
    maximum_speed REAL NOT NULL,
    domain_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO trajectory_audit_cases VALUES
('coarse_time_step',1.0,7,7.42,6.28,0.846,1.237,1.395,'trajectory r(t)=<t,sin(t)>','Time step is coarse; turns and speed variation may be undersampled.'),
('medium_time_step',0.5,13,7.60,6.28,0.826,1.267,1.411,'trajectory r(t)=<t,sin(t)>','Synthetic trajectory audit; document units parameter meaning and sampling.'),
('fine_time_step',0.25,26,7.63,6.25,0.819,1.272,1.414,'trajectory r(t)=<t,sin(t)>','Synthetic trajectory audit; document units parameter meaning and sampling.');
