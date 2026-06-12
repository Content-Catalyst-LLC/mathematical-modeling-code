{-# OPTIONS_GHC -Wall #-}

module Main where

data DynamicComponent
  = StateVariable
  | RateEquation
  | InitialCondition
  | BoundaryCondition
  | Parameter
  | NumericalSetting
  | OutputDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data DynamicRecord = DynamicRecord
  { key :: String
  , component :: DynamicComponent
  , expression :: String
  , interpretation :: String
  , unitsOrDomain :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

dynamicRegister :: [DynamicRecord]
dynamicRegister =
  [ DynamicRecord
      "storage"
      StateVariable
      "S(t)"
      "Current resource storage."
      "resource units"
      Active
  , DynamicRecord
      "storage_rate"
      RateEquation
      "dS/dt = I - D - lambda*S"
      "Storage changes through inflow, demand, and proportional loss."
      "resource units per time"
      RequiresReview
  , DynamicRecord
      "initial_storage"
      InitialCondition
      "S(0) = S0"
      "Initial system state."
      "0 <= S0 <= K"
      RequiresValidation
  , DynamicRecord
      "capacity_boundary"
      BoundaryCondition
      "0 <= S(t) <= K"
      "Storage remains within physical bounds."
      "bounded domain"
      RequiresReview
  , DynamicRecord
      "time_step"
      NumericalSetting
      "dt"
      "Numerical integration step size."
      "positive time increment"
      RequiresSensitivityTest
  ]

needsReview :: DynamicRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed dynamic model records:"
  mapM_ print dynamicRegister

  putStrLn "\nDynamic records requiring review:"
  mapM_ print (filter needsReview dynamicRegister)
