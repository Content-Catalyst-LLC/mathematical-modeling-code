CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('rank-nullity-and-structural-dependence', 'Rank, Nullity, and Structural Dependence', 'planned', 'A study of dependency, redundancy, and degrees of freedom.');
