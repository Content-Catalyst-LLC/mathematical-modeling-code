CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('graph-theory-foundations-for-systems-modeling', 'Graph Theory Foundations for Systems Modeling', 'planned', 'A bridge between graph concepts and linear algebraic representation.');
