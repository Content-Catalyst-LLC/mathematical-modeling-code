module Main where

data LinearityDistortionAudit = LinearityDistortionAudit
  { workflowName :: String
  , modelPurpose :: String
  , fittedIntercept :: Double
  , fittedSlope :: Double
  , residualSumSquares :: Double
  , maxAbsoluteResidual :: Double
  , residualSignPattern :: String
  , curvatureWarning :: String
  , extrapolationWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: LinearityDistortionAudit
buildAudit =
  LinearityDistortionAudit
    "linearity_distortion_audit"
    "baseline_linear_approximation_for_system_behavior"
    0.3
    2.1
    0.98
    0.7
    "+--0+"
    "Residuals show a structured sign pattern consistent with curvature. The linear fit is useful as a baseline but risks distortion if interpreted as the system mechanism."
    "Do not extrapolate the fitted line beyond the observed operating range without additional validation."
    "Linear models clarify first-order structure, but residuals, thresholds, interactions, feedback, aggregation, and causal assumptions must be reviewed before using results for decisions."

main :: IO ()
main =
  print buildAudit
