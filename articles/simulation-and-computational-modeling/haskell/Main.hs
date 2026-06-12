{-# OPTIONS_GHC -Wall #-}

module Main where

data SimulationComponent
  = StateDefinition
  | UpdateRule
  | NumericalMethod
  | ScenarioDefinition
  | StochasticProtocol
  | OutputMetric
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data SimulationRecord = SimulationRecord
  { key :: String
  , component :: SimulationComponent
  , computationalStructure :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

simulationRegister :: [SimulationRecord]
simulationRegister =
  [ SimulationRecord
      "state_variable"
      StateDefinition
      "resource_stock"
      "The model tracks resource stock over time."
      "State definition."
      RequiresReview
  , SimulationRecord
      "update_rule"
      UpdateRule
      "R_next = R + growth - extraction - shock"
      "Stock changes through regeneration, extraction, and stochastic shocks."
      "Equation-code alignment."
      RequiresValidation
  , SimulationRecord
      "time_step"
      NumericalMethod
      "discrete annual step"
      "The model advances in equal time increments."
      "Numerical appropriateness."
      RequiresReview
  , SimulationRecord
      "ensemble_protocol"
      StochasticProtocol
      "multiple random seeds per scenario"
      "Stochastic variation is summarized across replications."
      "Replication adequacy."
      Active
  ]

needsReview :: SimulationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed simulation model records:"
  mapM_ print simulationRegister

  putStrLn "\nSimulation records requiring review:"
  mapM_ print (filter needsReview simulationRegister)
