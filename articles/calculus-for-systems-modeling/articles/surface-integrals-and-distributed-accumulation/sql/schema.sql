DROP TABLE IF EXISTS surface_integral_assumption_registry;
DROP TABLE IF EXISTS surface_integral_audit_cases;

CREATE TABLE surface_integral_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO surface_integral_assumption_registry VALUES
('surface_definition','Surface definition','Specifies the surface over which the integral is computed.','Determines the boundary membrane terrain envelope or control surface being analyzed.','A surface integral is not interpretable without a clearly defined surface.'),
('surface_orientation','Surface orientation','Defines the normal direction for flux calculations.','Determines what counts as positive crossing outflow or inflow.','Reversing the normal reverses flux sign.'),
('surface_area_element','Surface area element','Converts parameter or projected area into actual surface area.','Accounts for curvature slope and geometry.','Projected area can underestimate curved or sloped surfaces.'),
('scalar_surface_units','Scalar surface units','Defines the quantity accumulated per unit surface area.','Supports pressure load exposure radiation contamination or burden interpretation.','Scalar surface-integral units combine field units and area units.'),
('flux_units','Flux units','Defines vector-field crossing through an oriented surface.','Supports flow energy water material air or emissions accounting.','Vector-field units normal direction and area units must be compatible.'),
('mesh_resolution','Mesh resolution','Defines how the continuous surface is approximated by patches.','Shapes computed area scalar accumulation and flux.','Coarse meshes can miss curvature or field variation.');

CREATE TABLE surface_integral_audit_cases (
    scenario TEXT NOT NULL,
    grid_step REAL NOT NULL,
    patch_count INTEGER NOT NULL,
    approximate_surface_area REAL NOT NULL,
    scalar_surface_integral REAL NOT NULL,
    vector_flux_integral REAL NOT NULL,
    average_flux_density REAL NOT NULL,
    maximum_patch_area REAL NOT NULL,
    surface_description TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO surface_integral_audit_cases VALUES
('coarse_surface_mesh',1.0,4,4.050,4.150,3.900,0.963,1.025,'graph z=0.1x^2+0.05y^2','Grid step is coarse; curvature and field variation may be undersampled.'),
('medium_surface_mesh',0.5,16,4.030,4.120,3.950,0.980,0.256,'graph z=0.1x^2+0.05y^2','Synthetic surface-integral audit; document surface normal units and mesh.'),
('fine_surface_mesh',0.25,64,4.020,4.105,3.975,0.989,0.064,'graph z=0.1x^2+0.05y^2','Synthetic surface-integral audit; document surface normal units and mesh.');
