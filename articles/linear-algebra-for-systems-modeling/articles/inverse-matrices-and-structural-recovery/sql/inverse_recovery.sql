-- Inverse Matrices and Structural Recovery
-- Demonstrates the 2x2 inverse idea using tables.

DROP TABLE IF EXISTS matrix_a;
DROP TABLE IF EXISTS vector_b;

CREATE TABLE matrix_a (
  row_id INTEGER,
  col_id INTEGER,
  value REAL
);

CREATE TABLE vector_b (
  row_id INTEGER,
  value REAL
);

INSERT INTO matrix_a VALUES
(1, 1, 3), (1, 2, 1),
(2, 1, 2), (2, 2, 4);

INSERT INTO vector_b VALUES
(1, 7),
(2, 8);

-- For A = [[3,1],[2,4]], determinant = 10.
-- A^-1 = 1/10 * [[4,-1],[-2,3]]
-- Recovered x = A^-1 b.

SELECT
  'x1' AS component,
  (4.0 * (SELECT value FROM vector_b WHERE row_id = 1)
   -1.0 * (SELECT value FROM vector_b WHERE row_id = 2)) / 10.0 AS recovered_value
UNION ALL
SELECT
  'x2' AS component,
  (-2.0 * (SELECT value FROM vector_b WHERE row_id = 1)
   +3.0 * (SELECT value FROM vector_b WHERE row_id = 2)) / 10.0 AS recovered_value;
