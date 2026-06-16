struct Record {
    record_type: &'static str,
    name: &'static str,
    value: &'static str,
    unit: &'static str,
    interpretation: &'static str,
    warning: &'static str,
}

fn main() {
    let records = [
        Record { record_type: "unit_record", name: "population_stock", value: "40", unit: "state units", interpretation: "synthetic teaching value", warning: "synthetic value do not treat as empirical measurement" },
        Record { record_type: "unit_record", name: "carrying_capacity", value: "100", unit: "state units", interpretation: "synthetic teaching capacity", warning: "capacity scale controls normalized interpretation" },
        Record { record_type: "unit_record", name: "growth_rate", value: "0.35", unit: "per time unit", interpretation: "synthetic teaching rate", warning: "rate units must match the time variable" },
        Record { record_type: "scale_record", name: "stock_scale", value: "100", unit: "state units", interpretation: "carrying capacity used to normalize population stock", warning: "changing the scale changes dimensionless stock" },
        Record { record_type: "nondimensional_record", name: "scaled_stock", value: "0.4", unit: "dimensionless", interpretation: "population stock as fraction of carrying capacity", warning: "dimensionless form depends on documented scale" },
    ];
    println!("record_type,name,value,unit,interpretation,warning");
    for r in records {
        println!("{},{},{},{},{},{}", r.record_type, r.name, r.value, r.unit, r.interpretation, r.warning);
    }
}
