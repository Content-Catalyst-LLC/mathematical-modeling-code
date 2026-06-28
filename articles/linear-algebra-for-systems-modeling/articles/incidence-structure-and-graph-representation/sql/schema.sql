CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('incidence-structure-and-graph-representation', 'Incidence Structure and Graph Representation', 'planned', 'An article on node-edge relationships, direction, and connectivity.');
