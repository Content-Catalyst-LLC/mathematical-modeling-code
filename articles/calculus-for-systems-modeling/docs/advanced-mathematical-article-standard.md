# Advanced Mathematical Article Standard

This is the default standard for future **Calculus for Systems Modeling** articles.

Each article should remain readable for interdisciplinary systems modelers while also being credible to mathematicians, applied mathematicians, numerical analysts, and mathematically mature scientific-computing readers.

## Required article additions

Every future article should include:

```html
<h2 id="mathematical-deepening">Mathematical Deepening</h2>
```

Depending on the topic, include:

- formal definitions;
- propositions, lemmas, or preservation results;
- examples and counterexamples;
- codomain, image/range, feasible-set, and state-space distinctions;
- assumptions about continuity, differentiability, compactness, smoothness, boundedness, measurability, or topology;
- boundary behavior and pathological cases;
- convergence, stability, conditioning, and approximation error when computation is involved;
- rigorous historical distinctions when the article is historical.

## Required code additions

Each companion folder should include an `advanced/` layer with:

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

## Style rules

Use Harvard-style Further Reading and References entries followed by authoritative links whenever possible.

Do not include E-E-A-T/source-authority notes in the article body.

Do not use `:::writing` blocks.
