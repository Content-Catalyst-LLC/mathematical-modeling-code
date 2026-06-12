# State-Space Representation Guide

State-space representation separates the state update equation from the observation equation.

## Canonical discrete-time form

x[t+1] = F(x[t], u[t], theta)

y[t] = G(x[t], theta) + error[t]

## Canonical linear form

x[t+1] = A x[t] + B u[t]

y[t] = C x[t] + D u[t]

## Review questions

- What is the state vector?
- What are inputs or actions?
- What outputs are observed?
- What state is hidden or latent?
- What parameters govern the transition?
- Does the state contain enough information to update the system?
