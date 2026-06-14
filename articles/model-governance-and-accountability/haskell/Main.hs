{-# OPTIONS_GHC -Wall #-}

module Main where

data RiskTier
  = LowRisk
  | MediumRisk
  | HighRisk
  | CriticalRisk
  deriving (Eq, Show)

data ValidationStatus
  = NotValidated
  | ReviewRequired
  | ValidatedWithLimits
  | RetiredValidation
  deriving (Eq, Show)

data UseLimitStatus
  = NotApproved
  | DraftUseLimit
  | Approved
  | ApprovedWithLimits
  deriving (Eq, Show)

data MonitoringStatus
  = PendingMonitoring
  | ActiveMonitoring
  | IncidentReview
  | RetiredMonitoring
  deriving (Eq, Show)

data ModelGovernanceRecord = ModelGovernanceRecord
  { key :: String
  , modelName :: String
  , modelPurpose :: String
  , riskTier :: RiskTier
  , validationStatus :: ValidationStatus
  , useLimitStatus :: UseLimitStatus
  , monitoringStatus :: MonitoringStatus
  , modelOwner :: String
  , decisionOwner :: String
  } deriving (Eq, Show)

governanceRegister :: [ModelGovernanceRecord]
governanceRegister =
  [ ModelGovernanceRecord
      "infrastructure_risk"
      "Infrastructure risk prioritization model"
      "Planning support for repair prioritization"
      HighRisk
      ValidatedWithLimits
      ApprovedWithLimits
      ActiveMonitoring
      "Infrastructure analytics team"
      "Capital planning office"
  , ModelGovernanceRecord
      "public_health_demand"
      "Public health demand model"
      "Scenario planning for service demand"
      HighRisk
      ReviewRequired
      DraftUseLimit
      PendingMonitoring
      "Health modeling team"
      "Public health operations"
  , ModelGovernanceRecord
      "ai_triage_support"
      "AI-assisted triage support model"
      "Decision support under clinical review"
      CriticalRisk
      ReviewRequired
      NotApproved
      PendingMonitoring
      "Clinical analytics team"
      "Clinical governance board"
  ]

requiresGovernanceReview :: ModelGovernanceRecord -> Bool
requiresGovernanceReview item =
  validationStatus item /= ValidatedWithLimits
  || useLimitStatus item == NotApproved
  || monitoringStatus item /= ActiveMonitoring
  || riskTier item == CriticalRisk

main :: IO ()
main = do
  putStrLn "Typed model governance records:"
  mapM_ print governanceRegister

  putStrLn "\nRecords requiring governance review:"
  mapM_ print (filter requiresGovernanceReview governanceRegister)
