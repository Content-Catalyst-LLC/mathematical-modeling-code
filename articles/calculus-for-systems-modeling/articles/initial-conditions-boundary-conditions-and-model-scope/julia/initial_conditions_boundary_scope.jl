records = [
    ("initial_condition", "population_stock", "10 state units", "synthetic teaching baseline", "starting values need source and uncertainty notes"),
    ("boundary_condition", "left_edge", "no_flux", "material does not leave through the left boundary", "no-flux boundaries may overstate retention"),
    ("boundary_condition", "right_edge", "absorbing", "material can leave the modeled domain", "absorbing boundaries may understate feedback"),
    ("scope_record", "temporal_scope", "0 to 20 time units", "short-horizon teaching simulation", "do not interpret as long-term forecast"),
    ("scope_record", "parameter_scope", "growth_rate between 0.1 and 0.6", "local sensitivity and teaching examples", "do not use outside tested range without review")
]

println("record_type,name,value_or_type,interpretation,warning")
for row in records
    println(join(row, ","))
end
