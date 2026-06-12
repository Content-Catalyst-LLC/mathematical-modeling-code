.headers on
.mode column

SELECT 'REPOSITORY LAYERS' AS section;
SELECT repository_layer, description, typical_failure
FROM repository_layer_type
ORDER BY repository_layer;

SELECT 'REPOSITORY RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, repository_layer, artifact, review_question
FROM repository_audit_register
WHERE status IN ('review', 'revise');

SELECT 'EXPECTED REQUIRED ARTIFACTS' AS section;
SELECT artifact, path, purpose
FROM expected_repository_artifact
WHERE required = 1
ORDER BY artifact;

SELECT 'ARTIFACT REQUIREMENT SUMMARY' AS section;
SELECT required, COUNT(*) AS artifact_count
FROM expected_repository_artifact
GROUP BY required
ORDER BY required DESC;

SELECT 'REPOSITORY GOVERNANCE COVERAGE' AS section;
SELECT repository_layer, COUNT(*) AS record_count
FROM repository_audit_register
GROUP BY repository_layer
ORDER BY repository_layer;
