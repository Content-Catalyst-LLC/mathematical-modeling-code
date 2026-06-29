module Main where

data LinearDynamicsAudit = LinearDynamicsAudit
  { systemName :: String
  , stateNames :: String
  , updateMatrix :: String
  , initialState :: String
  , horizon :: Int
  , finalState :: String
  , spectralRadius :: Double
  , stabilityClassification :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: LinearDynamicsAudit
buildAudit =
  LinearDynamicsAudit
    "two_state_linear_dynamics_audit"
    "infrastructure_stress|service_delay"
    "0.820000,0.120000;0.180000,0.760000"
    "10.000000,4.000000"
    20
    "3.626170,3.452104"
    0.94
    "asymptotically_stable_discrete_time"
    "Linear dynamics depend on state definitions, units, scaling, time step, matrix validity, and whether linearity is structural or approximate."

main :: IO ()
main =
  print buildAudit
