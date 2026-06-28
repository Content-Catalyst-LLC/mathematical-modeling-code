CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('vector-spaces-and-system-representation', 'Vector Spaces and System Representation', 'planned', 'An article on spaces of possible states and the structure of multivariable systems.');
