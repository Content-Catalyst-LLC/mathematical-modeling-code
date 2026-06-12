#[derive(Debug)]
enum VariableRole {
    StateVariable,
    InputVariable,
    OutputVariable,
    Parameter,
    DerivedDiagnostic,
    LatentState,
}

#[derive(Debug)]
enum Observability {
    DirectlyObserved,
    PartiallyObserved,
    ProxyObserved,
    Hidden,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct VariableRecord {
    key: &'static str,
    role: VariableRole,
    unit_label: &'static str,
    observability: Observability,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        VariableRecord {
            key: "storage",
            role: VariableRole::StateVariable,
            unit_label: "resource units",
            observability: Observability::DirectlyObserved,
            status: ReviewStatus::Active,
        },
        VariableRecord {
            key: "demand",
            role: VariableRole::StateVariable,
            unit_label: "resource units per period",
            observability: Observability::PartiallyObserved,
            status: ReviewStatus::RequiresReview,
        },
        VariableRecord {
            key: "infrastructure_condition",
            role: VariableRole::LatentState,
            unit_label: "dimensionless index",
            observability: Observability::ProxyObserved,
            status: ReviewStatus::RequiresValidation,
        },
        VariableRecord {
            key: "shortage",
            role: VariableRole::DerivedDiagnostic,
            unit_label: "resource units",
            observability: Observability::DirectlyObserved,
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
