module Main where

data ScalingNormalizationAudit = ScalingNormalizationAudit
  { workflowName :: String
  , matrixShape :: String
  , rowMeaning :: String
  , columnMeaning :: String
  , rawColumnNorm1 :: Double
  , rawColumnNorm2 :: Double
  , standardizedColumnNorm1 :: Double
  , standardizedColumnNorm2 :: Double
  , rawConditionProxy :: Double
  , standardizedConditionProxy :: Double
  , comparisonWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: ScalingNormalizationAudit
buildAudit =
  ScalingNormalizationAudit
    "scaling_normalization_audit"
    "3x2"
    "infrastructure_zones"
    "annual_demand_and_outage_exposure"
    2345.21
    0.1749
    1.4142
    1.4142
    13406.31
    1.0
    "Raw units compare magnitude; standardized columns compare relative position; row normalization compares composition; unit-vector normalization compares direction."
    "Scaling and normalization change what comparison means. Every transformed matrix should record original units, transformation rule, purpose, and interpretation limits."

main :: IO ()
main =
  print buildAudit
