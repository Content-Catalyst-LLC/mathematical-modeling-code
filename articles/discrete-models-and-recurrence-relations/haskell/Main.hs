{-# OPTIONS_GHC -Wall #-}

module Main where

data RecurrenceComponent
  = StateVariable
  | UpdateRule
  | InitialCondition
  | BoundaryRule
  | Parameter
  | OutputDiagnostic
  | StepDefinition
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data RecurrenceRecord = RecurrenceRecord
  { key :: String
  , component :: RecurrenceComponent
  , expression :: String
  , interpretation :: String
  , domainOrStep :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

recurrenceRegister :: [RecurrenceRecord]
recurrenceRegister =
  [ RecurrenceRecord
      "storage"
      StateVariable
      "S_t"
      "Current resource storage at period t."
      "0 <= S_t <= K"
      Active
  , RecurrenceRecord
      "storage_update"
      UpdateRule
      "S_{t+1} = min(K, max(0, S_t + I_t - D_t - lambda*S_t))"
      "Storage updates through inflow, demand, and proportional loss."
      "one period"
      RequiresReview
  , RecurrenceRecord
      "initial_storage"
      InitialCondition
      "S_0"
      "Starting storage."
      "0 <= S_0 <= K"
      RequiresValidation
  , RecurrenceRecord
      "shortage"
      OutputDiagnostic
      "Q_t = max(0, -raw_next_storage)"
      "Unmet demand before boundary clipping."
      "reported each period"
      RequiresSensitivityTest
  ]

needsReview :: RecurrenceRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed recurrence records:"
  mapM_ print recurrenceRegister

  putStrLn "\nRecurrence records requiring review:"
  mapM_ print (filter needsReview recurrenceRegister)
