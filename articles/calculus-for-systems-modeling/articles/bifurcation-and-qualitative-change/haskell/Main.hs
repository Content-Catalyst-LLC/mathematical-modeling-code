module Main where

data BifurcationRecord = BifurcationRecord
  { model :: String
  , parameterMu :: Double
  , equilibrium :: Maybe Double
  , derivativeValue :: Maybe Double
  , stability :: String
  , branchStatus :: String
  , warning :: String
  } deriving (Show)

saddleNodeEquilibria :: Double -> [Double]
saddleNodeEquilibria mu
  | mu < 0 = []
  | abs mu < 1e-12 = [0]
  | otherwise = [-sqrt mu, sqrt mu]

saddleNodeDerivative :: Double -> Double
saddleNodeDerivative x =
  -2 * x

classifyScalarStability :: Double -> String
classifyScalarStability derivativeValue
  | derivativeValue < (-1e-8) = "locally_stable"
  | derivativeValue > 1e-8 = "locally_unstable"
  | otherwise = "inconclusive_at_critical_value"

recordForEquilibrium :: Double -> Double -> BifurcationRecord
recordForEquilibrium mu eq =
  let derivative = saddleNodeDerivative eq
      status = if abs mu < 1e-12 then "critical_branch" else "equilibrium_present"
  in BifurcationRecord
      "saddle_node_normal_form"
      mu
      (Just eq)
      (Just derivative)
      (classifyScalarStability derivative)
      status
      "Bifurcation interpretation depends on model form, parameter meaning, and domain validity."

recordsForParameter :: Double -> [BifurcationRecord]
recordsForParameter mu =
  case saddleNodeEquilibria mu of
    [] ->
      [ BifurcationRecord
          "saddle_node_normal_form"
          mu
          Nothing
          Nothing
          "no_real_equilibrium"
          "equilibrium_absent"
          "For mu below zero, the saddle-node normal form has no real equilibrium."
      ]
    equilibria -> map (recordForEquilibrium mu) equilibria

parameterValues :: [Double]
parameterValues =
  [fromIntegral step / 10 | step <- [-20..40]]

main :: IO ()
main =
  mapM_ print (concatMap recordsForParameter parameterValues)
