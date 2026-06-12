#[derive(Debug)]
enum BoundaryType {
    Physical,
    Temporal,
    Population,
    Decision,
    Uncertainty,
}

#[derive(Debug)]
enum ScopeStatus {
    SupportedUse,
    ExploratoryUse,
    RequiresValidation,
    ProhibitedUse,
}

#[derive(Debug)]
struct BoundaryRecord {
    key: &'static str,
    boundary_type: BoundaryType,
    excluded: &'static str,
    scope_status: ScopeStatus,
}

fn main() {
    let records = vec![
        BoundaryRecord {
            key: "physical_stock_boundary",
            boundary_type: BoundaryType::Physical,
            excluded: "spatial distribution, quality, local access",
            scope_status: ScopeStatus::SupportedUse,
        },
        BoundaryRecord {
            key: "time_horizon_boundary",
            boundary_type: BoundaryType::Temporal,
            excluded: "long-term infrastructure change and regime shifts",
            scope_status: ScopeStatus::RequiresValidation,
        },
        BoundaryRecord {
            key: "population_boundary",
            boundary_type: BoundaryType::Population,
            excluded: "user groups, access differences, vulnerable populations",
            scope_status: ScopeStatus::RequiresValidation,
        },
        BoundaryRecord {
            key: "policy_boundary",
            boundary_type: BoundaryType::Decision,
            excluded: "implementation capacity, compliance, enforcement, equity",
            scope_status: ScopeStatus::ExploratoryUse,
        },
        BoundaryRecord {
            key: "uncertainty_boundary",
            boundary_type: BoundaryType::Uncertainty,
            excluded: "probabilistic inflow, demand variability, extreme events",
            scope_status: ScopeStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
