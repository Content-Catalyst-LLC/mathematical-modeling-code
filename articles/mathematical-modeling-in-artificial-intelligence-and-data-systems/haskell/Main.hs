{-# OPTIONS_GHC -Wall #-}

module Main where

data AIModelRole
  = Prediction
  | Classification
  | Ranking
  | Generation
  | Monitoring
  | Governance
  deriving (Eq, Show)

data AIModelFamily
  = SupervisedLearning
  | LearningToRank
  | LanguageModel
  | DriftDetection
  | ModelCardAndAuditRegister
  deriving (Eq, Show)

data DataDomain
  = StructuredRecords
  | RecommendationLogs
  | TextCorpus
  | DeploymentStreams
  | ModelLifecycleRecords
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresBiasReview
  | RequiresPrivacyReview
  | RequiresDeploymentReview
  deriving (Eq, Show)

data AIModelRecord = AIModelRecord
  { key :: String
  , role :: AIModelRole
  , family :: AIModelFamily
  , dataDomain :: DataDomain
  , decisionContext :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

aiRegister :: [AIModelRecord]
aiRegister =
  [ AIModelRecord
      "prediction_model"
      Prediction
      SupervisedLearning
      StructuredRecords
      "Risk scoring with human review"
      Active
  , AIModelRecord
      "ranking_model"
      Ranking
      LearningToRank
      RecommendationLogs
      "Prioritization and visibility"
      RequiresBiasReview
  , AIModelRecord
      "generative_model"
      Generation
      LanguageModel
      TextCorpus
      "Drafting and synthesis support"
      RequiresReview
  , AIModelRecord
      "monitoring_model"
      Monitoring
      DriftDetection
      DeploymentStreams
      "Post-deployment governance"
      RequiresDeploymentReview
  , AIModelRecord
      "governance_model"
      Governance
      ModelCardAndAuditRegister
      ModelLifecycleRecords
      "Accountability and review"
      RequiresPrivacyReview
  ]

needsReview :: AIModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed AI model records:"
  mapM_ print aiRegister

  putStrLn "\nAI model records requiring review:"
  mapM_ print (filter needsReview aiRegister)
