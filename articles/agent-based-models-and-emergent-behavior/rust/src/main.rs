#[derive(Debug)]
enum ABMComponent {
    AgentState,
    BehaviorRule,
    InteractionStructure,
    EnvironmentDefinition,
    ScheduleRule,
    EmergenceDiagnostic,
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
struct ABMRecord {
    key: &'static str,
    component: ABMComponent,
    rule_or_structure: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        ABMRecord {
            key: "agent_state",
            component: ABMComponent::AgentState,
            rule_or_structure: "adopted in {0,1}",
            review_focus: "State simplification",
            status: ReviewStatus::RequiresReview,
        },
        ABMRecord {
            key: "threshold_rule",
            component: ABMComponent::BehaviorRule,
            rule_or_structure: "adopt if adopted_neighbors_share >= threshold",
            review_focus: "Behavioral evidence",
            status: ReviewStatus::RequiresReview,
        },
        ABMRecord {
            key: "ring_network",
            component: ABMComponent::InteractionStructure,
            rule_or_structure: "two neighbors on each side",
            review_focus: "Interaction validity",
            status: ReviewStatus::RequiresValidation,
        },
        ABMRecord {
            key: "ensemble_replication",
            component: ABMComponent::ValidationDiagnostic,
            rule_or_structure: "multiple random seeds",
            review_focus: "Stochastic robustness",
            status: ReviewStatus::Active,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
