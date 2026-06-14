{-# OPTIONS_GHC -Wall #-}

module Main where

data PolicyDomain
  = PublicSystems
  | PublicPlanning
  | ResourceAllocation
  | PublicAccountability
  | InstitutionalGovernance
  deriving (Eq, Show)

data PolicyModelRole
  = ProblemFraming
  | Forecasting
  | OptionComparison
  | DistributionalReview
  | ModelGovernance
  | PublicCommunication
  deriving (Eq, Show)

data PolicyModelFamily
  = SystemsMap
  | ScenarioForecast
  | ConstrainedDecisionModel
  | EquityDiagnostic
  | ReviewRegister
  | ImpactEvaluation
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresEquityReview
  | RequiresGovernanceReview
  | Revise
  deriving (Eq, Show)

data PolicyModelRecord = PolicyModelRecord
  { key :: String
  , domain :: PolicyDomain
  , role :: PolicyModelRole
  , family :: PolicyModelFamily
  , publicQuestion :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

policyRegister :: [PolicyModelRecord]
policyRegister =
  [ PolicyModelRecord
      "problem_model"
      PublicSystems
      ProblemFraming
      SystemsMap
      "What drivers and boundaries define the public problem?"
      Active
  , PolicyModelRecord
      "forecast_model"
      PublicPlanning
      Forecasting
      ScenarioForecast
      "What demand or risk is plausible under future conditions?"
      RequiresReview
  , PolicyModelRecord
      "allocation_model"
      ResourceAllocation
      OptionComparison
      ConstrainedDecisionModel
      "Which option balances benefit, cost, feasibility, and equity?"
      RequiresReview
  , PolicyModelRecord
      "equity_model"
      PublicAccountability
      DistributionalReview
      EquityDiagnostic
      "How are benefits and burdens distributed across groups or places?"
      RequiresEquityReview
  , PolicyModelRecord
      "governance_model"
      InstitutionalGovernance
      ModelGovernance
      ReviewRegister
      "Who owns the model, decision, update process, and challenge pathway?"
      RequiresGovernanceReview
  ]

needsReview :: PolicyModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed policy model records:"
  mapM_ print policyRegister

  putStrLn "\nPolicy model records requiring review:"
  mapM_ print (filter needsReview policyRegister)
