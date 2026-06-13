#[derive(Debug)]
enum SensitivityLayer {
    LocalSensitivity,
    GlobalSensitivity,
    Robustness,
    DecisionSupport,
    ModelForm,
    DataQuality,
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
struct SensitivityRecord {
    key: &'static str,
    layer: SensitivityLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        SensitivityRecord {
            key: "parameter_sweep",
            layer: SensitivityLayer::LocalSensitivity,
            review_focus: "Influential parameters",
            status: ReviewStatus::Active,
        },
        SensitivityRecord {
            key: "threshold_fragility",
            layer: SensitivityLayer::DecisionSupport,
            review_focus: "Decision reversal",
            status: ReviewStatus::RequiresValidation,
        },
        SensitivityRecord {
            key: "scenario_stress",
            layer: SensitivityLayer::Robustness,
            review_focus: "Stress robustness",
            status: ReviewStatus::RequiresReview,
        },
        SensitivityRecord {
            key: "structural_dependence",
            layer: SensitivityLayer::ModelForm,
            review_focus: "Model-form uncertainty",
            status: ReviewStatus::RequiresReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
