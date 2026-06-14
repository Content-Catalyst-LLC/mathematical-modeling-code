#[derive(Debug)]
enum ModelStage {
    Framing,
    DataReview,
    Design,
    Validation,
    Communication,
    Deployment,
    Monitoring,
    Governance,
}

#[derive(Debug)]
enum FailureMode {
    BoundaryFailure,
    DataBias,
    ValidationGap,
    FalsePrecision,
    ScopeCreep,
    AccountabilityGap,
}

#[derive(Debug)]
enum EthicalIssue {
    HiddenConsequences,
    UnequalError,
    UnsupportedAuthority,
    Overconfidence,
    Misuse,
    ResponsibilityShifting,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresRevision,
    Retire,
}

#[derive(Debug)]
struct ModelEthicsRecord {
    key: &'static str,
    stage: ModelStage,
    failure_mode: FailureMode,
    ethical_issue: EthicalIssue,
    use_limit_required: bool,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        ModelEthicsRecord {
            key: "boundary_failure",
            stage: ModelStage::Design,
            failure_mode: FailureMode::BoundaryFailure,
            ethical_issue: EthicalIssue::HiddenConsequences,
            use_limit_required: true,
            status: ReviewStatus::RequiresReview,
        },
        ModelEthicsRecord {
            key: "validation_gap",
            stage: ModelStage::Validation,
            failure_mode: FailureMode::ValidationGap,
            ethical_issue: EthicalIssue::UnsupportedAuthority,
            use_limit_required: true,
            status: ReviewStatus::RequiresReview,
        },
        ModelEthicsRecord {
            key: "accountability_gap",
            stage: ModelStage::Governance,
            failure_mode: FailureMode::AccountabilityGap,
            ethical_issue: EthicalIssue::ResponsibilityShifting,
            use_limit_required: true,
            status: ReviewStatus::RequiresRevision,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
