#[derive(Debug)]
enum RecurrenceComponent {
    StateVariable,
    UpdateRule,
    InitialCondition,
    BoundaryRule,
    Parameter,
    OutputDiagnostic,
    StepDefinition,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct RecurrenceRecord {
    key: &'static str,
    component: RecurrenceComponent,
    expression: &'static str,
    domain_or_step: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        RecurrenceRecord {
            key: "storage",
            component: RecurrenceComponent::StateVariable,
            expression: "S_t",
            domain_or_step: "0 <= S_t <= K",
            status: ReviewStatus::Active,
        },
        RecurrenceRecord {
            key: "storage_update",
            component: RecurrenceComponent::UpdateRule,
            expression: "S[t+1] = min(K, max(0, S[t] + I[t] - D[t] - lambda*S[t]))",
            domain_or_step: "one period",
            status: ReviewStatus::RequiresReview,
        },
        RecurrenceRecord {
            key: "initial_storage",
            component: RecurrenceComponent::InitialCondition,
            expression: "S_0",
            domain_or_step: "0 <= S_0 <= K",
            status: ReviewStatus::RequiresValidation,
        },
        RecurrenceRecord {
            key: "shortage",
            component: RecurrenceComponent::OutputDiagnostic,
            expression: "Q[t] = max(0, -raw_next_storage)",
            domain_or_step: "reported each period",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
