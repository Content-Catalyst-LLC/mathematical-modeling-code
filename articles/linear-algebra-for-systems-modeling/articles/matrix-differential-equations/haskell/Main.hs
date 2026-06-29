module Main where

data MatrixDifferentialAudit = MatrixDifferentialAudit
  { systemName :: String
  , stateNames :: String
  , systemMatrix :: String
  , initialState :: String
  , timeHorizon :: Double
  , eigenvalues :: String
  , maxRealPart :: Double
  , stabilityClassification :: String
  , finalStateEstimate :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: MatrixDifferentialAudit
buildAudit =
  MatrixDifferentialAudit
    "two_state_matrix_differential_equation_audit"
    "infrastructure_stress|service_delay"
    "-0.280000,0.080000;0.120000,-0.340000"
    "10.000000,4.000000"
    10.0
    "-0.200000,-0.420000"
    (-0.20)
    "asymptotically_stable_continuous_time"
    "1.558000,0.882000"
    "Matrix differential equations depend on state definitions, units, time scale, solver choices, stiffness review, and domain constraints."

main :: IO ()
main =
  print buildAudit
