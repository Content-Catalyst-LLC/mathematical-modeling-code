# Advanced PageRank and Network Influence Review

- **node_definition** (required): Define ranked entities and graph boundary.
- **directed_edge_meaning** (required): Document whether links represent citation, endorsement, dependence, exposure, attention, or flow.
- **transition_normalization** (required): State row or column stochastic convention and normalization rule.
- **dangling_node_handling** (required): Define redistribution rule for nodes with no outgoing links.
- **damping_teleportation** (required): Document damping factor and teleportation or personalization vector.
- **convergence_diagnostics** (required): Report tolerance, iteration count, residuals, and convergence status.
- **sensitivity_testing** (recommended): Test edge perturbations, weight perturbations, damping changes, and graph-boundary alternatives.
- **ranking_governance** (required): Review manipulation incentives, feedback loops, provenance, and interpretive limits.
