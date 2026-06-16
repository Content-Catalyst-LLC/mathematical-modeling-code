#include <iostream>
#include <string>
#include <vector>

struct Record {
  std::string recordType;
  std::string name;
  std::string category;
  std::string permittedOrDescription;
  std::string warning;
};

int main() {
  std::vector<Record> records = {
    {"purpose_record","synthetic_logistic_growth","teaching","illustrates_growth_saturation_capacity","synthetic_models_are_not_empirical_evidence"},
    {"purpose_record","scenario_sweep","exploratory","compares_parameter_scenarios","scenario_outputs_are_not_forecasts"},
    {"assumption_record","continuous_growth","mathematical","state_changes_continuously","smooth_model_may_hide_shocks_thresholds"},
    {"assumption_record","objective_function_weights","normative","priority_structure","value_judgments_can_hide_inside_mathematics"},
    {"claim_boundary","predictive","validation","validated_domain_forecast","validation_is_purpose_specific"}
  };
  std::cout << "record_type,name,category,permitted_or_description,warning\n";
  for (const auto& r : records) {
    std::cout << r.recordType << "," << r.name << "," << r.category << "," << r.permittedOrDescription << "," << r.warning << "\n";
  }
}
