#[derive(Debug)]
enum RepresentationStatus {
    Active,
    RequiresReview,
    PotentialDistortion,
}

#[derive(Debug)]
struct RepresentationRecord {
    target_feature: &'static str,
    formal_representation: &'static str,
    omitted_detail: &'static str,
    status: RepresentationStatus,
}

fn main() {
    let records = vec![
        RepresentationRecord {
            target_feature: "Stored resource",
            formal_representation: "S_t",
            omitted_detail: "Spatial distribution, quality, ownership, and access",
            status: RepresentationStatus::Active,
        },
        RepresentationRecord {
            target_feature: "Resource additions",
            formal_representation: "I_t",
            omitted_detail: "Seasonality, stochastic hydrology, and upstream governance",
            status: RepresentationStatus::RequiresReview,
        },
        RepresentationRecord {
            target_feature: "Shortage risk",
            formal_representation: "shortage periods",
            omitted_detail: "Severity distribution and affected users",
            status: RepresentationStatus::PotentialDistortion,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
