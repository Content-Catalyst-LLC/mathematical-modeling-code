#[derive(Debug)]
enum AssumptionType {
    Boundary,
    FunctionalForm,
    Uncertainty,
    Interpretive,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresSensitivityTest,
    RequiresValidation,
}

#[derive(Debug)]
struct AssumptionRecord {
    key: &'static str,
    assumption_type: AssumptionType,
    risk_if_false: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        AssumptionRecord {
            key: "fixed_capacity",
            assumption_type: AssumptionType::Boundary,
            risk_if_false: "Usable capacity may depend on operating rules.",
            status: ReviewStatus::Active,
        },
        AssumptionRecord {
            key: "proportional_losses",
            assumption_type: AssumptionType::FunctionalForm,
            risk_if_false: "Losses may depend on season, temperature, or leakage.",
            status: ReviewStatus::RequiresSensitivityTest,
        },
        AssumptionRecord {
            key: "deterministic_inflow",
            assumption_type: AssumptionType::Uncertainty,
            risk_if_false: "Shortage risk may be understated.",
            status: ReviewStatus::RequiresReview,
        },
        AssumptionRecord {
            key: "shortage_proxy",
            assumption_type: AssumptionType::Interpretive,
            risk_if_false: "Severity and affected users may be hidden.",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
