CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('control-systems-modeling', 'Control Systems Modeling', 'planned', 'A treatment of states, inputs, outputs, controllability, observability, and system response.');
