CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('projections-reflections-and-geometric-interpretation', 'Projections, Reflections, and Geometric Interpretation', 'planned', 'A geometric article on how transformations reshape state spaces.');
