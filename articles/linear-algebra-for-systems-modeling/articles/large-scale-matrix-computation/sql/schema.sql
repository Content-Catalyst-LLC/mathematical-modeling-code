CREATE TABLE IF NOT EXISTS article_status (
  slug TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  status TEXT NOT NULL,
  systems_modeling_note TEXT
);

INSERT OR REPLACE INTO article_status (slug, title, status, systems_modeling_note)
VALUES ('large-scale-matrix-computation', 'Large-Scale Matrix Computation', 'planned', 'A practical article on computational workflows for large matrices, high-dimensional structure, and scalable numerical reasoning.');
