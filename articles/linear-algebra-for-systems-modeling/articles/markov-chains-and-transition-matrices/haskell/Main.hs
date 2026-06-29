module Main where

data MarkovAudit = MarkovAudit
  { systemName :: String
  , states :: String
  , orientation :: String
  , transitionMatrix :: String
  , initialDistribution :: String
  , rowSumError :: Double
  , nonnegative :: Bool
  , oneStepDistribution :: String
  , tenStepDistribution :: String
  , steadyStateEstimate :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: MarkovAudit
buildAudit =
  MarkovAudit
    "infrastructure_condition_transition_audit"
    "good|fair|poor"
    "row_stochastic_row_vector_update_pi_next_equals_pi_P"
    "0.820000,0.160000,0.020000;0.100000,0.760000,0.140000;0.030000,0.220000,0.750000"
    "0.600000,0.300000,0.100000"
    0.0
    True
    "0.525000,0.346000,0.129000"
    "0.286282,0.478868,0.234850"
    "0.233333,0.488889,0.277778"
    "Transition matrices depend on state definitions, time step, stationarity, data quality, and the Markov assumption."

main :: IO ()
main =
  print buildAudit
