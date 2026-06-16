# Financial Dynamics and Continuous Compounding Audit

## Scenario Records
- **continuous_compounding_case** (future_value): final value=4481.6891, present value=1000.0000. continuous compounding accumulates value exponentially.
- **monthly_compounding_case** (discrete_compounding): final value=4467.7443, present value=1000.0000. discrete compounding depends on compounding frequency.
- **discounted_future_value** (present_value): final value=5000.0000, present value=1115.6508. discounting translates future value into present value.
- **cash_flow_npv** (net_present_value): final value=504.4933, present value=504.4933. cash-flow timing and discount rate determine net present value.
- **debt_dynamics_case** (debt_balance): final value=4030.4701, present value=0.0000. debt balance depends on interest, payments, and time.
- **real_return_case** (inflation_adjusted_growth): final value=2785.3965, present value=1000.0000. real growth adjusts nominal return for inflation.
- **geometric_return_case** (portfolio_compounding): final value=0.0307, present value=0.0000. geometric return reflects compounded path behavior.
- **leverage_case** (leverage_ratio): final value=5.0000, present value=0.0000. leverage magnifies sensitivity to asset value changes.
- **rate_sensitivity_case** (sensitivity): final value=134450.6721, present value=0.0000. value sensitivity to rate grows with time and accumulated value.

## Rate Records
- **nominal_to_real_rate_case**: real rate=0.034146; continuous equivalent=0.058269. Cash flows and rates should use consistent real or nominal units.
- **effective_to_continuous_case**: real rate=0.050000; continuous equivalent=0.048790. Continuous equivalent rate is a convention conversion, not a risk adjustment.

Financial model outputs depend on rate convention, time horizon, cash-flow timing, compounding rule, inflation basis, risk, liquidity, fees, taxes, uncertainty, and claim boundaries.
