# Abstraction Specification

## Article

**Abstraction and Representation in Mathematical Models**

## Central claim

A mathematical model is not a copy of the world. It is a selective representation that preserves structure relevant to a stated purpose while omitting, aggregating, idealizing, or parameterizing other features.

## Core abstraction questions

1. What is the target system?
2. What is the model’s intended use?
3. Which relationships must be preserved?
4. Which details can be omitted?
5. Which details are omitted only temporarily?
6. Which omissions could distort conclusions?
7. Which formal representation best preserves the relevant structure?
8. What evidence would show representational adequacy?

## Example formal representation

\[
S_{t+1}=\min(K,\max(0,S_t+I_t-D_t-L_t))
\]

This represents a resource system as a bounded stock-flow model.

## Useful when

- aggregate storage is the relevant state;
- inflows and outflows are the core structure;
- a first-pass scenario model is appropriate;
- the goal is explanation, audit, or teaching.

## Not sufficient when

- spatial distribution matters;
- legal or ecological allocation matters;
- stochastic hydrology matters;
- subgroup effects matter;
- water quality matters;
- operational decision-making requires validated empirical data.
