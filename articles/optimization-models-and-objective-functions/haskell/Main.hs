{-# OPTIONS_GHC -Wall #-}

module Main where

data OptimizationComponent
  = DecisionVariable
  | ObjectiveFunction
  | Constraint
  | Parameter
  | FeasibleRegion
  | SolverSetting
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data OptimizationRecord = OptimizationRecord
  { key :: String
  , component :: OptimizationComponent
  , expression :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

optimizationRegister :: [OptimizationRecord]
optimizationRegister =
  [ OptimizationRecord
      "decision_variables"
      DecisionVariable
      "x_i"
      "Allocation to program i."
      "Controllability."
      Active
  , OptimizationRecord
      "objective_function"
      ObjectiveFunction
      "maximize sum_i benefit_i * x_i"
      "Maximize estimated total benefit."
      "Goal validity and distributional effects."
      RequiresReview
  , OptimizationRecord
      "budget_constraint"
      Constraint
      "sum_i cost_i * x_i <= B"
      "Total cost cannot exceed budget."
      "Cost completeness."
      RequiresReview
  , OptimizationRecord
      "equity_floor"
      Constraint
      "x_i >= floor"
      "Each program receives a minimum allocation."
      "Equity and feasibility."
      RequiresSensitivityTest
  ]

needsReview :: OptimizationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed optimization model records:"
  mapM_ print optimizationRegister

  putStrLn "\nOptimization records requiring review:"
  mapM_ print (filter needsReview optimizationRegister)
