CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('gaussian-elimination-and-row-reduction', 'Gaussian Elimination and Row Reduction', 'planned', 'A treatment of systematic solution methods and equivalent systems.');
