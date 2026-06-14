#[derive(Debug, PartialEq)]
enum RiskTier {
    Low,
    Medium,
    High,
    Critical,
}

#[derive(Debug, PartialEq)]
enum ValidationStatus {
    NotValidated,
    ReviewRequired,
    ValidatedWithLimits,
    Retired,
}

#[derive(Debug, PartialEq)]
enum UseLimitStatus {
    NotApproved,
    Draft,
    Approved,
    ApprovedWithLimits,
}

#[derive(Debug, PartialEq)]
enum MonitoringStatus {
    Pending,
    Active,
    IncidentReview,
    Retired,
}

#[derive(Debug)]
struct ModelGovernanceRecord {
    key: &'static str,
    model_name: &'static str,
    risk_tier: RiskTier,
    validation_status: ValidationStatus,
    use_limit_status: UseLimitStatus,
    monitoring_status: MonitoringStatus,
    model_owner: &'static str,
    decision_owner: &'static str,
}

fn requires_review(record: &ModelGovernanceRecord) -> bool {
    record.validation_status != ValidationStatus::ValidatedWithLimits
        || record.use_limit_status == UseLimitStatus::NotApproved
        || record.monitoring_status != MonitoringStatus::Active
        || record.risk_tier == RiskTier::Critical
}

fn main() {
    let records = vec![
        ModelGovernanceRecord {
            key: "infrastructure_risk",
            model_name: "Infrastructure risk prioritization model",
            risk_tier: RiskTier::High,
            validation_status: ValidationStatus::ValidatedWithLimits,
            use_limit_status: UseLimitStatus::ApprovedWithLimits,
            monitoring_status: MonitoringStatus::Active,
            model_owner: "infrastructure analytics team",
            decision_owner: "capital planning office",
        },
        ModelGovernanceRecord {
            key: "ai_triage_support",
            model_name: "AI-assisted triage support model",
            risk_tier: RiskTier::Critical,
            validation_status: ValidationStatus::ReviewRequired,
            use_limit_status: UseLimitStatus::NotApproved,
            monitoring_status: MonitoringStatus::Pending,
            model_owner: "clinical analytics team",
            decision_owner: "clinical governance board",
        },
    ];

    for record in records {
        println!("{:?} requires_review={}", record, requires_review(&record));
    }
}
