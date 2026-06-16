.headers on
.mode column

SELECT 'CONTINUOUS MODEL VISUALIZATION REGISTRY' AS section;
SELECT visualization_name, visual_operation, systems_modeling_role, review_warning
FROM continuous_model_visualization_registry
ORDER BY visualization_key;

SELECT 'VISUALIZATION AUDIT RECORDS' AS section;
SELECT figure_id, visual_type, model_object, x_axis, y_axis, scale_note, uncertainty_note, interpretation_warning
FROM visualization_audit_records
ORDER BY figure_id;
