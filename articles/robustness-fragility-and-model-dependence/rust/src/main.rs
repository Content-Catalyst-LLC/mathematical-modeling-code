#[derive(Debug)]
enum DependenceLayer {
    ParameterDependence,
    StructuralDependence,
    ScenarioDependence,
    ThresholdFragility,
    DataDependence,
    MetricDependence,
    Governance,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresStressTest,
    RequiresComparison,
}

#[derive(Debug)]
struct RobustnessRecord {
    key: &'static str,
    layer: DependenceLayer,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        RobustnessRecord {
            key: "parameter_dependence",
            layer: DependenceLayer::ParameterDependence,
            review_focus: "Do parameter changes reverse the conclusion?",
            status: ReviewStatus::RequiresReview,
        },
        RobustnessRecord {
            key: "structural_dependence",
            layer: DependenceLayer::StructuralDependence,
            review_focus: "Do plausible model forms disagree?",
            status: ReviewStatus::RequiresComparison,
        },
        RobustnessRecord {
            key: "scenario_dependence",
            layer: DependenceLayer::ScenarioDependence,
            review_focus: "Does the recommendation hold under stress?",
            status: ReviewStatus::RequiresStressTest,
        },
        RobustnessRecord {
            key: "threshold_fragility",
            layer: DependenceLayer::ThresholdFragility,
            review_focus: "How close is the output to decision reversal?",
            status: ReviewStatus::RequiresReview,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
