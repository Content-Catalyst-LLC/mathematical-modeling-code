#[derive(Debug)]
enum OptimizationComponent {
    DecisionVariable,
    ObjectiveFunction,
    Constraint,
    Parameter,
    FeasibleRegion,
    SolverSetting,
    ValidationDiagnostic,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct OptimizationRecord {
    key: &'static str,
    component: OptimizationComponent,
    expression: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        OptimizationRecord {
            key: "decision_variables",
            component: OptimizationComponent::DecisionVariable,
            expression: "x_i",
            review_focus: "Controllability",
            status: ReviewStatus::Active,
        },
        OptimizationRecord {
            key: "objective_function",
            component: OptimizationComponent::ObjectiveFunction,
            expression: "maximize sum_i benefit_i * x_i",
            review_focus: "Goal validity and distributional effects",
            status: ReviewStatus::RequiresReview,
        },
        OptimizationRecord {
            key: "budget_constraint",
            component: OptimizationComponent::Constraint,
            expression: "sum_i cost_i * x_i <= B",
            review_focus: "Cost completeness",
            status: ReviewStatus::RequiresReview,
        },
        OptimizationRecord {
            key: "equity_floor",
            component: OptimizationComponent::Constraint,
            expression: "x_i >= floor",
            review_focus: "Equity and feasibility",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
