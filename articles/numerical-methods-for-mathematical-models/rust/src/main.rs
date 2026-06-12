#[derive(Debug)]
enum NumericalComponent {
    TimeStepMethod,
    Discretization,
    SolverTolerance,
    ConvergenceDiagnostic,
    StabilityDiagnostic,
    StateConstraint,
    ValidationDiagnostic,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct NumericalRecord {
    key: &'static str,
    component: NumericalComponent,
    numerical_structure: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        NumericalRecord {
            key: "euler_step",
            component: NumericalComponent::TimeStepMethod,
            numerical_structure: "R_next = R + h * f(R)",
            review_focus: "Method suitability",
            status: ReviewStatus::RequiresReview,
        },
        NumericalRecord {
            key: "step_size",
            component: NumericalComponent::Discretization,
            numerical_structure: "h in {1.0, 0.5, 0.25, 0.1}",
            review_focus: "Step-size sensitivity",
            status: ReviewStatus::RequiresSensitivityTest,
        },
        NumericalRecord {
            key: "convergence_diagnostic",
            component: NumericalComponent::ConvergenceDiagnostic,
            numerical_structure: "compare final stock across h",
            review_focus: "Approximation credibility",
            status: ReviewStatus::Active,
        },
        NumericalRecord {
            key: "nonnegative_constraint",
            component: NumericalComponent::StateConstraint,
            numerical_structure: "R = max(0, R)",
            review_focus: "Constraint interpretation",
            status: ReviewStatus::RequiresReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
