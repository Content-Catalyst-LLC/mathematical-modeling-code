{-# OPTIONS_GHC -Wall #-}

module Main where

data NumericalComponent
  = TimeStepMethod
  | Discretization
  | SolverTolerance
  | ConvergenceDiagnostic
  | StabilityDiagnostic
  | StateConstraint
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data NumericalRecord = NumericalRecord
  { key :: String
  , component :: NumericalComponent
  , numericalStructure :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

numericalRegister :: [NumericalRecord]
numericalRegister =
  [ NumericalRecord
      "euler_step"
      TimeStepMethod
      "R_next = R + h * f(R)"
      "Euler stepping approximates continuous resource dynamics."
      "Method suitability."
      RequiresReview
  , NumericalRecord
      "step_size"
      Discretization
      "h in {1.0, 0.5, 0.25, 0.1}"
      "Step size controls time discretization."
      "Step-size sensitivity."
      RequiresSensitivityTest
  , NumericalRecord
      "convergence_diagnostic"
      ConvergenceDiagnostic
      "compare final stock across h"
      "Convergence is assessed by comparing refined approximations."
      "Approximation credibility."
      Active
  , NumericalRecord
      "nonnegative_constraint"
      StateConstraint
      "R = max(0, R)"
      "Resource stock is constrained to remain nonnegative."
      "Constraint interpretation."
      RequiresReview
  ]

needsReview :: NumericalRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed numerical method records:"
  mapM_ print numericalRegister

  putStrLn "\nNumerical records requiring review:"
  mapM_ print (filter needsReview numericalRegister)
