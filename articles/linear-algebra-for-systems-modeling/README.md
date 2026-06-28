# Linear Algebra for Systems Modeling

Companion repository folder for the **Linear Algebra for Systems Modeling** article map and nested article-level workflows.

Article-specific code lives under:

```text
articles/linear-algebra-for-systems-modeling/articles/
```

All nested article folders are currently marked **planned**. The folder structure matches the calculus article-map format: a root article-map folder with an `article-registry.csv`, nested article folders, article metadata, WordPress GitHub embeds, notebook-ready documentation, Canvas-ready metadata, and reproducible modeling scaffolds.

Full article folders preserve Python, R, Julia, SQL, Haskell, C, C++, Fortran, Rust, Go, notebooks, docs, data, outputs, schemas, Canvas, advanced audit logic, and calculators.

## Code stack

- Python for numerical linear algebra, sparse computation, network analysis, simulation, and scientific-computing workflows.
- R for statistical structure, visualization, exploratory decomposition, PCA/SVD review, and reproducible reporting.
- Julia for high-performance numerical matrix workflows.
- SQL for state vectors, coefficient tables, adjacency matrices, scenario registries, provenance records, and output governance.
- Haskell for typed representations of system states, matrix transformations, assumptions, and validation logic.
- C, C++, and Fortran for performance-oriented matrix operations and legacy scientific computing.
- Rust and Go for reliable command-line tools, typed pipelines, and scalable workflow infrastructure.

## Run smoke checks

```bash
make smoke
```

## Run calculator checks where available

```bash
make calculators
```

## Principle

Linear algebra supports systems interpretation. It does not replace model assumptions, measurement judgment, uncertainty analysis, validation, or responsible systems thinking.
