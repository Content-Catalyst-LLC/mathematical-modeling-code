{-# OPTIONS_GHC -Wall #-}

module Main where

data WorkflowStage
  = DataIntake
  | ParameterControl
  | ModelExecution
  | OutputGeneration
  | Reproducibility
  | Validation
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresReproducibilityCheck
  | Revise
  deriving (Eq, Show)

data WorkflowRecord = WorkflowRecord
  { key :: String
  , stage :: WorkflowStage
  , computationalObject :: String
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

workflowRegister :: [WorkflowRecord]
workflowRegister =
  [ WorkflowRecord
      "input_schema"
      DataIntake
      "resource_scenario_fields"
      "Defines required model inputs and units."
      "Input validity."
      RequiresReview
  , WorkflowRecord
      "configuration"
      ParameterControl
      "scenario configuration"
      "Separates run-specific values from code."
      "Parameter traceability."
      Active
  , WorkflowRecord
      "simulation_engine"
      ModelExecution
      "resource update loop"
      "Implements the model's state transition rule."
      "Code-model alignment."
      RequiresValidation
  , WorkflowRecord
      "run_manifest"
      Reproducibility
      "manifest json"
      "Records command, environment, seed, and outputs."
      "Rerun capability."
      RequiresReproducibilityCheck
  , WorkflowRecord
      "audit_card"
      Governance
      "workflow audit card"
      "Summarizes checks, outputs, and limitations."
      "Decision-support governance."
      RequiresReview
  ]

needsReview :: WorkflowRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed scientific computing workflow records:"
  mapM_ print workflowRegister

  putStrLn "\nWorkflow records requiring review:"
  mapM_ print (filter needsReview workflowRegister)
