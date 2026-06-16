#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("record_type,name,category,permitted_or_description,warning\n");
  printf("purpose_record,synthetic_logistic_growth,teaching,illustrates_growth_saturation_capacity,synthetic_models_are_not_empirical_evidence\n");
  printf("purpose_record,scenario_sweep,exploratory,compares_parameter_scenarios,scenario_outputs_are_not_forecasts\n");
  printf("assumption_record,continuous_growth,mathematical,state_changes_continuously,smooth_model_may_hide_shocks_thresholds\n");
  printf("assumption_record,objective_function_weights,normative,priority_structure,value_judgments_can_hide_inside_mathematics\n");
  printf("claim_boundary,predictive,validation,validated_domain_forecast,validation_is_purpose_specific\n");
  return EXIT_SUCCESS;
}
