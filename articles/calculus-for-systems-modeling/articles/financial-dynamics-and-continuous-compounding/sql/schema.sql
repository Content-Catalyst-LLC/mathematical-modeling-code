DROP TABLE IF EXISTS financial_governance_registry;
DROP TABLE IF EXISTS financial_parameter_records;
DROP TABLE IF EXISTS financial_scenario_records;
DROP TABLE IF EXISTS financial_rate_records;

CREATE TABLE financial_governance_registry (
    registry_key TEXT PRIMARY KEY,
    registry_name TEXT NOT NULL,
    analytical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO financial_governance_registry VALUES
('rate_record','Rate record','Defines whether a rate is nominal, real, effective, annualized, continuous, fixed, variable, expected, contractual, or scenario-based.','Prevents rate-convention confusion.','Rate convention must be documented before comparing financial outcomes.'),
('cash_flow_record','Cash-flow record','Documents payment amount, sign, timing, uncertainty, frequency, inflation basis, and discount convention.','Connects valuation to time-stamped flows.','Cash-flow timing can dominate financial conclusions.'),
('compounding_record','Compounding record','Documents simple, discrete, periodic, effective, or continuous compounding assumptions.','Connects rate convention to accumulation path.','Compounding convention should match contract terms or model purpose.'),
('discount_record','Discount record','Documents discount rate, purpose, risk basis, inflation basis, and sensitivity.','Connects future value to present value.','Discount-rate choices can dominate long-horizon conclusions.'),
('debt_record','Debt record','Documents principal, interest, payments, fees, maturity, amortization, refinancing, and default risk.','Connects debt stock to repayment and interest flows.','Debt may grow if payment does not exceed interest accumulation.'),
('risk_record','Risk record','Documents volatility, drawdown, leverage, liquidity, correlation, default, and stress assumptions.','Connects expected value to uncertain paths.','Expected return does not guarantee realized compounded outcome.'),
('claim_boundary','Claim boundary','Defines whether the model supports teaching, comparison, contract analysis, valuation, planning, risk assessment, or decision support.','Prevents overclaiming and scope drift.','Financial conclusions should not exceed rate conventions, cash-flow evidence, risk assumptions, uncertainty, and tested scope.');

CREATE TABLE financial_parameter_records (
    parameter_name TEXT PRIMARY KEY,
    value REAL NOT NULL,
    unit TEXT NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO financial_parameter_records VALUES
('V0',1000.0,'currency units','initial value or principal','Initial value must match the modeled account, asset, or debt balance.');
INSERT INTO financial_parameter_records VALUES
('r',0.05,'per year','interest, return, or discount rate','Rate convention must be documented as nominal, real, effective, or continuous.');
INSERT INTO financial_parameter_records VALUES
('t',30.0,'years','time horizon','Long horizons amplify small rate differences.');
INSERT INTO financial_parameter_records VALUES
('n',12.0,'compounding periods per year','discrete compounding frequency','Compounding convention should match the contract or model purpose.');
INSERT INTO financial_parameter_records VALUES
('pi',0.025,'per year','inflation rate','Cash flows and rates should use consistent real or nominal units.');
INSERT INTO financial_parameter_records VALUES
('sigma',0.18,'annualized volatility','volatility estimate','Expected return does not guarantee realized compounded outcome.');
INSERT INTO financial_parameter_records VALUES
('payment',80.0,'currency units per year','debt repayment flow','Debt may grow if payment does not exceed interest accumulation.');

CREATE TABLE financial_scenario_records (
    scenario_name TEXT PRIMARY KEY,
    model_type TEXT NOT NULL,
    final_value REAL NOT NULL,
    present_value REAL NOT NULL,
    interpretation TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO financial_scenario_records VALUES
('continuous_compounding_case','future_value',4481.689070,1000.0,'continuous compounding accumulates value exponentially','Long horizons amplify small rate differences.');
INSERT INTO financial_scenario_records VALUES
('monthly_compounding_case','discrete_compounding',4467.744314,1000.0,'discrete compounding depends on compounding frequency','Compounding convention should match the contract or model purpose.');
INSERT INTO financial_scenario_records VALUES
('discounted_future_value','present_value',5000.0,1115.650801,'discounting translates future value into present value','Discount-rate choices can dominate long-horizon conclusions.');
INSERT INTO financial_scenario_records VALUES
('cash_flow_npv','net_present_value',691.0,691.0,'cash-flow timing and discount rate determine net present value','Cash-flow timing can dominate financial conclusions.');
INSERT INTO financial_scenario_records VALUES
('debt_dynamics_case','debt_balance',1800.0,0.0,'debt balance depends on interest, payments, and time','Debt may grow if payment does not exceed interest accumulation.');
INSERT INTO financial_scenario_records VALUES
('real_return_case','inflation_adjusted_growth',2765.0,1000.0,'real growth adjusts nominal return for inflation','Cash flows and rates should use consistent real or nominal units.');
INSERT INTO financial_scenario_records VALUES
('geometric_return_case','portfolio_compounding',0.030,0.0,'geometric return reflects compounded path behavior','Expected return does not guarantee realized compounded outcome.');

CREATE TABLE financial_rate_records (
    record_name TEXT PRIMARY KEY,
    nominal_rate REAL NOT NULL,
    inflation_rate REAL NOT NULL,
    real_rate REAL NOT NULL,
    continuous_equivalent REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO financial_rate_records VALUES
('nominal_to_real_rate_case',0.06,0.025,0.034146,0.058269,'Cash flows and rates should use consistent real or nominal units.');
INSERT INTO financial_rate_records VALUES
('effective_to_continuous_case',0.05,0.0,0.05,0.048790,'Continuous equivalent rate is a convention conversion, not a risk adjustment.');
