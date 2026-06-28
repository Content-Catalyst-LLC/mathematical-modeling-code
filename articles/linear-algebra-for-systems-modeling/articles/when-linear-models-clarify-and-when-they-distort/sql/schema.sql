CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('when-linear-models-clarify-and-when-they-distort', 'When Linear Models Clarify and When They Distort', 'planned', 'A cautionary article on linear simplification, missed nonlinearities, and hidden assumptions.');
