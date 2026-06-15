# Network Models and Graph Structures

Companion code and reproducible workflows for **“Network Models and Graph Structures”** in the **Mathematical Modeling** knowledge series.

This folder treats nodes, edges, weights, directions, adjacency structures, reachability, centrality, components, dependency pathways, graph diagnostics, and network-model governance as explicit mathematical modeling objects.

## Run everything available

```bash
make all
```

## Dependency-light smoke test

```bash
make smoke
```

## Selected targets

```bash
make python
make test
make r
make sql
make julia
make haskell
make rust
make go
make cpp
make fortran
make c
```

## Minimal Python run

```bash
python3 python/network_models_graph_structures/cli.py --output-dir outputs
```

## Folder structure

```text
articles/network-models-and-graph-structures/
├── python/
├── r/
├── julia/
├── sql/
├── haskell/
├── rust/
├── go/
├── cpp/
├── fortran/
├── c/
├── notebooks/
├── docs/
├── data/
├── outputs/
├── canvas/
└── schemas/
```

## Modeling themes

- graph structures as relational mathematical objects;
- nodes, edges, weights, directions, and boundaries;
- edge-list, adjacency-list, and matrix representation;
- reachability, degree, dependency, and centrality diagnostics;
- network validation under missing-edge and weight uncertainty;
- responsible interpretation of centrality, community, and cascading risk.

## Self-contained calculators

This article folder includes a reusable calculator layer in `calculators/` for quick command-line exploration of derivatives, definite integrals, finite differences, ODE solvers, logistic dynamics, and parameter sensitivity. The scripts are intentionally self-contained so they can be run without installing article-specific dependencies.

Example commands:

```bash
cd calculators
python3 python/model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
python3 python/model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 10 --method simpson
python3 python/model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --dt 0.1 --steps 50
bash run_calculator_smoke_tests.sh
```
