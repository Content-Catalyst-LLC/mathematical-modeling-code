.headers on
.mode column

SELECT 'TYPED MODEL RECORD REGISTRY' AS section;
SELECT record_name, computational_role, systems_modeling_role, review_warning
FROM typed_model_record_registry
ORDER BY record_key;

SELECT 'TYPED MODEL OUTPUT RECORDS' AS section;
SELECT output_id, model_use, growth_rate, carrying_capacity, initial_stock, time_step, horizon, review_warning
FROM typed_model_output_records
ORDER BY output_id;
