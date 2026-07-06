module Main where

data MachineLearningPipelineAudit = MachineLearningPipelineAudit
  { workflowName :: String
  , scenarioName :: String
  , observationCount :: Int
  , featureCount :: Int
  , trainCount :: Int
  , testCount :: Int
  , modelFamily :: String
  , regularizationStrength :: Double
  , testRmse :: Double
  , maxAbsoluteResidual :: Double
  , largestWeightFeature :: String
  , preprocessingSummary :: String
  , leakageWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: MachineLearningPipelineAudit
buildAudit =
  MachineLearningPipelineAudit
    "machine_learning_linear_structure_audit"
    "synthetic_infrastructure_risk_pipeline"
    10
    4
    7
    3
    "ridge_regression_linear_baseline"
    0.25
    0.041
    0.061
    "inspection_gap"
    "Training means and scales were fit on training rows only and then applied to test rows."
    "Full-data preprocessing can leak evaluation information into the model."
    "Coefficients and predictions are not automatic causal explanations or decision rules."

main :: IO ()
main =
  print buildAudit
