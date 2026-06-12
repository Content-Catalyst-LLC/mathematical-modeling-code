-- Dimensional analysis, units, and scale governance schema.

DROP TABLE IF EXISTS conversion_audit;
DROP TABLE IF EXISTS scale_scenario;
DROP TABLE IF EXISTS unit_register;
DROP TABLE IF EXISTS quantity_type;

CREATE TABLE quantity_type (
    quantity_type TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    typical_failure TEXT NOT NULL
);

CREATE TABLE unit_register (
    unit_id INTEGER PRIMARY KEY,
    unit_key TEXT NOT NULL,
    quantity_type TEXT NOT NULL,
    unit TEXT NOT NULL,
    dimension TEXT NOT NULL,
    expected_range TEXT NOT NULL,
    review_question TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'review', 'revise', 'archive')),
    FOREIGN KEY (quantity_type) REFERENCES quantity_type(quantity_type)
);

CREATE TABLE scale_scenario (
    scenario TEXT PRIMARY KEY,
    initial_storage_m3 REAL NOT NULL CHECK (initial_storage_m3 >= 0),
    capacity_m3 REAL NOT NULL CHECK (capacity_m3 > 0),
    inflow_m3_per_day REAL NOT NULL CHECK (inflow_m3_per_day >= 0),
    demand_m3_per_day REAL NOT NULL CHECK (demand_m3_per_day >= 0),
    loss_rate_per_day REAL NOT NULL CHECK (loss_rate_per_day >= 0 AND loss_rate_per_day <= 1),
    delta_t_days REAL NOT NULL CHECK (delta_t_days > 0),
    periods INTEGER NOT NULL CHECK (periods > 0),
    description TEXT
);

CREATE TABLE conversion_audit (
    conversion TEXT PRIMARY KEY,
    source_unit TEXT NOT NULL,
    target_unit TEXT NOT NULL,
    factor REAL NOT NULL,
    review_question TEXT NOT NULL
);

INSERT INTO quantity_type VALUES
('stock','Stored quantity measured at a time.','Stocks are confused with flows.'),
('stock_bound','Capacity or bound for a stock.','Capacity is expressed in a different unit from stock.'),
('flow','Quantity per unit time.','Flow is added directly to stock without time-step conversion.'),
('rate','Inverse-time or proportional rate.','Rate unit does not match time step.'),
('time_step','Simulation interval or temporal resolution.','Time step is omitted from update equations.'),
('dimensionless_ratio','Quantity normalized by a characteristic scale.','Ratio is interpreted without stating denominator.');

INSERT INTO unit_register(unit_key, quantity_type, unit, dimension, expected_range, review_question, status) VALUES
('storage','stock','m3','volume','[0, capacity]','Does storage remain within physical bounds?','active'),
('capacity','stock_bound','m3','volume','positive','Is capacity in the same unit as storage?','active'),
('inflow','flow','m3/day','volume/time','nonnegative','Is inflow multiplied by the model time step?','review'),
('demand','flow','m3/day','volume/time','nonnegative','Is demand multiplied by the model time step?','review'),
('loss_rate','rate','1/day','time^-1','[0, 1] for daily fractional loss','Does the loss-rate unit match the time step?','review'),
('delta_t','time_step','day','time','positive','Is the time step used to convert rates and flows?','review'),
('storage_fraction','dimensionless_ratio','dimensionless','1','[0, 1]','Is dimensionless storage used for cross-scale comparison?','active');

INSERT INTO scale_scenario VALUES
('daily_baseline',80,100,8,6,0.015,1,60,'Daily baseline with consistent flow-to-stock conversion'),
('weekly_step',80,100,8,6,0.015,7,12,'Weekly time-step scenario'),
('high_demand',80,100,8,10,0.015,1,60,'Higher demand scenario'),
('tight_capacity',70,75,8,6,0.015,1,60,'Tight capacity scenario'),
('high_loss',80,100,8,6,0.05,1,60,'Higher daily loss-rate scenario');

INSERT INTO conversion_audit VALUES
('percent_to_proportion','percent','proportion',0.01,'Was percent converted before computation?'),
('days_to_years','day','year',0.0027397260273972603,'Does the rate need annualization?'),
('years_to_days','year','day',365,'Does the annual rate need daily conversion?'),
('kilometers_to_meters','km','m',1000,'Are spatial coefficients in consistent length units?'),
('hectares_to_square_kilometers','ha','km2',0.01,'Are area units consistent before density calculation?');
