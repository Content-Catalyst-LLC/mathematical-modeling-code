#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("record_type,name,pattern_or_element,response_or_warning,status\n");
  printf("continuity_assumption,smooth_state_change,state_trajectory_x_t,smooth_output_does_not_prove_smooth_system_behavior,review\n");
  printf("continuity_assumption,continuous_rate_function,dxdt_equals_f,rate_continuity_should_be_justified,review\n");
  printf("risk_record,false_smoothness,smooth_curve_hides_structural_breaks,test_for_breaks_and_document_discontinuities,review\n");
  printf("risk_record,equilibrium_bias,steady_state_overinterpreted,analyze_trajectories_and_stability,review\n");
  printf("solver_diagnostic,convergence_check,numerical_solution_converged,a_plotted_output_can_hide_convergence_failure,review\n");
  return EXIT_SUCCESS;
}
