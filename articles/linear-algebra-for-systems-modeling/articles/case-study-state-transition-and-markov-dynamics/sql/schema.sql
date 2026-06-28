CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('case-study-state-transition-and-markov-dynamics', 'Case Study: State Transition and Markov Dynamics', 'planned', 'A worked example connecting linear algebra, probability, and dynamic systems.');
