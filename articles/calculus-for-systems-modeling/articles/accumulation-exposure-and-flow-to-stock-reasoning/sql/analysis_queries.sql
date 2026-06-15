.headers on
.mode column

SELECT 'ACCUMULATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM accumulation_assumption_registry
ORDER BY assumption_key;

SELECT 'FLOW TO STOCK AUDIT' AS section;
SELECT
  50.0 AS initial_stock,
  SUM(inflow * duration) AS cumulative_inflow,
  SUM(outflow * duration) AS cumulative_outflow,
  SUM(inflow * duration) - SUM(outflow * duration) AS net_accumulation,
  50.0 + SUM(inflow * duration) - SUM(outflow * duration) AS ending_stock,
  SUM(exposure_intensity * duration) AS cumulative_exposure,
  SUM(exposure_intensity * population_weight * duration) AS population_weighted_exposure,
  SUM(inflow * duration) + SUM(outflow * duration) AS gross_activity
FROM flow_records;
