#[derive(Debug)]
enum GeneralizationLayer {
    EvidenceSplit,
    OverfitDiagnostic,
    UnderfitDiagnostic,
    ComplexityReview,
    DistributionShift,
    DecisionThreshold,
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
struct GeneralizationRecord {
    key: &'static str,
    layer: GeneralizationLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        GeneralizationRecord {
            key: "training_validation_split",
            layer: GeneralizationLayer::EvidenceSplit,
            review_focus: "Evidence separation",
            status: ReviewStatus::Active,
        },
        GeneralizationRecord {
            key: "overfit_gap",
            layer: GeneralizationLayer::OverfitDiagnostic,
            review_focus: "Noise memorization",
            status: ReviewStatus::RequiresReview,
        },
        GeneralizationRecord {
            key: "underfit_check",
            layer: GeneralizationLayer::UnderfitDiagnostic,
            review_focus: "Missing structure",
            status: ReviewStatus::RequiresReview,
        },
        GeneralizationRecord {
            key: "distribution_shift",
            layer: GeneralizationLayer::DistributionShift,
            review_focus: "Transfer limits",
            status: ReviewStatus::RequiresMonitoring,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
