module Main where

data MatrixArithmeticAudit = MatrixArithmeticAudit
  { operationName :: String
  , matrixShape :: String
  , rowMeaning :: String
  , columnMeaning :: String
  , units :: String
  , weights :: String
  , compatibleShape :: Bool
  , outputEntrySum :: Double
  , interpretationWarning :: String
  } deriving (Show)

type Matrix = [[Double]]

sameShape :: Matrix -> Matrix -> Bool
sameShape a b =
  length a == length b &&
  all (\(rowA, rowB) -> length rowA == length rowB) (zip a b)

addMatrices :: Matrix -> Matrix -> Matrix
addMatrices a b =
  zipWith (zipWith (+)) a b

scaleMatrix :: Double -> Matrix -> Matrix
scaleMatrix alpha =
  map (map (* alpha))

entrySum :: Matrix -> Double
entrySum matrix =
  sum (map sum matrix)

buildAudit :: MatrixArithmeticAudit
buildAudit =
  let baseline =
        [ [10.0, 2.0, 0.0]
        , [1.0, 12.0, 3.0]
        , [0.0, 4.0, 8.0]
        ]
      intervention =
        [ [1.0, 0.5, 0.0]
        , [0.2, 1.5, 0.4]
        , [0.0, 0.7, 1.2]
        ]
      stress =
        [ [-0.5, -0.2, 0.0]
        , [-0.1, -0.8, -0.3]
        , [0.0, -0.4, -0.9]
        ]
      combinedChange = addMatrices intervention (scaleMatrix 0.5 stress)
      future = addMatrices baseline combinedChange
      difference = addMatrices future (scaleMatrix (-1.0) baseline)
  in MatrixArithmeticAudit
      "baseline_plus_weighted_intervention_and_stress"
      "3x3"
      "infrastructure subsystem"
      "performance relationship or dependency category"
      "normalized condition-effect score"
      "1.0 intervention effect plus 0.5 stress effect"
      (sameShape baseline intervention && sameShape baseline stress)
      (entrySum difference)
      "Shape compatibility is not enough; rows, columns, units, baselines, and effect definitions must align."

main :: IO ()
main =
  print buildAudit
