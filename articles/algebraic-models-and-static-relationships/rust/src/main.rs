#[derive(Debug)]
enum RelationshipType {
    Identity,
    LinearRelationship,
    NonlinearRelationship,
    InequalityConstraint,
    ObjectiveFunction,
    RatioDefinition,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct AlgebraicRelationship {
    key: &'static str,
    relationship_type: RelationshipType,
    expression: &'static str,
    domain_or_constraint: &'static str,
    status: ReviewStatus,
}

fn main() {
    let relationships = vec![
        AlgebraicRelationship {
            key: "total_cost",
            relationship_type: RelationshipType::Identity,
            expression: "C = c_a*x_a + c_b*x_b",
            domain_or_constraint: "x_a >= 0, x_b >= 0",
            status: ReviewStatus::Active,
        },
        AlgebraicRelationship {
            key: "budget_constraint",
            relationship_type: RelationshipType::InequalityConstraint,
            expression: "c_a*x_a + c_b*x_b <= B",
            domain_or_constraint: "B > 0",
            status: ReviewStatus::RequiresReview,
        },
        AlgebraicRelationship {
            key: "benefit_objective",
            relationship_type: RelationshipType::ObjectiveFunction,
            expression: "V = b_a*x_a + b_b*x_b",
            domain_or_constraint: "benefit units must be comparable",
            status: ReviewStatus::RequiresValidation,
        },
        AlgebraicRelationship {
            key: "benefit_per_cost",
            relationship_type: RelationshipType::RatioDefinition,
            expression: "r = V / C",
            domain_or_constraint: "C > 0",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for relationship in relationships {
        println!("{:?}", relationship);
    }
}
