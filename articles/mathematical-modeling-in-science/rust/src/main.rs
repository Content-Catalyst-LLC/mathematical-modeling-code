#[derive(Debug)]
enum ScientificDomain {
    Physics,
    Chemistry,
    Biology,
    Ecology,
    EarthSystems,
    Epidemiology,
    ScientificComputing,
}

#[derive(Debug)]
enum ModelRole {
    Explanation,
    Prediction,
    Measurement,
    Simulation,
    ModelComparison,
    UncertaintyQuantification,
}

#[derive(Debug)]
enum ModelFamily {
    Algebraic,
    DifferentialEquation,
    Statistical,
    Stochastic,
    Network,
    Spatial,
    Computational,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresUncertaintyReview,
}

#[derive(Debug)]
struct ScientificModelRecord {
    key: &'static str,
    domain: ScientificDomain,
    role: ModelRole,
    family: ModelFamily,
    evidence_question: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        ScientificModelRecord {
            key: "mechanism_model",
            domain: ScientificDomain::Ecology,
            role: ModelRole::Explanation,
            family: ModelFamily::DifferentialEquation,
            evidence_question: "Can resource limitation explain observed slowing growth?",
            status: ReviewStatus::Active,
        },
        ScientificModelRecord {
            key: "forecast_model",
            domain: ScientificDomain::Biology,
            role: ModelRole::Prediction,
            family: ModelFamily::Computational,
            evidence_question: "What range of population outcomes is plausible after ten years?",
            status: ReviewStatus::RequiresUncertaintyReview,
        },
        ScientificModelRecord {
            key: "comparison_model",
            domain: ScientificDomain::ScientificComputing,
            role: ModelRole::ModelComparison,
            family: ModelFamily::Statistical,
            evidence_question: "Does a logistic model explain observations better than exponential growth?",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
