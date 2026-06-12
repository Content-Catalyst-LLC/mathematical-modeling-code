#[derive(Debug)]
enum ModelPurpose {
    Explanation,
    Prediction,
    Control,
    DecisionSupport,
    Simulation,
    Optimization,
}

#[derive(Debug)]
enum UseStatus {
    Supported,
    Exploratory,
    RequiresValidation,
    Prohibited,
}

#[derive(Debug)]
struct PurposeRecord {
    purpose: ModelPurpose,
    validation_need: &'static str,
    misuse_risk: &'static str,
    status: UseStatus,
}

fn main() {
    let records = vec![
        PurposeRecord {
            purpose: ModelPurpose::Explanation,
            validation_need: "mechanism and structural plausibility review",
            misuse_risk: "plausible mechanism treated as validated cause",
            status: UseStatus::Supported,
        },
        PurposeRecord {
            purpose: ModelPurpose::Prediction,
            validation_need: "out-of-sample validation and uncertainty calibration",
            misuse_risk: "forecast used beyond validation horizon",
            status: UseStatus::RequiresValidation,
        },
        PurposeRecord {
            purpose: ModelPurpose::Control,
            validation_need: "stability, robustness, monitoring, and fail-safes",
            misuse_risk: "automated action without oversight",
            status: UseStatus::RequiresValidation,
        },
        PurposeRecord {
            purpose: ModelPurpose::DecisionSupport,
            validation_need: "decision context, trade-offs, and governance review",
            misuse_risk: "decision support becomes decision substitution",
            status: UseStatus::Exploratory,
        },
        PurposeRecord {
            purpose: ModelPurpose::Simulation,
            validation_need: "scenario adequacy and structural review",
            misuse_risk: "simulation trace treated as forecast",
            status: UseStatus::RequiresValidation,
        },
        PurposeRecord {
            purpose: ModelPurpose::Optimization,
            validation_need: "objective sensitivity and constraint validation",
            misuse_risk: "objective treated as complete value system",
            status: UseStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
