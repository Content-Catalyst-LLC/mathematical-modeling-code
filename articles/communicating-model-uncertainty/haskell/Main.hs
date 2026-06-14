{-# OPTIONS_GHC -Wall #-}

module Main where

data CommunicationLayer
  = CentralResult
  | UncertaintyRange
  | ScenarioMessage
  | ThresholdRisk
  | StructuralLimit
  | UseLimit
  | Governance
  deriving (Eq, Show)

data Audience
  = TechnicalReviewer
  | DecisionMaker
  | PublicAudience
  | DomainExpert
  | FutureUser
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresPlainLanguage
  | RequiresDecisionContext
  | Revise
  deriving (Eq, Show)

data CommunicationRecord = CommunicationRecord
  { key :: String
  , layer :: CommunicationLayer
  , audience :: Audience
  , messageGoal :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

communicationRegister :: [CommunicationRecord]
communicationRegister =
  [ CommunicationRecord
      "central_result"
      CentralResult
      DecisionMaker
      "State the baseline result without overstating certainty."
      Active
  , CommunicationRecord
      "uncertainty_range"
      UncertaintyRange
      PublicAudience
      "Explain plausible output variation in plain language."
      RequiresPlainLanguage
  , CommunicationRecord
      "scenario_message"
      ScenarioMessage
      PublicAudience
      "Clarify that scenarios are plausible futures, not guaranteed forecasts."
      RequiresPlainLanguage
  , CommunicationRecord
      "threshold_risk"
      ThresholdRisk
      DecisionMaker
      "Explain whether uncertainty could reverse action."
      RequiresDecisionContext
  , CommunicationRecord
      "structural_limit"
      StructuralLimit
      TechnicalReviewer
      "State model-form limitations."
      RequiresReview
  , CommunicationRecord
      "use_limit"
      UseLimit
      FutureUser
      "Prevent use beyond validation domain."
      RequiresReview
  ]

needsReview :: CommunicationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed communication records:"
  mapM_ print communicationRegister

  putStrLn "\nCommunication records requiring review:"
  mapM_ print (filter needsReview communicationRegister)
