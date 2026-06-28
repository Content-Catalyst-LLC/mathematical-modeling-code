# Validation Workflow

Use this workflow before trusting structural recovery from an inverse matrix.

## Step 1: Define the transformation

Identify what `A` represents.

- measurement system
- coordinate transformation
- signal mixing process
- state transition
- control allocation
- input-output structure

## Step 2: Check structural recoverability

For square systems:

- compute rank
- compute determinant
- check pivots or singular values
- test whether the null space is trivial

For rectangular systems:

- compute rank
- compare rank to number of unknowns
- decide whether the system is overdetermined or underdetermined

## Step 3: Check numerical recoverability

- compute condition number
- perturb `b`
- compare recovered state changes
- evaluate residual and relative residual

## Step 4: Choose the method

- full-rank square system: solve directly
- overdetermined system: least squares
- underdetermined system: pseudoinverse or constrained recovery
- ill-conditioned system: regularization, rescaling, or measurement redesign

## Step 5: Interpret the result

A small residual does not always mean a trustworthy model. A recovered state should be checked against physical meaning, units, uncertainty, and model assumptions.
