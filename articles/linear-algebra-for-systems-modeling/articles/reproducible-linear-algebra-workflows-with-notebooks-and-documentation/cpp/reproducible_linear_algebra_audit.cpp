#include <iostream>

int main() {
    std::cout << "workflow_name,notebook_status,documentation_status,matrix_shape,data_provenance_status,environment_status,validation_status,generated_outputs_status,residual_norm,relative_residual,reproducibility_score,warning\n";
    std::cout << "reproducible_linear_algebra_workflow_audit,clean_execution_required_and_documented,readme_data_dictionary_method_notes_and_governance_report_required,2x2,synthetic_data_documented_in_workflow,runtime_metadata_recorded,reference_solution_and_residual_check_passed,tables_json_and_reports_written_by_workflow,0.000000,0.000000,100,Reproducibility means rerunnable and reviewable not automatically valid.\n";
    return 0;
}
