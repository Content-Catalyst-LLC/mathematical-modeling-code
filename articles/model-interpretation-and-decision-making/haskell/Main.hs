{-# OPTIONS_GHC -Wall #-}

module Main where

data InterpretationLayer
  = OutputMeaning
  | UncertaintyMeaning
  | ThresholdReview
  | ValueTradeoff
  | GovernanceReview
  | Communication
  deriving (Eq, Show)

data DecisionRole
  = Evidence
  | ReviewRequired
  | HumanJudgmentRequired
  | GovernanceRequired
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresDecisionContext
  | RequiresGovernance
  | Revise
  deriving (Eq, Show)

data InterpretationRecord = InterpretationRecord
  { key :: String
  , layer :: InterpretationLayer
  , decisionRole :: DecisionRole
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

interpretationRegister :: [InterpretationRecord]
interpretationRegister =
  [ InterpretationRecord
      "output_meaning"
      OutputMeaning
      Evidence
      "What claim is being made from the model output?"
      Active
  , InterpretationRecord
      "uncertainty_meaning"
      UncertaintyMeaning
      ReviewRequired
      "Could uncertainty change the decision?"
      RequiresReview
  , InterpretationRecord
      "threshold_review"
      ThresholdReview
      ReviewRequired
      "Does the result cross or approach the threshold?"
      RequiresDecisionContext
  , InterpretationRecord
      "value_tradeoff"
      ValueTradeoff
      HumanJudgmentRequired
      "Which values are represented or excluded?"
      RequiresDecisionContext
  , InterpretationRecord
      "governance_review"
      GovernanceReview
      GovernanceRequired
      "Who owns the decision and monitoring plan?"
      RequiresGovernance
  ]

needsReview :: InterpretationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed interpretation records:"
  mapM_ print interpretationRegister

  putStrLn "\nInterpretation records requiring review:"
  mapM_ print (filter needsReview interpretationRegister)
