#[derive(Debug)]
enum UncertaintyLayer {
    DataUncertainty,
    ParameterUncertainty,
    ModelFormUncertainty,
    ScenarioUncertainty,
    AleatoryUncertainty,
    DecisionUncertainty,
    Governance,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresMonitoring,
}

#[derive(Debug)]
struct UncertaintyRecord {
    key: &'static str,
    layer: UncertaintyLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        UncertaintyRecord {
            key: "measurement_uncertainty",
            layer: UncertaintyLayer::DataUncertainty,
            review_focus: "Data quality and measurement error",
            status: ReviewStatus::Active,
        },
        UncertaintyRecord {
            key: "parameter_uncertainty",
            layer: UncertaintyLayer::ParameterUncertainty,
            review_focus: "Parameter intervals and sensitivity",
            status: ReviewStatus::RequiresReview,
        },
        UncertaintyRecord {
            key: "structural_uncertainty",
            layer: UncertaintyLayer::ModelFormUncertainty,
            review_focus: "Alternative model forms",
            status: ReviewStatus::RequiresReview,
        },
        UncertaintyRecord {
            key: "decision_uncertainty",
            layer: UncertaintyLayer::DecisionUncertainty,
            review_focus: "Decision stability",
            status: ReviewStatus::RequiresMonitoring,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
