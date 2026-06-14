#[derive(Debug)]
enum InterpretationLayer {
    OutputMeaning,
    UncertaintyMeaning,
    ThresholdReview,
    ValueTradeoff,
    GovernanceReview,
    Communication,
}

#[derive(Debug)]
enum DecisionRole {
    Evidence,
    ReviewRequired,
    HumanJudgmentRequired,
    GovernanceRequired,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresDecisionContext,
    RequiresGovernance,
}

#[derive(Debug)]
struct InterpretationRecord {
    key: &'static str,
    layer: InterpretationLayer,
    role: DecisionRole,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        InterpretationRecord {
            key: "output_meaning",
            layer: InterpretationLayer::OutputMeaning,
            role: DecisionRole::Evidence,
            review_focus: "What claim is being made from the model output?",
            status: ReviewStatus::Active,
        },
        InterpretationRecord {
            key: "uncertainty_meaning",
            layer: InterpretationLayer::UncertaintyMeaning,
            role: DecisionRole::ReviewRequired,
            review_focus: "Could uncertainty change the decision?",
            status: ReviewStatus::RequiresReview,
        },
        InterpretationRecord {
            key: "threshold_review",
            layer: InterpretationLayer::ThresholdReview,
            role: DecisionRole::ReviewRequired,
            review_focus: "Does the result cross or approach the threshold?",
            status: ReviewStatus::RequiresDecisionContext,
        },
        InterpretationRecord {
            key: "governance_review",
            layer: InterpretationLayer::GovernanceReview,
            role: DecisionRole::GovernanceRequired,
            review_focus: "Who owns the decision and monitoring plan?",
            status: ReviewStatus::RequiresGovernance,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
