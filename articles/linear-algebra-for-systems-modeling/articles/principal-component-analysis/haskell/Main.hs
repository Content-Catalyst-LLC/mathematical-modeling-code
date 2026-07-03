module Main where

data PCADiagnosticAudit = PCADiagnosticAudit
  { modelName :: String
  , observations :: Int
  , variables :: Int
  , preprocessing :: String
  , retainedComponents :: Int
  , explainedVarianceRatio :: String
  , cumulativeExplainedVariance :: Double
  , relativeReconstructionError :: Double
  , largestLoadingVariablePC1 :: String
  , largestLoadingVariablePC2 :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: PCADiagnosticAudit
buildAudit =
  PCADiagnosticAudit
    "synthetic_pca_diagnostic_audit"
    8
    5
    "centered_and_standardized"
    2
    "0.946;0.044;0.007;0.002;0.001"
    0.990
    0.100
    "transport_delay"
    "water_demand"
    "PCA components depend on data matrix construction, centering, scaling, outliers, retained-rank choice, explained-variance criteria, residual review, and domain interpretation."

main :: IO ()
main =
  print buildAudit
