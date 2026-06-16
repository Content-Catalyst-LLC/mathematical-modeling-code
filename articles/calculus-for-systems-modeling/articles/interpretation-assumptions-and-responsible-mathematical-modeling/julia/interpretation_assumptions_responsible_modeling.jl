records = [
    ("purpose_record", "synthetic_logistic_growth", "teaching", "empirical forecast prohibited", "synthetic teaching models are not empirical evidence"),
    ("purpose_record", "scenario_sweep", "exploratory", "single-point prediction prohibited", "scenario outputs are not forecasts"),
    ("assumption_record", "continuous_growth", "mathematical", "smoothness assumption", "smooth model may hide shocks or thresholds"),
    ("assumption_record", "objective_function_weights", "normative", "priority structure", "value judgments can hide inside mathematics"),
    ("claim_boundary", "predictive", "validated-domain forecast", "outside validation scope prohibited", "validation is purpose-specific")
]

println("record_type,name,category,permitted_or_description,warning")
for row in records
    println(join(row, ","))
end
