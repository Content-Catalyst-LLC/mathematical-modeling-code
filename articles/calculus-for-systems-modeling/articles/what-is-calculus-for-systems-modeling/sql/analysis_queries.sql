.headers on
.mode column

SELECT 'SYSTEM SCENARIOS' AS section;
SELECT scenario, initial_state, rate, capacity, dt, steps, interpretation
FROM system_scenario
ORDER BY scenario;

SELECT 'MODELING USES OF CALCULUS' AS section;
SELECT use_case, calculus_concept, systems_interpretation
FROM modeling_use
ORDER BY use_case;
