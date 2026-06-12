#[derive(Debug)]
enum RelationshipType {
    Linear,
    Nonlinear,
    Dynamic,
    Stochastic,
    Feedback,
    Constraint,
    Networked,
    Optimization,
}

#[derive(Debug)]
enum StructureStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct RelationshipRecord {
    key: &'static str,
    relationship_type: RelationshipType,
    expression: &'static str,
    assumption: &'static str,
    status: StructureStatus,
}

fn main() {
    let records = vec![
        RelationshipRecord {
            key: "linear_update",
            relationship_type: RelationshipType::Dynamic,
            expression: "S[t+1] = S[t] + I[t] - D[t] - lambda*S[t]",
            assumption: "loss is proportional; demand is exogenous",
            status: StructureStatus::Active,
        },
        RelationshipRecord {
            key: "constrained_update",
            relationship_type: RelationshipType::Constraint,
            expression: "S[t+1] = min(K, max(0, raw_next_stock))",
            assumption: "constraints must not hide shortage or overflow",
            status: StructureStatus::RequiresReview,
        },
        RelationshipRecord {
            key: "feedback_demand",
            relationship_type: RelationshipType::Feedback,
            expression: "D[t+1] = max(0, D[t] - alpha*shortage[t])",
            assumption: "feedback is immediate and proportional",
            status: StructureStatus::RequiresValidation,
        },
        RelationshipRecord {
            key: "stochastic_inflow",
            relationship_type: RelationshipType::Stochastic,
            expression: "I[t] = I_bar * exp(epsilon[t])",
            assumption: "random shocks require evidence",
            status: StructureStatus::RequiresSensitivityTest,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
