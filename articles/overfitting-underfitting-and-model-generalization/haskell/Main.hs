{-# OPTIONS_GHC -Wall #-}

module Main where

data GeneralizationLayer
  = EvidenceSplit
  | OverfitDiagnostic
  | UnderfitDiagnostic
  | ComplexityReview
  | DistributionShift
  | DecisionThreshold
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresMonitoring
  | Revise
  deriving (Eq, Show)

data GeneralizationRecord = GeneralizationRecord
  { key :: String
  , layer :: GeneralizationLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

generalizationRegister :: [GeneralizationRecord]
generalizationRegister =
  [ GeneralizationRecord
      "training_validation_split"
      EvidenceSplit
      "Separates fitting evidence from generalization evidence."
      "Evidence separation."
      Active
  , GeneralizationRecord
      "overfit_gap"
      OverfitDiagnostic
      "Compares validation error against training error."
      "Noise memorization."
      RequiresReview
  , GeneralizationRecord
      "underfit_check"
      UnderfitDiagnostic
      "Flags high training and validation error."
      "Missing structure."
      RequiresReview
  , GeneralizationRecord
      "complexity_review"
      ComplexityReview
      "Reviews whether flexibility is justified."
      "Appropriate complexity."
      RequiresReview
  , GeneralizationRecord
      "distribution_shift"
      DistributionShift
      "Reviews whether use conditions differ from fitting conditions."
      "Transfer limits."
      RequiresMonitoring
  , GeneralizationRecord
      "decision_threshold"
      DecisionThreshold
      "Connects generalization evidence to decision consequences."
      "Fitness for decision use."
      RequiresValidation
  ]

needsReview :: GeneralizationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed generalization records:"
  mapM_ print generalizationRegister

  putStrLn "\nGeneralization records requiring review:"
  mapM_ print (filter needsReview generalizationRegister)
