# State Transition and Markov Dynamics Audit

- Workflow: state_transition_markov_audit
- Scenario: synthetic_infrastructure_condition_transition_model
- State count: 4
- Time steps: 5
- Stochastic check passed: True
- Initial primary state: normal
- Highest-probability state after horizon: normal
- Highest probability after horizon: 0.42833125
- Stationary highest-probability state: normal
- Stationary highest probability: 0.406021897809
- Baseline disrupted probability after horizon: 0.1756128125
- Stress disrupted probability after horizon: 0.41016825

The Markov assumption treats the current state as sufficient for predicting the next state. If cumulative stress, repeated disruption, policy intervention, repair history, or hidden subgroups matter, the model should be expanded or treated as exploratory.

State transition results depend on state definitions, transition estimation, time-step choice, matrix orientation, sparse data, uncertainty, validation evidence, and scenario assumptions. Stationary distributions and multi-step probabilities describe the model, not guaranteed system destiny.
