module Main where

data MatrixStructureAudit = MatrixStructureAudit
  { matrixName :: String
  , matrixRole :: String
  , rowMeaning :: String
  , columnMeaning :: String
  , rowCount :: Int
  , columnCount :: Int
  , nonzeroEntries :: Int
  , symmetricMatrix :: Bool
  , interpretationWarning :: String
  } deriving (Show)

countNonzero :: [[Double]] -> Int
countNonzero matrix =
  length [value | row <- matrix, value <- row, value /= 0.0]

isSymmetric :: [[Double]] -> Bool
isSymmetric matrix =
  let n = length matrix
      square = all ((== n) . length) matrix
      pairs = [(i, j) | i <- [0..n-1], j <- [0..n-1]]
  in square && all (\(i, j) -> (matrix !! i) !! j == (matrix !! j) !! i) pairs

buildAudit :: MatrixStructureAudit
buildAudit =
  let matrix =
        [ [0.0, 2.0, 0.0, 1.0]
        , [2.0, 0.0, 3.0, 0.0]
        , [0.0, 3.0, 0.0, 4.0]
        , [1.0, 0.0, 4.0, 0.0]
        ]
  in MatrixStructureAudit
      "infrastructure_interdependency_matrix"
      "weighted adjacency matrix"
      "infrastructure subsystem receiving or indexed by relationship"
      "infrastructure subsystem sending or paired by relationship"
      (length matrix)
      (length (head matrix))
      (countNonzero matrix)
      (isSymmetric matrix)
      "Matrix symmetry should not be assumed unless system relationships are reciprocal."

main :: IO ()
main =
  print buildAudit
