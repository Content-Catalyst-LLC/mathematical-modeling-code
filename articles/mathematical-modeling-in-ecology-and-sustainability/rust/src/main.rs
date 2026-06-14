#[derive(Debug)]
enum EcologyDomain {
    RenewableResourceManagement,
    EcosystemResilience,
    ClimateAdaptation,
    ConservationPlanning,
    SustainabilityGovernance,
}

#[derive(Debug)]
enum EcologyModelRole {
    StockFlowReview,
    ThresholdReview,
    ScenarioAnalysis,
    NetworkReview,
    AdaptiveManagement,
}

#[derive(Debug)]
enum EcologyModelFamily {
    DynamicResourceModel,
    ResilienceMarginModel,
    StressTestModel,
    BiodiversityDependencyModel,
    MonitoringTriggerModel,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresFieldEvidence,
    RequiresGovernanceReview,
}

#[derive(Debug)]
struct EcologyModelRecord {
    key: &'static str,
    domain: EcologyDomain,
    role: EcologyModelRole,
    family: EcologyModelFamily,
    sustainability_question: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        EcologyModelRecord {
            key: "resource_stock_model",
            domain: EcologyDomain::RenewableResourceManagement,
            role: EcologyModelRole::StockFlowReview,
            family: EcologyModelFamily::DynamicResourceModel,
            sustainability_question: "Does extraction remain within regenerative capacity?",
            status: ReviewStatus::Active,
        },
        EcologyModelRecord {
            key: "resilience_model",
            domain: EcologyDomain::EcosystemResilience,
            role: EcologyModelRole::ThresholdReview,
            family: EcologyModelFamily::ResilienceMarginModel,
            sustainability_question: "How close is the system to a minimum ecological threshold?",
            status: ReviewStatus::RequiresReview,
        },
        EcologyModelRecord {
            key: "governance_model",
            domain: EcologyDomain::SustainabilityGovernance,
            role: EcologyModelRole::AdaptiveManagement,
            family: EcologyModelFamily::MonitoringTriggerModel,
            sustainability_question: "When should management action change as evidence updates?",
            status: ReviewStatus::RequiresGovernanceReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
