CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('case-study-dimensionality-reduction-in-high-dimensional-data', 'Case Study: Dimensionality Reduction in High-Dimensional Data', 'planned', 'A worked example using decomposition to reveal structure.');
