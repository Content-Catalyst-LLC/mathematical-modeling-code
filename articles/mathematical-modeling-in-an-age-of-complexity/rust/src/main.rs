#[derive(Debug)]
enum ComplexityFeature {
    FeedbackLoops,
    CascadingDependency,
    AdaptiveBehavior,
    DeepUncertainty,
    RobustnessUnderUncertainty,
}

#[derive(Debug)]
enum ComplexityModelFamily {
    SystemDynamics,
    NetworkModel,
    AgentBasedModel,
    ScenarioModeling,
    RobustDecisionAnalysis,
}

#[derive(Debug)]
enum ModelRole {
    DynamicExplanation,
    InterdependenceAnalysis,
    EmergenceAnalysis,
    DeepUncertaintyReview,
    DecisionSupport,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresRevision,
    Archive,
}

#[derive(Debug)]
struct ComplexityModelRecord {
    key: &'static str,
    role: ModelRole,
    family: ComplexityModelFamily,
    feature: ComplexityFeature,
    decision_context: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        ComplexityModelRecord {
            key: "feedback_model",
            role: ModelRole::DynamicExplanation,
            family: ComplexityModelFamily::SystemDynamics,
            feature: ComplexityFeature::FeedbackLoops,
            decision_context: "Understanding nonlinear policy resistance",
            status: ReviewStatus::Active,
        },
        ComplexityModelRecord {
            key: "network_model",
            role: ModelRole::InterdependenceAnalysis,
            family: ComplexityModelFamily::NetworkModel,
            feature: ComplexityFeature::CascadingDependency,
            decision_context: "Identifying systemic risk and fragile bridges",
            status: ReviewStatus::RequiresReview,
        },
        ComplexityModelRecord {
            key: "robustness_model",
            role: ModelRole::DecisionSupport,
            family: ComplexityModelFamily::RobustDecisionAnalysis,
            feature: ComplexityFeature::RobustnessUnderUncertainty,
            decision_context: "Choosing strategies across uncertainty",
            status: ReviewStatus::RequiresReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
