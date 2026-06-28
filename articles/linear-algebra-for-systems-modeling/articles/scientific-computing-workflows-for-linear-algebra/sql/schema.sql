CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('scientific-computing-workflows-for-linear-algebra', 'Scientific Computing Workflows for Linear Algebra', 'planned', 'A practical article on numerical libraries, sparse methods, network computation, reproducible outputs, and systems-oriented implementation.');
