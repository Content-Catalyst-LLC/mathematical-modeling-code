.headers on
.mode column

SELECT 'PURPOSE TYPES' AS section;
SELECT purpose, description, typical_failure
FROM purpose_type
ORDER BY purpose;

SELECT 'PURPOSES REQUIRING REVIEW' AS section;
SELECT purpose, primary_question, validation_standard, misuse_risk
FROM purpose_register
WHERE supported_use_status IN ('review', 'revise', 'prohibited');

SELECT 'SCENARIOS BY PURPOSE' AS section;
SELECT purpose, COUNT(*) AS scenario_count
FROM scenario_parameter
GROUP BY purpose
ORDER BY purpose;

SELECT 'VALIDATION MATRIX' AS section;
SELECT purpose, validation_emphasis, evidence_needed, prohibited_without_review
FROM purpose_validation_matrix
ORDER BY purpose;

SELECT 'PROHIBITED USES' AS section;
SELECT prohibited_use, reason, evidence_required_for_expansion
FROM prohibited_use;
