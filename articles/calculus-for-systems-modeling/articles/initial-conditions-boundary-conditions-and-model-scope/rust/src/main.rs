struct Record {
    record_type: &'static str,
    name: &'static str,
    value_or_type: &'static str,
    interpretation: &'static str,
    warning: &'static str,
}

fn main() {
    let records = [
        Record { record_type: "initial_condition", name: "population_stock", value_or_type: "10 state units", interpretation: "synthetic teaching baseline", warning: "starting values need source and uncertainty notes" },
        Record { record_type: "boundary_condition", name: "left_edge", value_or_type: "no_flux", interpretation: "material does not leave through the left boundary", warning: "no-flux boundaries may overstate retention" },
        Record { record_type: "boundary_condition", name: "right_edge", value_or_type: "absorbing", interpretation: "material can leave the modeled domain", warning: "absorbing boundaries may understate feedback" },
        Record { record_type: "scope_record", name: "temporal_scope", value_or_type: "0 to 20 time units", interpretation: "short-horizon teaching simulation", warning: "do not interpret as long-term forecast" },
        Record { record_type: "scope_record", name: "parameter_scope", value_or_type: "growth_rate between 0.1 and 0.6", interpretation: "local sensitivity and teaching examples", warning: "do not use outside tested range without review" },
    ];
    println!("record_type,name,value_or_type,interpretation,warning");
    for r in records {
        println!("{},{},{},{},{}", r.record_type, r.name, r.value_or_type, r.interpretation, r.warning);
    }
}
