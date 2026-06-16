records = [
    ("unit_record", "population_stock", "40", "state units", "stock", "synthetic value; do not treat as empirical measurement"),
    ("unit_record", "carrying_capacity", "100", "state units", "stock", "capacity scale controls normalized interpretation"),
    ("unit_record", "growth_rate", "0.35", "per time unit", "inverse time", "rate units must match the time variable"),
    ("scale_record", "stock_scale", "100", "state units", "carrying capacity used to normalize stock", "changing scale changes dimensionless stock"),
    ("nondimensional_record", "scaled_stock", "0.4", "dimensionless", "stock divided by carrying capacity", "dimensionless form depends on documented scale")
]

println("record_type,name,value,unit,interpretation,warning")
for row in records
    println(join(row, ","))
end
