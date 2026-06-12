#[derive(Debug)]
enum ProbabilityComponent {
    RandomVariable,
    DistributionChoice,
    ParameterUncertainty,
    DerivedRiskMeasure,
    ConditionalStatement,
    SimulationSetting,
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
struct ProbabilityRecord {
    key: &'static str,
    component: ProbabilityComponent,
    expression: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        ProbabilityRecord {
            key: "demand_distribution",
            component: ProbabilityComponent::RandomVariable,
            expression: "D ~ Lognormal(mu, sigma)",
            review_focus: "Tail behavior and evidence",
            status: ReviewStatus::RequiresReview,
        },
        ProbabilityRecord {
            key: "supply_distribution",
            component: ProbabilityComponent::DistributionChoice,
            expression: "S ~ Normal(mean, sd), truncated at zero",
            review_focus: "Support and truncation",
            status: ReviewStatus::RequiresReview,
        },
        ProbabilityRecord {
            key: "shortage_amount",
            component: ProbabilityComponent::DerivedRiskMeasure,
            expression: "Q = max(0, D - S - reserve)",
            review_focus: "Probability and severity",
            status: ReviewStatus::Active,
        },
        ProbabilityRecord {
            key: "simulation_count",
            component: ProbabilityComponent::SimulationSetting,
            expression: "M",
            review_focus: "Stability of estimated risk",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
