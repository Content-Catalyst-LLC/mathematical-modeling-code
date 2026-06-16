module Main where

data PurposeType
  = Teaching
  | Exploratory
  | Mechanistic
  | Predictive
  | Optimization
  | DecisionSupport
  deriving (Show, Eq)

data AssumptionType
  = Mathematical
  | Empirical
  | Computational
  | Boundary
  | MechanisticAssumption
  | Normative
  deriving (Show, Eq)

data GovernanceStatus
  = Active
  | Review
  | Revise
  | Archive
  deriving (Show, Eq)

data PurposeRecord = PurposeRecord
  { modelName :: String
  , purposeType :: PurposeType
  , supportedUse :: String
  , unsupportedUse :: String
  , purposeWarning :: String
  } deriving (Show, Eq)

data AssumptionRecord = AssumptionRecord
  { assumptionName :: String
  , assumptionType :: AssumptionType
  , assumptionDescription :: String
  , evidenceStatus :: String
  , riskIfHidden :: String
  } deriving (Show, Eq)

data ClaimBoundary = ClaimBoundary
  { claimType :: String
  , permittedClaim :: String
  , prohibitedClaim :: String
  , requiredEvidence :: String
  , governanceStatus :: GovernanceStatus
  } deriving (Show, Eq)

purposeRecords :: [PurposeRecord]
purposeRecords =
  [ PurposeRecord "synthetic_logistic_growth" Teaching "illustrates growth, saturation, and carrying capacity" "empirical forecast for a real population" "Synthetic teaching models should not be communicated as empirical evidence."
  , PurposeRecord "scenario_sweep" Exploratory "compares behavior across plausible parameter scenarios" "single-point prediction" "Scenario outputs should not be confused with forecasts."
  ]

assumptionRecords :: [AssumptionRecord]
assumptionRecords =
  [ AssumptionRecord "continuous_growth" Mathematical "state changes continuously over modeled time" "teaching assumption" "smooth model may hide shocks, thresholds, or discrete events"
  , AssumptionRecord "objective_function_weights" Normative "optimization weights reflect a chosen priority structure" "requires stakeholder and governance review" "value judgments are hidden inside mathematics"
  ]

claimBoundaries :: [ClaimBoundary]
claimBoundaries =
  [ ClaimBoundary "descriptive" "the model summarizes a specified structure or dataset" "the model proves a mechanism" "definition of variables, data source, and scope" Active
  , ClaimBoundary "predictive" "the model forecasts within validated domain and time horizon" "the model predicts outside validation scope" "validation data, uncertainty, and robustness analysis" Review
  ]

main :: IO ()
main = do
  putStrLn "Purpose records:"
  mapM_ print purposeRecords
  putStrLn ""
  putStrLn "Assumption records:"
  mapM_ print assumptionRecords
  putStrLn ""
  putStrLn "Claim boundaries:"
  mapM_ print claimBoundaries
