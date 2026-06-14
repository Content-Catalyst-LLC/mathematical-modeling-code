#[derive(Debug)]
enum PolicyDomain {
    PublicSystems,
    PublicPlanning,
    ResourceAllocation,
    PublicAccountability,
    InstitutionalGovernance,
}

#[derive(Debug)]
enum PolicyModelRole {
    ProblemFraming,
    Forecasting,
    OptionComparison,
    DistributionalReview,
    ModelGovernance,
    PublicCommunication,
}

#[derive(Debug)]
enum PolicyModelFamily {
    SystemsMap,
    ScenarioForecast,
    ConstrainedDecisionModel,
    EquityDiagnostic,
    ReviewRegister,
    ImpactEvaluation,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresEquityReview,
    RequiresGovernanceReview,
}

#[derive(Debug)]
struct PolicyModelRecord {
    key: &'static str,
    domain: PolicyDomain,
    role: PolicyModelRole,
    family: PolicyModelFamily,
    public_question: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        PolicyModelRecord {
            key: "problem_model",
            domain: PolicyDomain::PublicSystems,
            role: PolicyModelRole::ProblemFraming,
            family: PolicyModelFamily::SystemsMap,
            public_question: "What drivers and boundaries define the public problem?",
            status: ReviewStatus::Active,
        },
        PolicyModelRecord {
            key: "equity_model",
            domain: PolicyDomain::PublicAccountability,
            role: PolicyModelRole::DistributionalReview,
            family: PolicyModelFamily::EquityDiagnostic,
            public_question: "How are benefits and burdens distributed across groups or places?",
            status: ReviewStatus::RequiresEquityReview,
        },
        PolicyModelRecord {
            key: "governance_model",
            domain: PolicyDomain::InstitutionalGovernance,
            role: PolicyModelRole::ModelGovernance,
            family: PolicyModelFamily::ReviewRegister,
            public_question: "Who owns the model, decision, update process, and challenge pathway?",
            status: ReviewStatus::RequiresGovernanceReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
