records = [
    ("mechanism_record", "stock_flow_accumulation", "stock changes through inflow and outflow", "synthetic teaching example", "review", "flows must represent real processes"),
    ("mechanism_record", "balancing_feedback", "state-dependent adjustment limits growth", "formal teaching example", "review", "feedback parameters require evidence"),
    ("formal_record", "differential_equation", "dx/dt=f(x,t,theta)", "describes state change over time", "review", "rate equation needs process interpretation"),
    ("claim_record", "mechanistic", "organized process produces behavior", "requires process evidence", "review", "scope depends on mechanism and assumptions"),
    ("claim_record", "exploratory", "investigates possible system behavior", "scenario assumptions", "active", "not a confirmed mechanism or forecast")
]

println("record_type,name,role_or_process,evidence_or_requirement,status,warning")
for row in records
    println(join(row, ","))
end
