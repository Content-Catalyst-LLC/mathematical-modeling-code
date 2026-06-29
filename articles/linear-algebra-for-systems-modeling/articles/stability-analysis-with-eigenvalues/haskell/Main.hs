module Main where

data StabilityAudit = StabilityAudit
  { systemName :: String
  , matrixEntries :: String
  , eigenvalueOne :: Double
  , eigenvalueTwo :: Double
  , spectralRadius :: Double
  , discreteTimeClassification :: String
  , continuousTimeClassification :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: StabilityAudit
buildAudit =
  StabilityAudit
    "two_mode_stability_audit"
    "0.820000,0.120000;0.180000,0.760000"
    0.94
    0.64
    0.94
    "asymptotically_stable_discrete_time"
    "unstable_continuous_time_if_interpreted_as_generator"
    "Stability rules depend on whether the matrix is a discrete-time update, continuous-time generator, or local linearization."

main :: IO ()
main =
  print buildAudit
