DROP TABLE IF EXISTS accumulation_assumption_registry;
DROP TABLE IF EXISTS flow_records;

CREATE TABLE accumulation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO accumulation_assumption_registry VALUES
('initial_stock','Initial stock','Defines the starting value before interval accumulation begins.','Keeps inherited burden separate from new accumulated change.','Omitting the initial stock can make ending-stock claims misleading.'),
('net_flow','Net flow','Defines the rate of stock change as inflow minus outflow.','Explains why the stock grows, declines, or stabilizes.','Sign conventions must be explicit.'),
('gross_flows','Gross flows','Records cumulative inflow and cumulative outflow separately.','Prevents large offsetting activity from being hidden by net change.','Net change alone can conceal high stress or turnover.'),
('exposure_window','Exposure window','Defines the interval over which exposure is accumulated.','Clarifies whether the result is event-based, annual, lifetime, or moving-window exposure.','Changing the window changes the cumulative claim.'),
('unit_consistency','Unit consistency','Checks that rate multiplied by time produces stock or exposure units.','Prevents flow, stock, concentration, and exposure from being confused.','Unit mismatch indicates an invalid cumulative interpretation.');

CREATE TABLE flow_records (
    step INTEGER PRIMARY KEY,
    duration REAL NOT NULL,
    inflow REAL NOT NULL,
    outflow REAL NOT NULL,
    exposure_intensity REAL NOT NULL,
    population_weight REAL NOT NULL
);

INSERT INTO flow_records VALUES
(1,1.0,12.0,6.0,20.0,1000.0),
(2,1.0,10.0,7.0,18.0,1100.0),
(3,1.0,9.0,8.0,15.0,1050.0),
(4,1.0,8.0,9.0,13.0,980.0),
(5,1.0,7.0,9.0,11.0,960.0);
