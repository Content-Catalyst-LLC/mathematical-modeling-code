# Reproducibility Audit

Workflow: reproducible_calculus_workflow
Command: `make smoke`
Diagnostic status: review_required

## Artifacts
- **parameter_records** (csv): documents parameter names, values, units, sources, and ranges. Parameter records do not prove empirical correctness.
- **model_outputs** (csv): stores computed trajectory or summary outputs. Generated outputs require diagnostics and interpretation limits.
- **diagnostics** (json): records validation, convergence, and warning status. Diagnostics should remain attached to interpretation.
- **governance_queue** (markdown): collects warnings requiring human review. Governance queues support judgment but do not replace it.
- **notebook_placeholder** (ipynb): documents exploratory computational pathway. Notebook state can drift; clean reruns are needed.
- **r_markdown_report** (Rmd): keeps executable prose and code together. Rendered reports should be regenerated from source.

Reproducibility supports auditability but does not prove model validity.
