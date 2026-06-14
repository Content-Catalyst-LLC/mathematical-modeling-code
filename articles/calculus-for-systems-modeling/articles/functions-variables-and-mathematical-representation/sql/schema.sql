DROP TABLE IF EXISTS model_parameter;
DROP TABLE IF EXISTS functional_model_registry;

CREATE TABLE functional_model_registry (
    model_key TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    functional_form TEXT NOT NULL,
    primary_variable TEXT NOT NULL,
    output_variable TEXT NOT NULL,
    interpretation TEXT NOT NULL
);

CREATE TABLE model_parameter (
    model_key TEXT NOT NULL,
    parameter_name TEXT NOT NULL,
    parameter_value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    PRIMARY KEY (model_key, parameter_name),
    FOREIGN KEY (model_key) REFERENCES functional_model_registry(model_key)
);

INSERT INTO functional_model_registry VALUES
('linear_growth','Linear Growth','y = a + bx','x','y','Constant marginal change'),
('exponential_growth','Exponential Growth','y = a exp(bx)','x','y','Compounding change'),
('logistic_growth','Logistic Growth','y = K / (1 + exp(-r(x-c)))','x','y','Bounded growth toward capacity'),
('threshold_response','Threshold Response','piecewise threshold','x','y','Regime-dependent response');

INSERT INTO model_parameter VALUES
('linear_growth','a',10.0,'output units','baseline level'),
('linear_growth','b',2.0,'output units per input unit','constant marginal change'),
('exponential_growth','a',10.0,'output units','initial scale'),
('exponential_growth','b',0.18,'per input unit','compounding rate'),
('logistic_growth','K',100.0,'output units','upper capacity'),
('logistic_growth','r',0.75,'per input unit','response rate'),
('logistic_growth','c',5.0,'input units','midpoint'),
('threshold_response','threshold',5.0,'input units','regime breakpoint'),
('threshold_response','low',20.0,'output units','lower response value'),
('threshold_response','high',80.0,'output units','higher response value');
