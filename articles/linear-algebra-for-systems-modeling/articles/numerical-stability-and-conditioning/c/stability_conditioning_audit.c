#include <stdio.h>

int main(void) {
    printf("model_name,matrix_case,matrix_shape,determinant,condition_number_proxy,solution_norm,residual_norm,relative_residual,perturbation_size,perturbed_solution_change,stability_status,warning\n");
    printf("numerical_stability_conditioning_audit,well_conditioned_system,2x2,5.750000,2.100000,0.340000,0.000000,0.000000,0.000010,0.000004,stable_under_demo_threshold,Residuals require conditioning scaling perturbation solver precision and model-purpose review.\n");
    printf("numerical_stability_conditioning_audit,ill_conditioned_system,2x2,0.00000001,399920000.000000,50000000.000000,0.000000,0.000000,0.000010,2000.000000,review_required_ill_conditioned,Residuals require conditioning scaling perturbation solver precision and model-purpose review.\n");
    return 0;
}
