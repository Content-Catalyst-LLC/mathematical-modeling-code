program reproducible_calculus_workflows
  implicit none
  print '(A)', 'artifact_name artifact_type path source_or_generated review_role'
  print '(A)', 'parameter_records csv data/parameter_records.csv source documents_parameter_records'
  print '(A)', 'model_outputs csv outputs/tables/model_outputs.csv generated stores_computed_outputs'
  print '(A)', 'diagnostics json outputs/json/diagnostics.json generated records_warning_status'
  print '(A)', 'governance_queue markdown outputs/reports/governance_queue.md generated collects_review_items'
end program
