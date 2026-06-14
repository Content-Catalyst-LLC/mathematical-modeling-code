#[derive(Debug)]
enum EngineeringDomain {
    StructuralEngineering,
    MechanicalEngineering,
    ElectricalEngineering,
    ChemicalEngineering,
    SystemsEngineering,
    ReliabilityEngineering,
}

#[derive(Debug)]
enum EngineeringModelRole {
    InitialDesign,
    PerformanceAnalysis,
    SafetyReview,
    Optimization,
    Validation,
    LifecycleMonitoring,
}

#[derive(Debug)]
enum EngineeringModelFamily {
    AlgebraicDesignModel,
    DifferentialEquationModel,
    FiniteElementModel,
    ControlModel,
    ReliabilityModel,
    SimulationModel,
}

#[derive(Debug)]
enum ReviewStatus {
    Active,
    RequiresReview,
    RequiresValidation,
    RequiresSafetyReview,
}

#[derive(Debug)]
struct EngineeringModelRecord {
    key: &'static str,
    domain: EngineeringDomain,
    role: EngineeringModelRole,
    family: EngineeringModelFamily,
    design_question: &'static str,
    status: ReviewStatus,
}

fn main() {
    let records = vec![
        EngineeringModelRecord {
            key: "sizing_model",
            domain: EngineeringDomain::StructuralEngineering,
            role: EngineeringModelRole::InitialDesign,
            family: EngineeringModelFamily::AlgebraicDesignModel,
            design_question: "What beam dimensions are feasible under baseline load?",
            status: ReviewStatus::Active,
        },
        EngineeringModelRecord {
            key: "safety_model",
            domain: EngineeringDomain::StructuralEngineering,
            role: EngineeringModelRole::SafetyReview,
            family: EngineeringModelFamily::AlgebraicDesignModel,
            design_question: "Does the design maintain positive stress margin?",
            status: ReviewStatus::RequiresSafetyReview,
        },
        EngineeringModelRecord {
            key: "validation_model",
            domain: EngineeringDomain::ReliabilityEngineering,
            role: EngineeringModelRole::Validation,
            family: EngineeringModelFamily::ReliabilityModel,
            design_question: "What test evidence is needed before use?",
            status: ReviewStatus::RequiresValidation,
        },
    ];

    for record in records {
        println!("{:?}", record);
    }
}
