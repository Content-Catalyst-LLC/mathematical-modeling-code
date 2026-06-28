-- Inverse Matrices and Structural Recovery
-- SQL representation of a 2x2 recovery problem with residual checks.

DROP TABLE IF EXISTS matrix_a;
DROP TABLE IF EXISTS vector_b;
DROP TABLE IF EXISTS recovered_x;

CREATE TABLE matrix_a (
  row_id INTEGER,
  col_id INTEGER,
  value REAL
);

CREATE TABLE vector_b (
  row_id INTEGER,
  value REAL
);

CREATE TABLE recovered_x (
  component INTEGER,
  value REAL
);

INSERT INTO matrix_a VALUES
(1, 1, 3), (1, 2, 1),
(2, 1, 2), (2, 2, 4);

INSERT INTO vector_b VALUES
(1, 7),
(2, 8);

-- For A = [[3,1],[2,4]], determinant = 10.
-- A^-1 = 1/10 * [[4,-1],[-2,3]].

INSERT INTO recovered_x
SELECT
  1 AS component,
  (4.0 * (SELECT value FROM vector_b WHERE row_id = 1)
   -1.0 * (SELECT value FROM vector_b WHERE row_id = 2)) / 10.0 AS value
UNION ALL
SELECT
  2 AS component,
  (-2.0 * (SELECT value FROM vector_b WHERE row_id = 1)
   +3.0 * (SELECT value FROM vector_b WHERE row_id = 2)) / 10.0 AS value;

-- Reconstruct Ax and compare with b.
SELECT
  a.row_id,
  SUM(a.value * x.value) AS reconstructed_b,
  b.value AS observed_b,
  SUM(a.value * x.value) - b.value AS residual
FROM matrix_a a
JOIN recovered_x x
  ON a.col_id = x.component
JOIN vector_b b
  ON a.row_id = b.row_id
GROUP BY a.row_id, b.value
ORDER BY a.row_id;
