CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('what-is-linear-algebra-for-systems-modeling', 'What Is Linear Algebra for Systems Modeling?', 'planned', 'An opening article defining linear algebra as a formal language for structure, interdependence, transformation, and multivariable systems.');
