#[derive(Debug)]
enum NetworkComponent {
    NodeDefinition,
    EdgeDefinition,
    EdgeWeight,
    DirectionRule,
    CentralityDiagnostic,
    ProcessRule,
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
struct NetworkRecord {
    key: &'static str,
    component: NetworkComponent,
    expression: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        NetworkRecord { key: "node_definition", component: NetworkComponent::NodeDefinition, expression: "V", review_focus: "Boundary and scale", status: ReviewStatus::RequiresReview },
        NetworkRecord { key: "directed_dependency_edge", component: NetworkComponent::EdgeDefinition, expression: "source -> target", review_focus: "Direction and evidence quality", status: ReviewStatus::RequiresReview },
        NetworkRecord { key: "edge_weight", component: NetworkComponent::EdgeWeight, expression: "w_ij", review_focus: "Weight estimation and validation", status: ReviewStatus::RequiresValidation },
        NetworkRecord { key: "centrality_diagnostic", component: NetworkComponent::CentralityDiagnostic, expression: "in_degree, out_degree, reachability", review_focus: "Practical meaning of centrality", status: ReviewStatus::Active },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
