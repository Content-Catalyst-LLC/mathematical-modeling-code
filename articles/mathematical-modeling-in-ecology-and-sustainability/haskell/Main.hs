{-# OPTIONS_GHC -Wall #-}

module Main where

data EcologyDomain
  = RenewableResourceManagement
  | EcosystemResilience
  | ClimateAdaptation
  | ConservationPlanning
  | SustainabilityGovernance
  deriving (Eq, Show)

data EcologyModelRole
  = StockFlowReview
  | ThresholdReview
  | ScenarioAnalysis
  | NetworkReview
  | AdaptiveManagement
  deriving (Eq, Show)

data EcologyModelFamily
  = DynamicResourceModel
  | ResilienceMarginModel
  | StressTestModel
  | BiodiversityDependencyModel
  | MonitoringTriggerModel
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresFieldEvidence
  | RequiresGovernanceReview
  | Revise
  deriving (Eq, Show)

data EcologyModelRecord = EcologyModelRecord
  { key :: String
  , domain :: EcologyDomain
  , role :: EcologyModelRole
  , family :: EcologyModelFamily
  , sustainabilityQuestion :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

ecologyRegister :: [EcologyModelRecord]
ecologyRegister =
  [ EcologyModelRecord
      "resource_stock_model"
      RenewableResourceManagement
      StockFlowReview
      DynamicResourceModel
      "Does extraction remain within regenerative capacity?"
      Active
  , EcologyModelRecord
      "resilience_model"
      EcosystemResilience
      ThresholdReview
      ResilienceMarginModel
      "How close is the system to a minimum ecological threshold?"
      RequiresReview
  , EcologyModelRecord
      "climate_stress_model"
      ClimateAdaptation
      ScenarioAnalysis
      StressTestModel
      "How does climate stress change long-term stock viability?"
      RequiresReview
  , EcologyModelRecord
      "biodiversity_model"
      ConservationPlanning
      NetworkReview
      BiodiversityDependencyModel
      "Which ecological interactions and dependencies need review?"
      RequiresFieldEvidence
  , EcologyModelRecord
      "governance_model"
      SustainabilityGovernance
      AdaptiveManagement
      MonitoringTriggerModel
      "When should management action change as evidence updates?"
      RequiresGovernanceReview
  ]

needsReview :: EcologyModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed ecology and sustainability model records:"
  mapM_ print ecologyRegister

  putStrLn "\nEcology records requiring review:"
  mapM_ print (filter needsReview ecologyRegister)
