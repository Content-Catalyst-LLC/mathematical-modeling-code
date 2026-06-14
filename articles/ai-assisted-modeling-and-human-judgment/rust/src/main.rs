#[derive(Debug)]
enum ModelingStage {
    ProblemFraming,
    ScenarioDesign,
    Computation,
    Validation,
    Communication,
    Governance,
}

#[derive(Debug)]
enum AIRole {
    IdeaGenerator,
    CodeAssistant,
    DiagnosticAide,
    DocumentationAssistant,
    ReviewCompanion,
}

#[derive(Debug)]
enum ArtifactType {
    ScenarioList,
    ModelScript,
    DiagnosticReport,
    PublicSummary,
    UseLimitStatement,
}

#[derive(Debug)]
enum ReviewStatus {
    Exploratory,
    Draft,
    RequiresReview,
    Approved,
    Retired,
}

#[derive(Debug)]
struct AIAssistanceRecord {
    key: &'static str,
    stage: ModelingStage,
    ai_role: AIRole,
    artifact_type: ArtifactType,
    provenance_required: bool,
    human_review_required: bool,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        AIAssistanceRecord {
            key: "scenario_drafting",
            stage: ModelingStage::ScenarioDesign,
            ai_role: AIRole::IdeaGenerator,
            artifact_type: ArtifactType::ScenarioList,
            provenance_required: true,
            human_review_required: true,
            status: ReviewStatus::RequiresReview,
        },
        AIAssistanceRecord {
            key: "code_generation",
            stage: ModelingStage::Computation,
            ai_role: AIRole::CodeAssistant,
            artifact_type: ArtifactType::ModelScript,
            provenance_required: true,
            human_review_required: true,
            status: ReviewStatus::RequiresReview,
        },
        AIAssistanceRecord {
            key: "governance_template",
            stage: ModelingStage::Governance,
            ai_role: AIRole::ReviewCompanion,
            artifact_type: ArtifactType::UseLimitStatement,
            provenance_required: true,
            human_review_required: true,
            status: ReviewStatus::Draft,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
