CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('diagonalization-and-repeated-transformation', 'Diagonalization and Repeated Transformation', 'planned', 'An article on simplifying repeated matrix action and dynamic behavior.');
