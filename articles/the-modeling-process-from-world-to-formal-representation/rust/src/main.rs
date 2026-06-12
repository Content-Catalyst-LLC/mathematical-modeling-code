#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresSensitivityTest,
    RequiresValidation,
}

#[derive(Debug)]
struct ModelingProcessItem {
    stage: &'static str,
    component: &'static str,
    statement: &'static str,
    status: ReviewStatus,
}

fn main() {
    let items = vec![
        ModelingProcessItem {
            stage: "Problem framing",
            component: "Output metric",
            statement: "Shortage risk is the primary scenario-comparison output.",
            status: ReviewStatus::Active,
        },
        ModelingProcessItem {
            stage: "Assumption design",
            component: "Deterministic inflow",
            statement: "Inflow is scenario-based rather than stochastic.",
            status: ReviewStatus::RequiresSensitivityTest,
        },
        ModelingProcessItem {
            stage: "Validation",
            component: "Observed storage",
            statement: "Historical storage observations are required before operational use.",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for item in items {
        println!("{:?}", item);
    }
}
