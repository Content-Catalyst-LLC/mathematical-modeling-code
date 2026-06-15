DROP TABLE IF EXISTS spatial_accumulation_assumption_registry;
DROP TABLE IF EXISTS spatial_accumulation_cases;

CREATE TABLE spatial_accumulation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO spatial_accumulation_assumption_registry VALUES
('integrand_definition','Integrand definition','Specifies the local density or intensity being accumulated.','Determines what the spatial total actually measures.','The integral is only meaningful if the integrand represents the intended quantity.'),
('region_definition','Region definition','Defines the spatial domain of integration.','Determines what is included excluded and aggregated.','Changing the boundary can change the total and interpretation.'),
('measure_element','Measure element','Defines the area or volume element used in accumulation.','Ensures density units combine correctly with spatial units.','Coordinate transformations require correct area or volume scaling.'),
('grid_resolution','Grid resolution','Controls approximation of a continuous integral by cells.','Shapes how local variation appears in spatial totals.','Coarse grids may hide hotspots or edge effects.'),
('region_mask','Region mask','Selects cells or points inside a modeled domain.','Separates included from excluded spatial units.','Mask logic can drive the final total.'),
('weighted_aggregation','Weighted aggregation','Combines one spatial field with another weighting field.','Supports population-weighted exposure demand-weighted service burden or risk-weighted summaries.','Weighted averages can clarify burden but may also hide distributional inequality.');

CREATE TABLE spatial_accumulation_cases (
    scenario TEXT NOT NULL,
    cells_in_region INTEGER NOT NULL,
    cell_area REAL NOT NULL,
    total_area REAL NOT NULL,
    total_density_accumulation REAL NOT NULL,
    area_weighted_average REAL NOT NULL,
    population_weighted_burden REAL NOT NULL,
    population_total REAL NOT NULL,
    population_weighted_average_exposure REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO spatial_accumulation_cases VALUES
('coarse_grid',29,1.0,29.0,356.0,12.275862,35800.0,2900.0,12.344828,'Grid resolution is coarse; spatial accumulation may smooth local variation.'),
('medium_grid',113,0.25,28.25,346.0,12.247788,34700.0,2825.0,12.283186,'Synthetic grid audit; region mask cell area and units should be documented.'),
('fine_grid',441,0.0625,27.5625,337.0,12.226757,33800.0,2756.25,12.262132,'Synthetic grid audit; region mask cell area and units should be documented.');
