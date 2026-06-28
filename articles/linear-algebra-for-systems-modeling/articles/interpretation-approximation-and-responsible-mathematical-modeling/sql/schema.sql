CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('interpretation-approximation-and-responsible-mathematical-modeling', 'Interpretation, Approximation, and Responsible Mathematical Modeling', 'planned', 'A capstone article on responsible use of linear algebra in systems modeling.');
