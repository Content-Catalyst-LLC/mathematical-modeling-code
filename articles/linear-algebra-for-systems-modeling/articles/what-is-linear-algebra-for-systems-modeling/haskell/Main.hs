module Main where

data MatrixSystemRecord = MatrixSystemRecord
  { modelName :: String
  , rows :: Int
  , columns :: Int
  , matrixRank :: Int
  , determinant :: Double
  , dominantEigenvalue :: Double
  , matrixMeaning :: String
  , interpretationWarning :: String
  } deriving (Show)

determinant2x2 :: [[Double]] -> Double
determinant2x2 matrix =
  ((matrix !! 0) !! 0) * ((matrix !! 1) !! 1)
  - ((matrix !! 0) !! 1) * ((matrix !! 1) !! 0)

trace2x2 :: [[Double]] -> Double
trace2x2 matrix =
  ((matrix !! 0) !! 0) + ((matrix !! 1) !! 1)

eigenvalues2x2 :: [[Double]] -> (Double, Double)
eigenvalues2x2 matrix =
  let tr = trace2x2 matrix
      det = determinant2x2 matrix
      disc = tr * tr - 4.0 * det
      root = sqrt disc
  in ((tr + root) / 2.0, (tr - root) / 2.0)

rank2x2 :: [[Double]] -> Int
rank2x2 matrix =
  if abs (determinant2x2 matrix) > 1e-10 then 2 else 1

buildRecord :: MatrixSystemRecord
buildRecord =
  let matrix = [[0.80, 0.15], [0.20, 0.90]]
      (lambda1, lambda2) = eigenvalues2x2 matrix
      dominant = max (abs lambda1) (abs lambda2)
  in MatrixSystemRecord
      "two_component_transition_model"
      2
      2
      (rank2x2 matrix)
      (determinant2x2 matrix)
      dominant
      "transition-like matrix connecting two system components across a modeling step"
      "Matrix interpretation depends on entry meaning, scale, and model assumptions."

main :: IO ()
main = print buildRecord
