struct Artifact {
    name: &'static str,
    artifact_type: &'static str,
    path: &'static str,
    origin: &'static str,
    role: &'static str,
    warning: &'static str,
}

fn main() {
    let artifacts = [
        Artifact { name: "parameter_records", artifact_type: "csv", path: "data/parameter_records.csv", origin: "source", role: "documents parameter names values units sources and ranges", warning: "Parameter records do not prove empirical correctness." },
        Artifact { name: "model_outputs", artifact_type: "csv", path: "outputs/tables/model_outputs.csv", origin: "generated", role: "stores computed trajectory or summary outputs", warning: "Generated outputs require diagnostics and interpretation limits." },
        Artifact { name: "diagnostics", artifact_type: "json", path: "outputs/json/diagnostics.json", origin: "generated", role: "records validation convergence and warning status", warning: "Diagnostics should remain attached to interpretation." },
        Artifact { name: "governance_queue", artifact_type: "markdown", path: "outputs/reports/governance_queue.md", origin: "generated", role: "collects warnings requiring human review", warning: "Governance queues support judgment but do not replace it." },
    ];
    println!("artifact_name,artifact_type,path,source_or_generated,review_role,warning");
    for a in artifacts {
        println!("{},{},{},{},{},{}", a.name, a.artifact_type, a.path, a.origin, a.role, a.warning);
    }
}
