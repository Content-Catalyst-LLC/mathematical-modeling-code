DROP TABLE IF EXISTS system_scenario;
DROP TABLE IF EXISTS modeling_use;

CREATE TABLE system_scenario (
    scenario TEXT PRIMARY KEY,
    initial_state REAL NOT NULL CHECK (initial_state >= 0),
    rate REAL NOT NULL CHECK (rate >= 0),
    capacity REAL NOT NULL CHECK (capacity > 0),
    dt REAL NOT NULL CHECK (dt > 0),
    steps INTEGER NOT NULL CHECK (steps > 0),
    interpretation TEXT NOT NULL
);

CREATE TABLE modeling_use (
    use_case TEXT PRIMARY KEY,
    calculus_concept TEXT NOT NULL,
    systems_interpretation TEXT NOT NULL
);

INSERT INTO system_scenario VALUES
('baseline',10.0,0.20,100.0,0.1,300,'Basic bounded continuous-change trajectory'),
('slow_adjustment',10.0,0.10,100.0,0.1,300,'Lower rate of system change'),
('high_capacity',10.0,0.20,140.0,0.1,300,'Higher upper constraint or carrying capacity'),
('stress_capacity',10.0,0.20,70.0,0.1,300,'Lower upper constraint or capacity limit');

INSERT INTO modeling_use VALUES
('Rate modeling','Derivative','How quickly a system changes near a state'),
('Accumulation modeling','Integral','How local flows become cumulative totals'),
('Dynamic simulation','Differential equation','How rates determine trajectories over time'),
('Sensitivity analysis','Derivative or perturbation','How outputs respond to changes in assumptions'),
('Optimization','Gradient or critical point','How systems behave under objectives and constraints'),
('Spatial flow','Vector calculus','How fields flows and boundaries structure movement');
