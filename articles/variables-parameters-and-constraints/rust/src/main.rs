#[derive(Debug)] enum ComponentType { StateVariable, InputVariable, OutputVariable, DecisionVariable, Parameter, Constraint, DerivedVariable }
#[derive(Debug)] enum ReviewStatus { Active, RequiresReview, RequiresSensitivityTest, RequiresValidation }
#[derive(Debug)] struct ModelComponent { symbol: &'static str, component_type: ComponentType, domain: &'static str, interpretation: &'static str, status: ReviewStatus }
fn main() {
    let components = vec![
        ModelComponent { symbol:"S_t", component_type:ComponentType::StateVariable, domain:"0 <= S_t <= K", interpretation:"Stored resource at time t.", status:ReviewStatus::Active },
        ModelComponent { symbol:"I_t", component_type:ComponentType::InputVariable, domain:"nonnegative real", interpretation:"Resource entering the system.", status:ReviewStatus::RequiresReview },
        ModelComponent { symbol:"D_t", component_type:ComponentType::InputVariable, domain:"nonnegative real", interpretation:"Resource requested or consumed.", status:ReviewStatus::RequiresReview },
        ModelComponent { symbol:"lambda", component_type:ComponentType::Parameter, domain:"[0,1]", interpretation:"Proportional loss rate.", status:ReviewStatus::RequiresSensitivityTest },
        ModelComponent { symbol:"K", component_type:ComponentType::Constraint, domain:"positive real", interpretation:"Maximum storage capacity.", status:ReviewStatus::RequiresValidation },
    ];
    for c in components { println!("{:?}", c); }
}
