#[derive(Debug)]
enum SimulationComponent {
    StateDefinition,
    UpdateRule,
    NumericalMethod,
    ScenarioDefinition,
    StochasticProtocol,
    OutputMetric,
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
struct SimulationRecord {
    key: &'static str,
    component: SimulationComponent,
    computational_structure: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        SimulationRecord {
            key: "state_variable",
            component: SimulationComponent::StateDefinition,
            computational_structure: "resource_stock",
            review_focus: "State definition",
            status: ReviewStatus::RequiresReview,
        },
        SimulationRecord {
            key: "update_rule",
            component: SimulationComponent::UpdateRule,
            computational_structure: "R_next = R + growth - extraction - shock",
            review_focus: "Equation-code alignment",
            status: ReviewStatus::RequiresValidation,
        },
        SimulationRecord {
            key: "time_step",
            component: SimulationComponent::NumericalMethod,
            computational_structure: "discrete annual step",
            review_focus: "Numerical appropriateness",
            status: ReviewStatus::RequiresReview,
        },
        SimulationRecord {
            key: "ensemble_protocol",
            component: SimulationComponent::StochasticProtocol,
            computational_structure: "multiple random seeds per scenario",
            review_focus: "Replication adequacy",
            status: ReviewStatus::Active,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
