CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('simulation-of-high-dimensional-systems', 'Simulation of High-Dimensional Systems', 'planned', 'An article on evolving many-variable systems computationally.');
