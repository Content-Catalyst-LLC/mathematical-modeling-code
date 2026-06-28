CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('matrix-multiplication-and-interaction-effects', 'Matrix Multiplication and Interaction Effects', 'planned', 'A treatment of composed relationships, chained transformations, and interaction structure.');
