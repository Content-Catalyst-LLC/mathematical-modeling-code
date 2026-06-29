module Main where

data LongRunTransitionAudit = LongRunTransitionAudit
  { systemName :: String
  , states :: String
  , orientation :: String
  , transitionMatrix :: String
  , stationaryEstimate :: String
  , distributionAfter25Steps :: String
  , convergenceDistance :: Double
  , initialConditionWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: LongRunTransitionAudit
buildAudit =
  LongRunTransitionAudit
    "long_run_infrastructure_condition_transition_audit"
    "good|fair|poor"
    "row_stochastic_row_vector_update_pi_next_equals_pi_P"
    "0.820000,0.160000,0.020000;0.100000,0.760000,0.140000;0.030000,0.220000,0.750000"
    "0.233333,0.488889,0.277778"
    "0.236019,0.487126,0.276855"
    0.005372
    "Initial-condition effects may fade, persist, or determine absorbing outcomes depending on transition structure."
    "Long-run transition claims require state definitions, time-step clarity, stationarity review, convergence diagnostics, and domain interpretation."

main :: IO ()
main =
  print buildAudit
