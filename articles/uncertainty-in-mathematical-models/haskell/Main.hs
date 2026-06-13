{-# OPTIONS_GHC -Wall #-}

module Main where

data UncertaintyLayer
  = DataUncertainty
  | ParameterUncertainty
  | ModelFormUncertainty
  | ScenarioUncertainty
  | AleatoryUncertainty
  | DecisionUncertainty
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresMonitoring
  | Revise
  deriving (Eq, Show)

data UncertaintyRecord = UncertaintyRecord
  { key :: String
  , layer :: UncertaintyLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

uncertaintyRegister :: [UncertaintyRecord]
uncertaintyRegister =
  [ UncertaintyRecord
      "measurement_uncertainty"
      DataUncertainty
      "Reviews uncertainty in observed or input values."
      "Data quality and measurement error."
      Active
  , UncertaintyRecord
      "parameter_uncertainty"
      ParameterUncertainty
      "Documents plausible parameter ranges."
      "Parameter intervals and sensitivity."
      RequiresReview
  , UncertaintyRecord
      "structural_uncertainty"
      ModelFormUncertainty
      "Reviews uncertainty about the model structure."
      "Alternative model forms."
      RequiresReview
  , UncertaintyRecord
      "scenario_uncertainty"
      ScenarioUncertainty
      "Documents uncertainty about future conditions."
      "Scenario assumptions."
      RequiresReview
  , UncertaintyRecord
      "aleatory_variability"
      AleatoryUncertainty
      "Represents irreducible variability."
      "Random variation."
      RequiresValidation
  , UncertaintyRecord
      "decision_uncertainty"
      DecisionUncertainty
      "Connects uncertainty to thresholds and action."
      "Decision stability."
      RequiresMonitoring
  ]

needsReview :: UncertaintyRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed uncertainty records:"
  mapM_ print uncertaintyRegister

  putStrLn "\nUncertainty records requiring review:"
  mapM_ print (filter needsReview uncertaintyRegister)
