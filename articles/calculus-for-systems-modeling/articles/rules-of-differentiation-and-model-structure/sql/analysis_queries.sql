.headers on
.mode column

SELECT 'DIFFERENTIATION RULE REGISTRY' AS section;
SELECT rule_name, model_structure, systems_modeling_role, review_warning
FROM differentiation_rule_registry
ORDER BY rule_key;

SELECT 'RULE REVIEW WARNINGS' AS section;
SELECT warning_name, interpretation
FROM rule_review_warning
ORDER BY warning_key;
