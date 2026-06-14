# Advanced Mathematical Article Standard

This is the default standard for future **Calculus for Systems Modeling** articles.

The articles should remain readable for interdisciplinary systems modelers, but they should also be credible to mathematicians, applied mathematicians, numerical analysts, and mathematically mature scientific-computing readers.

## Required article additions

Every future article should include a section:

```html
<h2 id="mathematical-deepening">Mathematical Deepening</h2>
```

This section should include some or all of the following, depending on the article:

- formal definitions;
- propositions or lemmas when a precise statement clarifies the model;
- examples and counterexamples;
- codomain, image/range, feasible-set, and state-space distinctions where relevant;
- assumptions about continuity, differentiability, compactness, smoothness, boundedness, or measurability;
- boundary behavior and pathological cases;
- convergence, stability, conditioning, and approximation error when computation is involved;
- rigorous historical distinctions when the article is historical.

## Required code additions

Every companion folder should include an `advanced/` layer with:

```text
advanced/
├── Makefile
├── README.md
├── python/
│   ├── advanced_calculus_checks.py
│   ├── generate_advanced_report.py
│   └── test_advanced_calculus_checks.py
├── outputs/
│   ├── reports/
│   ├── tables/
│   └── json/
└── docs/
    └── mathematical_deepening.html
```

## Required numerical-analysis capabilities

Where applicable, include:

- forward difference;
- central difference;
- Richardson extrapolation;
- convergence-order estimates;
- truncation/roundoff discussion;
- stability review;
- conditioning review;
- invariant/domain preservation tests;
- boundary-value or edge-case checks;
- generated Markdown and JSON audit reports.

## Required formal-modeling capabilities

Where applicable, include:

- domain and codomain as explicit objects;
- image/range computed or approximated separately from codomain;
- feasible set and constraint checks;
- invariant set checks;
- typed validated records;
- separation of raw input from validated model objects;
- parameter-space and scenario-space registries.

## Article style

Use Harvard-style Further Reading and References entries followed by authoritative links whenever possible.

Do not include E-E-A-T/source-authority notes in the article body.

Do not use `:::writing` blocks in generated responses. Use normal HTML code blocks or plain text.
