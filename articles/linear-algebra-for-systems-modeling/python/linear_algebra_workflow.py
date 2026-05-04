"""
Linear Algebra for Systems Modeling:
State transitions, eigenanalysis, networks, and SVD.

Educational example only.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def load_transition_matrix(path: str) -> tuple[list[str], np.ndarray]:
    """Load a transition matrix from long-form CSV."""
    rows = pd.read_csv(path)
    states = sorted(set(rows["from_state"]).union(set(rows["to_state"])))
    index = {state: i for i, state in enumerate(states)}
    matrix = np.zeros((len(states), len(states)))

    for _, row in rows.iterrows():
        matrix[index[row["to_state"]], index[row["from_state"]]] = row["value"]

    return states, matrix


def simulate_state_transition(matrix: np.ndarray, initial_state: np.ndarray, steps: int) -> pd.DataFrame:
    """Simulate repeated matrix transformation of a state vector."""
    state = initial_state.copy()
    rows = []

    for t in range(steps):
        record = {"time": t}
        for i, value in enumerate(state):
            record[f"state_{i}"] = value
        rows.append(record)
        state = matrix @ state

    return pd.DataFrame(rows)


def adjacency_from_edges(path: str) -> tuple[list[str], np.ndarray]:
    """Create weighted adjacency matrix from edge list."""
    edges = pd.read_csv(path)
    nodes = sorted(set(edges["source"]).union(set(edges["target"])))
    index = {node: i for i, node in enumerate(nodes)}
    adjacency = np.zeros((len(nodes), len(nodes)))

    for _, row in edges.iterrows():
        adjacency[index[row["source"]], index[row["target"]]] = row["weight"]

    return nodes, adjacency


def main() -> None:
    states, transition_matrix = load_transition_matrix("../data/state_transition_matrix.csv")

    initial_state = np.array([0.10, 0.70, 0.20])

    transition_results = simulate_state_transition(
        matrix=transition_matrix,
        initial_state=initial_state,
        steps=25
    )

    eigenvalues, eigenvectors = np.linalg.eig(transition_matrix)

    eigen_summary = pd.DataFrame({
        "eigenvalue_real": eigenvalues.real,
        "eigenvalue_imag": eigenvalues.imag
    })

    nodes, adjacency = adjacency_from_edges("../data/network_edges.csv")

    network_summary = pd.DataFrame({
        "node": nodes,
        "out_strength": adjacency.sum(axis=1),
        "in_strength": adjacency.sum(axis=0)
    })

    observations = pd.read_csv("../data/systems_observations.csv")
    features = observations.drop(columns=["observation_id"]).to_numpy(dtype=float)

    standardized = (features - features.mean(axis=0)) / features.std(axis=0, ddof=1)

    U, singular_values, Vt = np.linalg.svd(standardized, full_matrices=False)

    svd_summary = pd.DataFrame({
        "component": np.arange(1, len(singular_values) + 1),
        "singular_value": singular_values,
        "variance_share": singular_values**2 / np.sum(singular_values**2)
    })

    print(transition_results.head())
    print(eigen_summary)
    print(network_summary)
    print(svd_summary)

    transition_results.to_csv("../outputs/python_state_transition_results.csv", index=False)
    eigen_summary.to_csv("../outputs/python_eigen_summary.csv", index=False)
    network_summary.to_csv("../outputs/python_network_summary.csv", index=False)
    svd_summary.to_csv("../outputs/python_svd_summary.csv", index=False)


if __name__ == "__main__":
    main()
