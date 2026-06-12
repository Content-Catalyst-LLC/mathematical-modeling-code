{-# OPTIONS_GHC -Wall #-}

module Main where

data SelectionLayer
  = Alternatives
  | Generalization
  | Parsimony
  | Communication
  | Uncertainty
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

data SelectionRecord = SelectionRecord
  { key :: String
  , layer :: SelectionLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

selectionRegister :: [SelectionRecord]
selectionRegister =
  [ SelectionRecord
      "candidate_set"
      Alternatives
      "Defines the models being compared."
      "Plausible baselines and alternatives."
      RequiresReview
  , SelectionRecord
      "validation_error"
      Generalization
      "Compares performance beyond fitting data."
      "Generalization."
      Active
  , SelectionRecord
      "complexity_penalty"
      Parsimony
      "Penalizes unnecessary complexity."
      "Complexity justification."
      RequiresReview
  , SelectionRecord
      "interpretability"
      Communication
      "Assesses whether model behavior can be explained."
      "User understanding."
      RequiresReview
  , SelectionRecord
      "robustness"
      Uncertainty
      "Reviews stability under assumptions and stress."
      "Uncertainty-aware selection."
      RequiresUncertaintyCheck
  , SelectionRecord
      "decision_relevance"
      DecisionSupport
      "Links model selection to intended use."
      "Fitness for purpose."
      RequiresValidation
  ]

needsReview :: SelectionRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed model selection records:"
  mapM_ print selectionRegister

  putStrLn "\nSelection records requiring review:"
  mapM_ print (filter needsReview selectionRegister)
