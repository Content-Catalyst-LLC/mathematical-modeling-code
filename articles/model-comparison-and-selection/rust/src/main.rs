#[derive(Debug)]
enum SelectionLayer {
    Alternatives,
    Generalization,
    Parsimony,
    Communication,
    Uncertainty,
    DecisionSupport,
    Governance,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresUncertaintyCheck,
}

#[derive(Debug)]
struct SelectionRecord {
    key: &'static str,
    layer: SelectionLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        SelectionRecord {
            key: "candidate_set",
            layer: SelectionLayer::Alternatives,
            review_focus: "Plausible baselines and alternatives",
            status: ReviewStatus::RequiresReview,
        },
        SelectionRecord {
            key: "validation_error",
            layer: SelectionLayer::Generalization,
            review_focus: "Generalization",
            status: ReviewStatus::Active,
        },
        SelectionRecord {
            key: "robustness",
            layer: SelectionLayer::Uncertainty,
            review_focus: "Uncertainty-aware selection",
            status: ReviewStatus::RequiresUncertaintyCheck,
        },
        SelectionRecord {
            key: "decision_relevance",
            layer: SelectionLayer::DecisionSupport,
            review_focus: "Fitness for purpose",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
