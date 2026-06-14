#[derive(Debug)]
enum CommunicationLayer {
    CentralResult,
    UncertaintyRange,
    ScenarioMessage,
    ThresholdRisk,
    StructuralLimit,
    UseLimit,
    Governance,
}

#[derive(Debug)]
enum Audience {
    TechnicalReviewer,
    DecisionMaker,
    PublicAudience,
    FutureUser,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresPlainLanguage,
    RequiresDecisionContext,
}

#[derive(Debug)]
struct CommunicationRecord {
    key: &'static str,
    layer: CommunicationLayer,
    audience: Audience,
    message_goal: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        CommunicationRecord {
            key: "central_result",
            layer: CommunicationLayer::CentralResult,
            audience: Audience::DecisionMaker,
            message_goal: "State the baseline result without overstating certainty.",
            status: ReviewStatus::Active,
        },
        CommunicationRecord {
            key: "uncertainty_range",
            layer: CommunicationLayer::UncertaintyRange,
            audience: Audience::PublicAudience,
            message_goal: "Explain plausible output variation in plain language.",
            status: ReviewStatus::RequiresPlainLanguage,
        },
        CommunicationRecord {
            key: "threshold_risk",
            layer: CommunicationLayer::ThresholdRisk,
            audience: Audience::DecisionMaker,
            message_goal: "Explain whether uncertainty could reverse action.",
            status: ReviewStatus::RequiresDecisionContext,
        },
        CommunicationRecord {
            key: "use_limit",
            layer: CommunicationLayer::UseLimit,
            audience: Audience::FutureUser,
            message_goal: "Prevent use beyond validation domain.",
            status: ReviewStatus::RequiresReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
