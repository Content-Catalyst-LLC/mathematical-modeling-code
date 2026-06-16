# Stiffness Diagnostic Audit

| Step size | Method | Amplification factor | Status | Absolute error |
|---:|---|---:|---|---:|
| 0.1 | explicit_euler | 4.000000 | unstable_for_test_problem | 1.048576000000e+06 |
| 0.1 | implicit_euler | 0.166667 | stable_for_test_problem | 1.653817168792e-08 |
| 0.05 | explicit_euler | 1.500000 | unstable_for_test_problem | 3.325256730080e+03 |
| 0.05 | implicit_euler | 0.285714 | stable_for_test_problem | 1.314132369763e-11 |
| 0.025 | explicit_euler | 0.250000 | stable_for_test_problem | 1.920478041838e-22 |
| 0.025 | implicit_euler | 0.444444 | stable_for_test_problem | 8.178982242780e-15 |
| 0.01 | explicit_euler | 0.500000 | stable_for_test_problem | 1.928749840075e-22 |
| 0.01 | implicit_euler | 0.666667 | stable_for_test_problem | 2.459461551595e-18 |

Stiffness diagnostics support numerical review, not empirical validation.
