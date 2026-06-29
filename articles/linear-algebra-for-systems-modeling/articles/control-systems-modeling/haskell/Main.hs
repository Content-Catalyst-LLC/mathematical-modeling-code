module Main where

data ControlSystemsAudit = ControlSystemsAudit
  { systemName :: String
  , timeModel :: String
  , stateMatrixA :: String
  , inputMatrixB :: String
  , outputMatrixC :: String
  , feedbackMatrixK :: String
  , openLoopEigenvalues :: String
  , closedLoopEigenvalues :: String
  , controllabilityRank :: Int
  , observabilityRank :: Int
  , controlWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: ControlSystemsAudit
buildAudit =
  ControlSystemsAudit
    "two_state_control_system_audit"
    "continuous_time_linear_state_space"
    "0.100000,1.000000;0.000000,0.200000"
    "0.000000;1.000000"
    "1.000000,0.000000"
    "0.500000,1.400000"
    "0.200000,0.100000"
    "-0.600000,-0.500000"
    2
    2
    "The feedback law is evaluated without actuator saturation, delay, noise, or uncertainty."
    "Control models require state definition, input authority, output reliability, constraint checks, objective transparency, and domain accountability."

main :: IO ()
main =
  print buildAudit
