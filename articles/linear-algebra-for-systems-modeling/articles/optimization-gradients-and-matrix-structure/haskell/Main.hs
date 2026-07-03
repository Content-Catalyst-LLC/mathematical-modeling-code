module Main where

data OptimizationMatrixAudit = OptimizationMatrixAudit
  { modelName :: String
  , observations :: Int
  , features :: Int
  , objective :: String
  , solver :: String
  , regularizationStrength :: Double
  , featureMatrixConditionNumber :: Double
  , hessianConditionNumber :: Double
  , gradientNormFinal :: Double
  , objectiveInitial :: Double
  , objectiveFinal :: Double
  , closedFormGapNorm :: Double
  , trainingRmse :: Double
  , convergenceWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: OptimizationMatrixAudit
buildAudit =
  OptimizationMatrixAudit
    "synthetic_optimization_gradient_matrix_audit"
    10
    5
    "mean_squared_error_plus_l2_regularization"
    "fixed_step_gradient_descent_compared_with_closed_form_ridge_solution"
    0.75
    18.4
    3.8
    0.0009
    52.0
    4.3
    0.002
    1.9
    "Gradient descent depends on step size, scaling, conditioning, stopping rules, and objective curvature."
    "The optimized parameter vector solves a chosen objective under assumptions, not automatic causal evidence or policy."

main :: IO ()
main =
  print buildAudit
