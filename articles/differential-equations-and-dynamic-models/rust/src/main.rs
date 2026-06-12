#[derive(Debug)]
enum DynamicComponent {
    StateVariable,
    RateEquation,
    InitialCondition,
    BoundaryCondition,
    Parameter,
    NumericalSetting,
    OutputDiagnostic,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct DynamicRecord {
    key: &'static str,
    component: DynamicComponent,
    expression: &'static str,
    units_or_domain: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        DynamicRecord {
            key: "storage",
            component: DynamicComponent::StateVariable,
            expression: "S(t)",
            units_or_domain: "resource units",
            status: ReviewStatus::Active,
        },
        DynamicRecord {
            key: "storage_rate",
            component: DynamicComponent::RateEquation,
            expression: "dS/dt = I - D - lambda*S",
            units_or_domain: "resource units per time",
            status: ReviewStatus::RequiresReview,
        },
        DynamicRecord {
            key: "initial_storage",
            component: DynamicComponent::InitialCondition,
            expression: "S(0) = S0",
            units_or_domain: "0 <= S0 <= K",
            status: ReviewStatus::RequiresValidation,
        },
        DynamicRecord {
            key: "time_step",
            component: DynamicComponent::NumericalSetting,
            expression: "dt",
            units_or_domain: "positive time increment",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
