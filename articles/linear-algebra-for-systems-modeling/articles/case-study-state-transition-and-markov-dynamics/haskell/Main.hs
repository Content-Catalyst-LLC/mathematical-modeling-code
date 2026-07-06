module Main where

data StateTransitionMarkovAudit = StateTransitionMarkovAudit
  { workflowName :: String
  , scenarioName :: String
  , stateCount :: Int
  , timeSteps :: Int
  , stochasticCheckPassed :: Bool
  , initialPrimaryState :: String
  , highestProbabilityStateAfterHorizon :: String
  , highestProbabilityAfterHorizon :: Double
  , stationaryHighestProbabilityState :: String
  , stationaryHighestProbability :: Double
  , stressDisruptedProbabilityAfterHorizon :: Double
  , baselineDisruptedProbabilityAfterHorizon :: Double
  , memorylessWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: StateTransitionMarkovAudit
buildAudit =
  StateTransitionMarkovAudit
    "state_transition_markov_audit"
    "synthetic_infrastructure_condition_transition_model"
    4
    5
    True
    "normal"
    "normal"
    0.42833125
    "normal"
    0.40602189781
    0.41016825
    0.1756128125
    "The Markov assumption treats the current state as sufficient for predicting the next state."
    "Stationary distributions and multi-step probabilities describe the model, not guaranteed system destiny."

main :: IO ()
main =
  print buildAudit
