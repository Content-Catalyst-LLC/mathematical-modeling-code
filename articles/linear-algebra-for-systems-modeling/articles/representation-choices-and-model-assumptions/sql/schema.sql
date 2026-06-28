CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('representation-choices-and-model-assumptions', 'Representation Choices and Model Assumptions', 'planned', 'A critical article on how vector and matrix choices shape model meaning.');
