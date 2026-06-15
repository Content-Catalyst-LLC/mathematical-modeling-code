DROP TABLE IF EXISTS pde_assumption_registry;
DROP TABLE IF EXISTS pde_audit_cases;

CREATE TABLE pde_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO pde_assumption_registry VALUES
('state_field','State field','Defines the distributed variable being modeled.','Represents temperature, concentration, pressure, density, risk, load, or another field.','The field should have clear units, domain, and interpretation.'),
('domain_geometry','Domain geometry','Defines where the field exists.','Represents a line, grid, surface, region, volume, or modeled space.','Domain shape and scale can strongly affect results.'),
('boundary_condition','Boundary condition','Defines field behavior at the edge of the domain.','Represents fixed values, flux, insulation, exchange, inflow, outflow, or periodicity.','Boundary conditions should be justified and tested.'),
('initial_condition','Initial condition','Defines the starting field.','Represents the spatial distribution at the beginning of simulation.','Initial-field uncertainty can strongly affect early dynamics.'),
('stability_ratio','Stability ratio','Controls numerical stability in explicit finite-difference schemes.','Helps distinguish valid approximation from numerical artifact.','Unstable numerical output should not be interpreted as system behavior.'),
('grid_resolution','Grid resolution','Defines spatial approximation of the continuous domain.','Controls detail, computational cost, and approximation error.','Grid refinement should be tested where results influence interpretation.');

CREATE TABLE pde_audit_cases (
    scenario TEXT NOT NULL,
    grid_points INTEGER NOT NULL,
    diffusivity REAL NOT NULL,
    dx REAL NOT NULL,
    dt REAL NOT NULL,
    steps INTEGER NOT NULL,
    stability_ratio REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO pde_audit_cases VALUES
('explicit_one_dimensional_diffusion_teaching_grid',51,0.1,1.0,0.25,100,0.025,'Explicit diffusion schemes require stability checks; boundary and grid assumptions shape results.');
