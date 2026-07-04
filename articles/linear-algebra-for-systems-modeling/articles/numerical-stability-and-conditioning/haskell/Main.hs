module Main where

data StabilityConditioningAudit = StabilityConditioningAudit
  { modelName :: String
  , matrixCase :: String
  , matrixShape :: String
  , determinantValue :: Double
  , conditionNumberProxy :: Double
  , solutionNorm :: Double
  , residualNorm :: Double
  , relativeResidual :: Double
  , perturbationSize :: Double
  , perturbedSolutionChange :: Double
  , stabilityStatus :: String
  , interpretationWarning :: String
  } deriving (Show)

wellConditionedAudit :: StabilityConditioningAudit
wellConditionedAudit =
  StabilityConditioningAudit
    "numerical_stability_conditioning_audit"
    "well_conditioned_system"
    "2x2"
    5.75
    2.10
    0.34
    0.0
    0.0
    0.00001
    0.000004
    "stable_under_demo_threshold"
    "Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose."

illConditionedAudit :: StabilityConditioningAudit
illConditionedAudit =
  StabilityConditioningAudit
    "numerical_stability_conditioning_audit"
    "ill_conditioned_system"
    "2x2"
    0.00000001
    399920000.0
    50000000.0
    0.0
    0.0
    0.00001
    2000.0
    "review_required_ill_conditioned"
    "Residuals should be interpreted alongside conditioning, scaling, perturbation sensitivity, solver method, precision, and model purpose."

main :: IO ()
main =
  mapM_ print [wellConditionedAudit, illConditionedAudit]
