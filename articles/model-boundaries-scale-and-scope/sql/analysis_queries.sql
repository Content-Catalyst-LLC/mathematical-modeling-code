.headers on
.mode column

SELECT 'BOUNDARY TYPES' AS section;
SELECT boundary_type, description, typical_failure
FROM boundary_type
ORDER BY boundary_type;

SELECT 'BOUNDARIES REQUIRING REVIEW' AS section;
SELECT boundary_key, boundary_type, excluded, risk_if_excluded, review_question
FROM boundary_register
WHERE status IN ('review', 'revise');

SELECT 'SCENARIOS BY BOUNDARY VERSION' AS section;
SELECT boundary_version, COUNT(*) AS scenario_count
FROM scenario_parameter
GROUP BY boundary_version
ORDER BY boundary_version;

SELECT 'SCOPE MATRIX' AS section;
SELECT scope_type, supported_use, unsupported_or_prohibited_use, validation_needed
FROM scope_matrix
ORDER BY scope_type;

SELECT 'SCOPE STATEMENT' AS section;
SELECT supported_use, exploratory_use, prohibited_use, evidence_required_for_expansion
FROM model_scope_statement;
