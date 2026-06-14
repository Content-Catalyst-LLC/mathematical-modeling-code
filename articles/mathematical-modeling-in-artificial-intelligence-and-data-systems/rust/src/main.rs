#[derive(Debug)]
enum AIModelRole {
    Prediction,
    Classification,
    Ranking,
    Generation,
    Monitoring,
    Governance,
}

#[derive(Debug)]
enum AIModelFamily {
    SupervisedLearning,
    LearningToRank,
    LanguageModel,
    DriftDetection,
    ModelCardAndAuditRegister,
}

#[derive(Debug)]
enum DataDomain {
    StructuredRecords,
    RecommendationLogs,
    TextCorpus,
    DeploymentStreams,
    ModelLifecycleRecords,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresBiasReview,
    RequiresPrivacyReview,
    RequiresDeploymentReview,
}

#[derive(Debug)]
struct AIModelRecord {
    key: &'static str,
    role: AIModelRole,
    family: AIModelFamily,
    data_domain: DataDomain,
    decision_context: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        AIModelRecord {
            key: "prediction_model",
            role: AIModelRole::Prediction,
            family: AIModelFamily::SupervisedLearning,
            data_domain: DataDomain::StructuredRecords,
            decision_context: "Risk scoring with human review",
            status: ReviewStatus::Active,
        },
        AIModelRecord {
            key: "ranking_model",
            role: AIModelRole::Ranking,
            family: AIModelFamily::LearningToRank,
            data_domain: DataDomain::RecommendationLogs,
            decision_context: "Prioritization and visibility",
            status: ReviewStatus::RequiresBiasReview,
        },
        AIModelRecord {
            key: "governance_model",
            role: AIModelRole::Governance,
            family: AIModelFamily::ModelCardAndAuditRegister,
            data_domain: DataDomain::ModelLifecycleRecords,
            decision_context: "Accountability and review",
            status: ReviewStatus::RequiresPrivacyReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
