"""
Probability for Systems Modeling:
Markov chain transition simulation.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def load_transition_matrix(path: str) -> tuple[list[str], np.ndarray]:
    """Load transition matrix from long-form CSV."""
    transitions = pd.read_csv(path)

    states = sorted(set(transitions["from_state"]).union(set(transitions["to_state"])))
    state_index = {state: i for i, state in enumerate(states)}

    matrix = np.zeros((len(states), len(states)))

    for _, row in transitions.iterrows():
        i = state_index[row["from_state"]]
        j = state_index[row["to_state"]]
        matrix[i, j] = row["probability"]

    return states, matrix


def simulate_markov_chain(states: list[str], transition_matrix: np.ndarray, initial_state: str, steps: int, seed: int = 42) -> pd.DataFrame:
    """Simulate a discrete-state Markov chain."""
    rng = np.random.default_rng(seed)
    state_index = {state: i for i, state in enumerate(states)}

    current = state_index[initial_state]
    sequence = [current]

    for _ in range(steps - 1):
        current = int(rng.choice(np.arange(len(states)), p=transition_matrix[current]))
        sequence.append(current)

    return pd.DataFrame({
        "time": np.arange(steps),
        "state_id": sequence,
        "state": [states[i] for i in sequence]
    })


def main() -> None:
    states, matrix = load_transition_matrix("../data/markov_transition_matrix.csv")

    simulation = simulate_markov_chain(
        states=states,
        transition_matrix=matrix,
        initial_state="stable",
        steps=500,
        seed=42
    )

    state_summary = simulation["state"].value_counts(normalize=True).reset_index()
    state_summary.columns = ["state", "proportion"]

    print(state_summary)

    simulation.to_csv("../outputs/python_markov_chain_simulation.csv", index=False)
    state_summary.to_csv("../outputs/python_markov_chain_state_summary.csv", index=False)


if __name__ == "__main__":
    main()
