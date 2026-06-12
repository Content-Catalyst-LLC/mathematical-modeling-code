{-# OPTIONS_GHC -Wall #-}

module Main where

data VariableRole
  = StateVariable
  | InputVariable
  | OutputVariable
  | Parameter
  | DerivedDiagnostic
  | LatentState
  deriving (Eq, Show)

data Observability
  = DirectlyObserved
  | PartiallyObserved
  | ProxyObserved
  | Hidden
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data VariableRecord = VariableRecord
  { key :: String
  , role :: VariableRole
  , unitLabel :: String
  , interpretation :: String
  , observability :: Observability
  , status :: ReviewStatus
  } deriving (Eq, Show)

stateRegister :: [VariableRecord]
stateRegister =
  [ VariableRecord
      "storage"
      StateVariable
      "resource units"
      "Current stored resource."
      DirectlyObserved
      Active
  , VariableRecord
      "demand"
      StateVariable
      "resource units per period"
      "Adaptive demand affected by shortage."
      PartiallyObserved
      RequiresReview
  , VariableRecord
      "infrastructure_condition"
      LatentState
      "dimensionless index"
      "Condition of infrastructure supporting storage and delivery."
      ProxyObserved
      RequiresValidation
  , VariableRecord
      "shortage"
      DerivedDiagnostic
      "resource units"
      "Unmet demand after update."
      DirectlyObserved
      RequiresSensitivityTest
  ]

needsReview :: VariableRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed state and representation records:"
  mapM_ print stateRegister

  putStrLn "\nRecords requiring representation review:"
  mapM_ print (filter needsReview stateRegister)
