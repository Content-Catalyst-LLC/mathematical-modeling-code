module Main where

data ResourceType
  = Renewable
  | Nonrenewable
  | CommonPool
  | ManagedStock
  deriving (Show, Eq)

data RegenerationModel
  = NoRegeneration
  | ConstantRenewal
  | LogisticRenewal
  | ThresholdRenewal
  | EnvironmentDependentRenewal
  deriving (Show, Eq)

data ParameterRecord = ParameterRecord
  { parameterName :: String
  , parameterValue :: Double
  , parameterUnit :: String
  , interpretation :: String
  , warning :: String
  } deriving (Show, Eq)

data ScenarioRecord = ScenarioRecord
  { scenarioName :: String
  , resourceType :: ResourceType
  , regenerationModel :: RegenerationModel
  , finalStock :: Double
  , cumulativeExtraction :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

maximumSustainableYield :: Double -> Double -> Double
maximumSustainableYield r k = r * k / 4

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "R0" 600.0 "stock units" "initial resource stock" "Stock definition and measurement boundary must be documented."
  , ParameterRecord "r" 0.18 "per year" "regeneration rate" "Regeneration may be seasonal, climate-dependent, or threshold-dependent."
  , ParameterRecord "K" 1000.0 "stock units" "carrying capacity" "Capacity can change with degradation, habitat, climate, or management."
  , ParameterRecord "MSY" (maximumSustainableYield 0.18 1000.0) "stock units per year" "maximum sustainable yield in ideal logistic model" "MSY is not a safe target under uncertainty by default."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "renewable_precautionary_harvest" Renewable LogisticRenewal 600.0 2800.0 "Harvest below idealized maximum yield allows persistence under baseline assumptions."
  , ScenarioRecord "threshold_recovery_risk" Renewable ThresholdRenewal 200.0 3000.0 "Threshold-dependent recovery can slow or fail under depletion."
  , ScenarioRecord "nonrenewable_drawdown" Nonrenewable NoRegeneration 0.0 600.0 "Nonrenewable resource declines through extraction without regeneration."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
