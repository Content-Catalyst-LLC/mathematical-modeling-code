CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('matrices-and-the-organization-of-multivariable-systems', 'Matrices and the Organization of Multivariable Systems', 'planned', 'A core article on matrices as representations of relationships, constraints, and interactions.');
