{-# OPTIONS_GHC -Wall #-}

module Main where

data DiagnosticLayer
  = Bias
  | DecisionThreshold
  | SubgroupError
  | TailError
  | ModelForm
  | UncertaintyReview
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresUncertaintyCheck
  | Revise
  deriving (Eq, Show)

data DiagnosticRecord = DiagnosticRecord
  { key :: String
  , layer :: DiagnosticLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

diagnosticRegister :: [DiagnosticRecord]
diagnosticRegister =
  [ DiagnosticRecord
      "residual_bias"
      Bias
      "Reviews directional error across observations."
      "Systematic overprediction or underprediction."
      Active
  , DiagnosticRecord
      "threshold_error"
      DecisionThreshold
      "Reviews residuals near action thresholds."
      "Decision-changing error."
      RequiresValidation
  , DiagnosticRecord
      "group_error"
      SubgroupError
      "Compares error across diagnostic groups."
      "Uneven model reliability."
      RequiresReview
  , DiagnosticRecord
      "outlier_review"
      TailError
      "Flags unusually large residuals."
      "Tail behavior and extreme cases."
      RequiresReview
  , DiagnosticRecord
      "structural_error"
      ModelForm
      "Reviews whether residual patterns suggest missing structure."
      "Model-form limitations."
      RequiresReview
  , DiagnosticRecord
      "uncertainty_review"
      UncertaintyReview
      "Connects diagnostic evidence to uncertainty communication."
      "Uncertainty adequacy."
      RequiresUncertaintyCheck
  ]

needsReview :: DiagnosticRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed diagnostic records:"
  mapM_ print diagnosticRegister

  putStrLn "\nDiagnostic records requiring review:"
  mapM_ print (filter needsReview diagnosticRegister)
