#[derive(Debug)]
enum CalibrationLayer {
    Evidence,
    ParameterSpace,
    LossFunction,
    Optimization,
    ResidualDiagnostic,
    ParameterUncertainty,
    Validation,
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
struct CalibrationRecord {
    key: &'static str,
    layer: CalibrationLayer,
    diagnostic_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        CalibrationRecord {
            key: "calibration_data",
            layer: CalibrationLayer::Evidence,
            diagnostic_focus: "Data relevance and measurement error",
            status: ReviewStatus::RequiresReview,
        },
        CalibrationRecord {
            key: "objective_function",
            layer: CalibrationLayer::LossFunction,
            diagnostic_focus: "Loss-function appropriateness",
            status: ReviewStatus::RequiresReview,
        },
        CalibrationRecord {
            key: "residual_diagnostics",
            layer: CalibrationLayer::ResidualDiagnostic,
            diagnostic_focus: "Residual structure",
            status: ReviewStatus::Active,
        },
        CalibrationRecord {
            key: "validation_split",
            layer: CalibrationLayer::Validation,
            diagnostic_focus: "Generalization",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
