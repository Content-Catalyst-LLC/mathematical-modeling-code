module Main where

data SVDDiagnosticAudit = SVDDiagnosticAudit
  { modelName :: String
  , rows :: Int
  , columns :: Int
  , singularValues :: String
  , numericalRank :: Int
  , rankTolerance :: Double
  , conditionNumber :: Double
  , retainedRank :: Int
  , explainedEnergyRetained :: Double
  , relativeReconstructionError :: Double
  , pseudoinverseWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: SVDDiagnosticAudit
buildAudit =
  SVDDiagnosticAudit
    "synthetic_svd_diagnostic_audit"
    6
    4
    "14.35;8.16;0.19;0.04"
    4
    1e-10
    358.75
    2
    0.9992
    0.0283
    "Small singular values can amplify noise when inverted; use rank tolerance, truncated SVD, or regularization when conditioning is poor."
    "SVD components depend on matrix construction, preprocessing, scaling, centering, rank tolerance, retained-rank choice, numerical method, and domain interpretation."

main :: IO ()
main =
  print buildAudit
