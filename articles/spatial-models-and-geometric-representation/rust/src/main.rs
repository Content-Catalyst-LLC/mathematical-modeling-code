#[derive(Debug)]
enum SpatialComponent {
    GeometryDefinition,
    CoordinateSystem,
    DistanceMetric,
    NeighborhoodRule,
    AccessibilityMetric,
    SpatialField,
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
struct SpatialRecord {
    key: &'static str,
    component: SpatialComponent,
    geometry_or_structure: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        SpatialRecord {
            key: "point_geometry",
            component: SpatialComponent::GeometryDefinition,
            geometry_or_structure: "p=(x,y)",
            review_focus: "Geometry simplification",
            status: ReviewStatus::RequiresReview,
        },
        SpatialRecord {
            key: "euclidean_distance",
            component: SpatialComponent::DistanceMetric,
            geometry_or_structure: "sqrt((x_i-x_j)^2+(y_i-y_j)^2)",
            review_focus: "Distance validity",
            status: ReviewStatus::RequiresReview,
        },
        SpatialRecord {
            key: "service_access",
            component: SpatialComponent::AccessibilityMetric,
            geometry_or_structure: "capacity / (1 + distance)",
            review_focus: "Decision relevance",
            status: ReviewStatus::RequiresValidation,
        },
        SpatialRecord {
            key: "spatial_uncertainty",
            component: SpatialComponent::ValidationDiagnostic,
            geometry_or_structure: "distance and boundary sensitivity",
            review_focus: "Uncertainty communication",
            status: ReviewStatus::Active,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
