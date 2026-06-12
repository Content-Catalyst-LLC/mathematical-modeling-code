#[derive(Debug)]
enum Dimension {
    Volume,
    Time,
    VolumePerTime,
    InverseTime,
    Dimensionless,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
}

#[derive(Debug)]
struct UnitRecord {
    key: &'static str,
    dimension: Dimension,
    unit_label: &'static str,
    review_question: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        UnitRecord {
            key: "storage",
            dimension: Dimension::Volume,
            unit_label: "m3",
            review_question: "Does storage remain within physical bounds?",
            status: ReviewStatus::Active,
        },
        UnitRecord {
            key: "inflow",
            dimension: Dimension::VolumePerTime,
            unit_label: "m3/day",
            review_question: "Is inflow multiplied by the model time step?",
            status: ReviewStatus::RequiresReview,
        },
        UnitRecord {
            key: "loss_rate",
            dimension: Dimension::InverseTime,
            unit_label: "1/day",
            review_question: "Does the rate unit match the time step?",
            status: ReviewStatus::RequiresValidation,
        },
        UnitRecord {
            key: "storage_fraction",
            dimension: Dimension::Dimensionless,
            unit_label: "1",
            review_question: "Is the denominator clearly documented?",
            status: ReviewStatus::Active,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
