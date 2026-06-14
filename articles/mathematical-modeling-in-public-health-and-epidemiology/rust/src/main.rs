#[derive(Debug)]
enum PublicHealthDomain {
    InfectiousDisease,
    PublicHealthSurveillance,
    HealthSystemPlanning,
    HealthEquity,
    PublicCommunication,
}

#[derive(Debug)]
enum PublicHealthModelRole {
    TransmissionAnalysis,
    DataInterpretation,
    CapacityReview,
    DistributionalReview,
    UncertaintyCommunication,
}

#[derive(Debug)]
enum PublicHealthModelFamily {
    SIRCompartmentalModel,
    NowcastingAndReportingDelayModel,
    HospitalDemandModel,
    SubgroupRiskModel,
    ScenarioSummaryModel,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresEquityReview,
    RequiresSurveillanceReview,
    RequiresCommunicationReview,
}

#[derive(Debug)]
struct PublicHealthModelRecord {
    key: &'static str,
    domain: PublicHealthDomain,
    role: PublicHealthModelRole,
    family: PublicHealthModelFamily,
    public_health_question: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        PublicHealthModelRecord {
            key: "transmission_model",
            domain: PublicHealthDomain::InfectiousDisease,
            role: PublicHealthModelRole::TransmissionAnalysis,
            family: PublicHealthModelFamily::SIRCompartmentalModel,
            public_health_question: "How does transmission change under different intervention assumptions?",
            status: ReviewStatus::Active,
        },
        PublicHealthModelRecord {
            key: "capacity_model",
            domain: PublicHealthDomain::HealthSystemPlanning,
            role: PublicHealthModelRole::CapacityReview,
            family: PublicHealthModelFamily::HospitalDemandModel,
            public_health_question: "Could projected severe cases exceed healthcare capacity?",
            status: ReviewStatus::RequiresReview,
        },
        PublicHealthModelRecord {
            key: "equity_model",
            domain: PublicHealthDomain::HealthEquity,
            role: PublicHealthModelRole::DistributionalReview,
            family: PublicHealthModelFamily::SubgroupRiskModel,
            public_health_question: "Which populations face unequal exposure, severity, or access?",
            status: ReviewStatus::RequiresEquityReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
