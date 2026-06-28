CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('matrix-arithmetic-and-the-logic-of-combination', 'Matrix Arithmetic and the Logic of Combination', 'planned', 'A practical article on addition, multiplication, scaling, and structural interpretation.');
