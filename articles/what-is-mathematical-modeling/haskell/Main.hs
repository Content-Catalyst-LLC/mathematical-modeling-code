{-# OPTIONS_GHC -Wall #-}

module Main where

data ModelPurpose
  = Explanation
  | Prediction
  | Simulation
  | Optimization
  | DecisionSupport
  | Governance
  deriving (Eq, Show)

data EvidenceStatus
  = Assumed
  | Synthetic
  | Calibrated
  | Validated
  | RequiresReview
  deriving (Eq, Show)

data ModelComponent
  = StateVariable String
  | Parameter String
  | Assumption String
  | Constraint String
  | OutputMetric String
  deriving (Eq, Show)

data ModelingRecord = ModelingRecord
  { component :: ModelComponent
  , purpose :: ModelPurpose
  , evidenceStatus :: EvidenceStatus
  , statement :: String
  , reviewQuestion :: String
  } deriving (Eq, Show)

records :: [ModelingRecord]
records =
  [ ModelingRecord
      (StateVariable "x(t)")
      Simulation
      Assumed
      "The state variable represents the modeled quantity over time."
      "Does a single aggregate state preserve the structure needed for the question?"
  , ModelingRecord
      (Parameter "r")
      Simulation
      RequiresReview
      "The growth rate controls the rate of change."
      "Is the growth rate estimated, assumed, calibrated, or scenario-based?"
  , ModelingRecord
      (Parameter "K")
      Simulation
      RequiresReview
      "The carrying capacity represents an upper bound."
      "Is capacity fixed, time-varying, empirical, or conceptual?"
  , ModelingRecord
      (Assumption "bounded growth")
      Explanation
      RequiresReview
      "Growth slows as the state approaches carrying capacity."
      "What evidence supports bounded rather than exponential growth?"
  , ModelingRecord
      (OutputMetric "final state")
      DecisionSupport
      Synthetic
      "Final state is one summary output of the model."
      "Does this output answer the intended modeling question?"
  ]

requiresReview :: ModelingRecord -> Bool
requiresReview item =
  case evidenceStatus item of
    RequiresReview -> True
    Assumed -> True
    _ -> False

main :: IO ()
main = do
  putStrLn "Typed mathematical modeling records:"
  mapM_ print records
  putStrLn "\nRecords requiring review:"
  mapM_ print (filter requiresReview records)
