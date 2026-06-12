#[derive(Debug)]
enum RepositoryLayer {
    Documentation,
    DataLayer,
    CodeLayer,
    Metadata,
    Reproducibility,
    Validation,
    Governance,
    Licensing,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresArchiveCheck,
}

#[derive(Debug)]
struct RepositoryRecord {
    key: &'static str,
    layer: RepositoryLayer,
    artifact: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        RepositoryRecord {
            key: "readme",
            layer: RepositoryLayer::Documentation,
            artifact: "README.md",
            review_focus: "Usability and onboarding",
            status: ReviewStatus::RequiresReview,
        },
        RepositoryRecord {
            key: "data_provenance",
            layer: RepositoryLayer::DataLayer,
            artifact: "data provenance notes",
            review_focus: "Evidence traceability",
            status: ReviewStatus::RequiresReview,
        },
        RepositoryRecord {
            key: "run_manifest",
            layer: RepositoryLayer::Reproducibility,
            artifact: "reproducibility_manifest.json",
            review_focus: "Rerun capability",
            status: ReviewStatus::Active,
        },
        RepositoryRecord {
            key: "model_card",
            layer: RepositoryLayer::Governance,
            artifact: "model_repository_card.json",
            review_focus: "Decision-support governance",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
