CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('pagerank-and-network-influence-models', 'PageRank and Network Influence Models', 'planned', 'A study of eigenvector-based influence, ranking, and network importance.');
