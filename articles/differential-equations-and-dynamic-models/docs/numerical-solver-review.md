# Numerical Solver Review

## Core checks

- What solver is used?
- What time step or tolerance is used?
- Is the model stiff?
- Do results change under smaller time steps?
- Are boundaries enforced during integration?
- Are units consistent between rates and time increments?

## Common risks

- using Euler integration with too large a step;
- hiding solver settings;
- confusing numerical artifacts with system behavior;
- failing to test trajectory sensitivity;
- ignoring boundary violations;
- reporting endpoints without path diagnostics.
