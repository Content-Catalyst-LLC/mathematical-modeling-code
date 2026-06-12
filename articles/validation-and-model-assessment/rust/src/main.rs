#[derive(Debug)]
enum ValidationLayer {
    ConceptualValidity,
    Verification,
    EvidenceQuality,
    Diagnostics,
    Generalization,
    UncertaintyReview,
    DecisionSupport,
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
struct ValidationRecord {
    key: &'static str,
    layer: ValidationLayer,
    assessment_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        ValidationRecord {
            key: "conceptual_validity",
            layer: ValidationLayer::ConceptualValidity,
            assessment_focus: "Model-system fit",
            status: ReviewStatus::RequiresReview,
        },
        ValidationRecord {
            key: "implementation_verification",
            layer: ValidationLayer::Verification,
            assessment_focus: "Implementation correctness",
            status: ReviewStatus::Active,
        },
        ValidationRecord {
            key: "residual_diagnostics",
            layer: ValidationLayer::Diagnostics,
            assessment_focus: "Systematic model error",
            status: ReviewStatus::Active,
        },
        ValidationRecord {
            key: "fitness_for_purpose",
            layer: ValidationLayer::DecisionSupport,
            assessment_focus: "Purpose-specific credibility",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
