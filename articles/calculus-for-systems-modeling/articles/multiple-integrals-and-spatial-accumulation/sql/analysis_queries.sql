.headers on
.mode column

SELECT 'SPATIAL ACCUMULATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM spatial_accumulation_assumption_registry
ORDER BY assumption_key;

SELECT 'SPATIAL ACCUMULATION CASES' AS section;
SELECT scenario, cells_in_region, cell_area, total_area, area_weighted_average, population_weighted_average_exposure, warning
FROM spatial_accumulation_cases
ORDER BY cell_area DESC;
