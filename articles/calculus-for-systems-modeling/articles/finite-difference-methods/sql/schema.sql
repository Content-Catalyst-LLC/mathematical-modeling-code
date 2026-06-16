DROP TABLE IF EXISTS finite_difference_assumption_registry;
CREATE TABLE finite_difference_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);
INSERT INTO finite_difference_assumption_registry VALUES
('grid_spacing','Grid spacing','Defines spatial resolution of the finite difference approximation.','Controls what spatial structure the model can represent.','Grid refinement should be tested when gradients or boundaries matter.'),
('time_step','Time step','Defines temporal resolution of the update scheme.','Controls simulation pace, stability, and temporal detail.','Time-step sensitivity should be tested and documented.'),
('stencil','Finite difference stencil','Defines which neighboring values approximate derivatives.','Encodes local interaction, smoothing, transport, or curvature.','Stencil choice affects accuracy, stability, and boundary behavior.'),
('boundary_condition','Boundary condition','Defines behavior at the domain edge.','Represents fixed, no-flux, inflow, outflow, reflective, or periodic boundaries.','Boundary assumptions can dominate results and should be compared.'),
('stability_condition','Stability condition','Defines whether numerical errors remain controlled under repeated updates.','Protects against simulation artifacts being mistaken for system behavior.','Scheme-specific stability checks should be recorded.'),
('convergence_check','Convergence check','Compares solutions across grid or time-step refinements.','Tests whether modeled conclusions persist under numerical refinement.','Lack of convergence is a warning.');
