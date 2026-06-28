CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('inverse-matrices-and-structural-recovery', 'Inverse Matrices and Structural Recovery', 'planned', 'A treatment of recovering inputs from outputs when structure permits.');
