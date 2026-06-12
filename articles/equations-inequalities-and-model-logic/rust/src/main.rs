#[derive(Debug)]
enum StatementType {
    Equation,
    Inequality,
    DomainRule,
    Definition,
    ConditionalRule,
    ObjectiveRule,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSensitivityTest,
}

#[derive(Debug)]
struct FormalStatement {
    key: &'static str,
    statement_type: StatementType,
    expression: &'static str,
    condition: &'static str,
    status: ReviewStatus,
}

fn main() {
    let statements = vec![
        FormalStatement {
            key: "storage_balance",
            statement_type: StatementType::Equation,
            expression: "S[t+1] = S[t] + I[t] - D[t] - lambda*S[t]",
            condition: "0 <= S[t], 0 <= lambda <= 1",
            status: ReviewStatus::Active,
        },
        FormalStatement {
            key: "storage_bounds",
            statement_type: StatementType::Inequality,
            expression: "0 <= S[t] <= K",
            condition: "K > 0",
            status: ReviewStatus::RequiresReview,
        },
        FormalStatement {
            key: "shortage_definition",
            statement_type: StatementType::Definition,
            expression: "Q[t] = max(0, demand + loss - available)",
            condition: "Q[t] >= 0",
            status: ReviewStatus::RequiresValidation,
        },
        FormalStatement {
            key: "low_storage_rule",
            statement_type: StatementType::ConditionalRule,
            expression: "if S[t] < T then reduce demand",
            condition: "0 <= T <= K",
            status: ReviewStatus::RequiresSensitivityTest,
        },
    ];

    for statement in statements {
        println!("{:?}", statement);
    }
}
