CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('long-run-behavior-in-state-transition-systems', 'Long-Run Behavior in State Transition Systems', 'planned', 'A treatment of steady states, convergence, and persistent structure.');
