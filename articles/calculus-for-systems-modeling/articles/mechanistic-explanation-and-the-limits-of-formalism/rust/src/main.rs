struct Record {
    record_type: &'static str,
    name: &'static str,
    role_or_process: &'static str,
    evidence_or_requirement: &'static str,
    status: &'static str,
    warning: &'static str,
}

fn main() {
    let records = [
        Record { record_type: "mechanism_record", name: "stock_flow_accumulation", role_or_process: "stock changes through inflow and outflow", evidence_or_requirement: "synthetic teaching example", status: "review", warning: "flows must represent real processes" },
        Record { record_type: "mechanism_record", name: "balancing_feedback", role_or_process: "state-dependent adjustment limits growth", evidence_or_requirement: "formal teaching example", status: "review", warning: "feedback parameters require evidence" },
        Record { record_type: "formal_record", name: "differential_equation", role_or_process: "dxdt=f", evidence_or_requirement: "process interpretation required", status: "review", warning: "rate equation needs mechanism meaning" },
        Record { record_type: "claim_record", name: "mechanistic", role_or_process: "organized process produces behavior", evidence_or_requirement: "process evidence required", status: "review", warning: "scope depends on assumptions" },
        Record { record_type: "claim_record", name: "exploratory", role_or_process: "investigates possible behavior", evidence_or_requirement: "scenario assumptions required", status: "active", warning: "not a confirmed mechanism or forecast" },
    ];
    println!("record_type,name,role_or_process,evidence_or_requirement,status,warning");
    for r in records {
        println!("{},{},{},{},{},{}", r.record_type, r.name, r.role_or_process, r.evidence_or_requirement, r.status, r.warning);
    }
}
