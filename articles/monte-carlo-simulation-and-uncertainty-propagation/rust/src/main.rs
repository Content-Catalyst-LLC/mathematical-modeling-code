#[derive(Debug)]
enum MonteCarloComponent {
    InputUncertainty,
    SamplingDesign,
    RandomSeedProtocol,
    OutputDistribution,
    RiskMetric,
    ConvergenceDiagnostic,
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
struct MonteCarloRecord {
    key: &'static str,
    component: MonteCarloComponent,
    uncertainty_structure: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        MonteCarloRecord {
            key: "input_distributions",
            component: MonteCarloComponent::InputUncertainty,
            uncertainty_structure: "bounded distributions for stock growth extraction and shocks",
            review_focus: "Distribution justification",
            status: ReviewStatus::RequiresReview,
        },
        MonteCarloRecord {
            key: "sampling_protocol",
            component: MonteCarloComponent::SamplingDesign,
            uncertainty_structure: "pseudo-random independent draws with recorded seed",
            review_focus: "Sampling adequacy",
            status: ReviewStatus::Active,
        },
        MonteCarloRecord {
            key: "threshold_metric",
            component: MonteCarloComponent::RiskMetric,
            uncertainty_structure: "P(final_stock <= depletion_threshold)",
            review_focus: "Threshold appropriateness",
            status: ReviewStatus::RequiresValidation,
        },
        MonteCarloRecord {
            key: "convergence_diagnostic",
            component: MonteCarloComponent::ConvergenceDiagnostic,
            uncertainty_structure: "running mean and threshold probability by replication count",
            review_focus: "Monte Carlo convergence",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
