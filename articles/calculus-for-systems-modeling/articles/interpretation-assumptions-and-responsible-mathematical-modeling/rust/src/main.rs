struct Record {
    record_type: &'static str,
    name: &'static str,
    category: &'static str,
    permitted_or_description: &'static str,
    warning: &'static str,
}

fn main() {
    let records = [
        Record { record_type: "purpose_record", name: "synthetic_logistic_growth", category: "teaching", permitted_or_description: "illustrates_growth_saturation_capacity", warning: "synthetic_models_are_not_empirical_evidence" },
        Record { record_type: "purpose_record", name: "scenario_sweep", category: "exploratory", permitted_or_description: "compares_parameter_scenarios", warning: "scenario_outputs_are_not_forecasts" },
        Record { record_type: "assumption_record", name: "continuous_growth", category: "mathematical", permitted_or_description: "state_changes_continuously", warning: "smooth_model_may_hide_shocks_thresholds" },
        Record { record_type: "assumption_record", name: "objective_function_weights", category: "normative", permitted_or_description: "priority_structure", warning: "value_judgments_can_hide_inside_mathematics" },
        Record { record_type: "claim_boundary", name: "predictive", category: "validation", permitted_or_description: "validated_domain_forecast", warning: "validation_is_purpose_specific" },
    ];
    println!("record_type,name,category,permitted_or_description,warning");
    for r in records {
        println!("{},{},{},{},{}", r.record_type, r.name, r.category, r.permitted_or_description, r.warning);
    }
}
