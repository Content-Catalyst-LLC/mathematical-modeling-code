#[derive(Debug)]
enum StructuralLayer {
    ModelFamily,
    FunctionalForm,
    BoundaryChoice,
    AggregationChoice,
    ScaleChoice,
    RegimeBehavior,
    Governance,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresComparison,
    RequiresValidation,
}

#[derive(Debug)]
struct StructuralRecord {
    key: &'static str,
    layer: StructuralLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        StructuralRecord {
            key: "model_family_choice",
            layer: StructuralLayer::ModelFamily,
            review_focus: "Does the conclusion depend on the model family?",
            status: ReviewStatus::RequiresComparison,
        },
        StructuralRecord {
            key: "functional_form",
            layer: StructuralLayer::FunctionalForm,
            review_focus: "Does the equation form distort system behavior?",
            status: ReviewStatus::RequiresReview,
        },
        StructuralRecord {
            key: "boundary_choice",
            layer: StructuralLayer::BoundaryChoice,
            review_focus: "Could excluded drivers change the conclusion?",
            status: ReviewStatus::RequiresReview,
        },
        StructuralRecord {
            key: "threshold_regime",
            layer: StructuralLayer::RegimeBehavior,
            review_focus: "Could regime shift invalidate the baseline structure?",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
