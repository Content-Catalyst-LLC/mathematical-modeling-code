{-# OPTIONS_GHC -Wall #-}

module Main where

data ValidationLayer
  = ConceptualValidity
  | Verification
  | EvidenceQuality
  | Diagnostics
  | Generalization
  | UncertaintyReview
  | DecisionSupport
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresUncertaintyCheck
  | Revise
  deriving (Eq, Show)

data ValidationRecord = ValidationRecord
  { key :: String
  , layer :: ValidationLayer
  , modelingRole :: String
  , assessmentFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

validationRegister :: [ValidationRecord]
validationRegister =
  [ ValidationRecord
      "conceptual_validity"
      ConceptualValidity
      "Reviews structure, assumptions, boundaries, and purpose."
      "Model-system fit."
      RequiresReview
  , ValidationRecord
      "implementation_verification"
      Verification
      "Checks that code implements the model specification."
      "Implementation correctness."
      Active
  , ValidationRecord
      "data_validation"
      EvidenceQuality
      "Reviews observations, units, provenance, and alignment."
      "Evidence reliability."
      RequiresReview
  , ValidationRecord
      "residual_diagnostics"
      Diagnostics
      "Examines residuals, bias, and error patterns."
      "Systematic model error."
      Active
  , ValidationRecord
      "uncertainty_review"
      UncertaintyReview
      "Reviews sensitivity, robustness, and uncertainty."
      "Decision-changing uncertainty."
      RequiresUncertaintyCheck
  , ValidationRecord
      "fitness_for_purpose"
      DecisionSupport
      "Assesses adequacy for intended use."
      "Purpose-specific credibility."
      RequiresValidation
  ]

needsReview :: ValidationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed validation records:"
  mapM_ print validationRegister

  putStrLn "\nValidation records requiring review:"
  mapM_ print (filter needsReview validationRegister)
