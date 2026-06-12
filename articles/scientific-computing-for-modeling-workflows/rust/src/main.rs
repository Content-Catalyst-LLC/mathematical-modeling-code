#[derive(Debug)]
enum WorkflowStage {
    DataIntake,
    ParameterControl,
    ModelExecution,
    OutputGeneration,
    Reproducibility,
    Validation,
    Governance,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresReproducibilityCheck,
}

#[derive(Debug)]
struct WorkflowRecord {
    key: &'static str,
    stage: WorkflowStage,
    computational_object: &'static str,
    review_focus: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        WorkflowRecord {
            key: "input_schema",
            stage: WorkflowStage::DataIntake,
            computational_object: "resource_scenario_fields",
            review_focus: "Input validity",
            status: ReviewStatus::RequiresReview,
        },
        WorkflowRecord {
            key: "configuration",
            stage: WorkflowStage::ParameterControl,
            computational_object: "scenario configuration",
            review_focus: "Parameter traceability",
            status: ReviewStatus::Active,
        },
        WorkflowRecord {
            key: "simulation_engine",
            stage: WorkflowStage::ModelExecution,
            computational_object: "resource update loop",
            review_focus: "Code-model alignment",
            status: ReviewStatus::RequiresValidation,
        },
        WorkflowRecord {
            key: "run_manifest",
            stage: WorkflowStage::Reproducibility,
            computational_object: "manifest json",
            review_focus: "Rerun capability",
            status: ReviewStatus::RequiresReproducibilityCheck,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
