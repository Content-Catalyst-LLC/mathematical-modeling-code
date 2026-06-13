#[derive(Debug)]
enum DiagnosticLayer {
    Bias,
    DecisionThreshold,
    SubgroupError,
    TailError,
    ModelForm,
    UncertaintyReview,
    Governance,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresUncertaintyCheck,
}

#[derive(Debug)]
struct DiagnosticRecord {
    key: &'static str,
    layer: DiagnosticLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        DiagnosticRecord {
            key: "residual_bias",
            layer: DiagnosticLayer::Bias,
            review_focus: "Systematic overprediction or underprediction",
            status: ReviewStatus::Active,
        },
        DiagnosticRecord {
            key: "threshold_error",
            layer: DiagnosticLayer::DecisionThreshold,
            review_focus: "Decision-changing error",
            status: ReviewStatus::RequiresValidation,
        },
        DiagnosticRecord {
            key: "group_error",
            layer: DiagnosticLayer::SubgroupError,
            review_focus: "Uneven model reliability",
            status: ReviewStatus::RequiresReview,
        },
        DiagnosticRecord {
            key: "structural_error",
            layer: DiagnosticLayer::ModelForm,
            review_focus: "Model-form limitations",
            status: ReviewStatus::RequiresReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
