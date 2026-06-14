# Calculus for Systems Modeling

Companion repository folder for the **Calculus for Systems Modeling** article map and its nested article-level workflows.

This folder supports calculus-based systems modeling across continuous change, rates, accumulation, optimization, multivariable interaction, vector fields, differential equations, numerical approximation, simulation, sensitivity analysis, responsible interpretation, and reproducible scientific-computing workflows.

## Nested article folders

Article-specific code now lives under:

```text
articles/calculus-for-systems-modeling/articles/
```

The first nested article companion folder is:

```text
articles/calculus-for-systems-modeling/articles/what-is-calculus-for-systems-modeling/
```

## Standard article folder structure

Each nested article folder may include:

```text
python/
r/
julia/
sql/
haskell/
c/
cpp/
fortran/
rust/
go/
notebooks/
docs/
data/
outputs/
schemas/
canvas/
README.md
Makefile
article-metadata.yml
github-embed-wordpress.html
```

## General principles

- Keep models transparent.
- Make assumptions explicit.
- Separate synthetic teaching data from real-world datasets.
- Document parameters, uncertainty, and limitations.
- Use reproducible workflows.
- Treat computation as support for interpretation, not a substitute for judgment.
- Keep examples educational, auditable, and extensible.

## Default language standard

This folder uses Python, R, Julia, SQL, Haskell, C, C++, Fortran, Rust, Go, notebooks, documentation, schemas, generated outputs, and Canvas-ready workflow artifacts by default.

## Run the first nested article workflow

```bash
make smoke
```

or:

```bash
cd articles/what-is-calculus-for-systems-modeling
make smoke
```
