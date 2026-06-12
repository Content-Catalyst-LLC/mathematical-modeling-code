{-# OPTIONS_GHC -Wall #-}

module Main where

data ModelPurpose
  = Explanation
  | Prediction
  | Control
  | DecisionSupport
  | Simulation
  | Optimization
  deriving (Eq, Show)

data UseStatus
  = Supported
  | Exploratory
  | RequiresValidation
  | Prohibited
  deriving (Eq, Show)

data ValidationRequirement
  = MechanismReview
  | ForecastValidation
  | StabilityAndRobustness
  | DecisionContextReview
  | ObjectiveSensitivity
  | ScenarioAdequacy
  deriving (Eq, Show)

data PurposeRecord = PurposeRecord
  { purpose :: ModelPurpose
  , primaryQuestion :: String
  , validationRequirement :: ValidationRequirement
  , useStatus :: UseStatus
  , misuseRisk :: String
  } deriving (Eq, Show)

records :: [PurposeRecord]
records =
  [ PurposeRecord
      Explanation
      "Why does the system behave this way?"
      MechanismReview
      Supported
      "Plausible mechanism treated as validated cause."
  , PurposeRecord
      Prediction
      "What is likely to happen?"
      ForecastValidation
      RequiresValidation
      "Forecast used beyond validation horizon."
  , PurposeRecord
      Control
      "What action should steer the system?"
      StabilityAndRobustness
      RequiresValidation
      "Action taken without robustness or monitoring."
  , PurposeRecord
      DecisionSupport
      "Which alternative should be considered?"
      DecisionContextReview
      Exploratory
      "Decision support becomes decision substitution."
  , PurposeRecord
      Optimization
      "Which feasible option best satisfies the objective?"
      ObjectiveSensitivity
      RequiresValidation
      "Objective function treated as complete value system."
  ]

needsWarning :: PurposeRecord -> Bool
needsWarning record =
  case useStatus record of
    Supported -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed model-purpose records:"
  mapM_ print records
  putStrLn "\nRecords requiring use warning:"
  mapM_ print (filter needsWarning records)
