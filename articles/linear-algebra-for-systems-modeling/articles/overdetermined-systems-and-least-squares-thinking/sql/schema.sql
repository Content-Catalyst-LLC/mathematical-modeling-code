CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('overdetermined-systems-and-least-squares-thinking', 'Overdetermined Systems and Least Squares Thinking', 'planned', 'A bridge to regression, calibration, approximation, and empirical modeling.');
