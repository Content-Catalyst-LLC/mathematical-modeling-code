records = [
    ("parameter_record", "growth_rate", "0.35", "0.20 to 0.50", "per time unit", "synthetic teaching range"),
    ("parameter_record", "carrying_capacity", "100", "75 to 125", "state units", "synthetic teaching range"),
    ("sensitivity_record", "growth_rate", "sensitive", "local sensitivity may miss thresholds", "review", "conclusion may depend on growth-rate assumptions"),
    ("sensitivity_record", "carrying_capacity", "sensitive", "capacity controls final stock scale", "review", "capacity scale affects interpretation"),
    ("sensitivity_record", "initial_stock", "stable", "limited variation across tested range", "active", "output variation is limited in this example")
]

println("record_type,name,value_or_status,range_or_interpretation,unit_or_status,warning")
for row in records
    println(join(row, ","))
end
