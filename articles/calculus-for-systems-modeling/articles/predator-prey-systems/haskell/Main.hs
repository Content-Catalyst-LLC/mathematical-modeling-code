module Main where

data InteractionModel
  = LotkaVolterra
  | LogisticPrey
  | TypeIIResponse
  | Harvesting
  | Stochastic
  | Spatial
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
  , interactionModel :: InteractionModel
  , finalTime :: Double
  , finalPrey :: Double
  , finalPredator :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "alpha" 0.6 "per year" "prey intrinsic growth rate" "Prey growth may be resource-limited rather than exponential."
  , ParameterRecord "beta" 0.02 "encounter coefficient" "predation interaction coefficient" "Mass-action encounters may overstate interaction in spatial systems."
  , ParameterRecord "gamma" 0.5 "per year" "predator mortality rate" "Mortality may vary by age, season, or environment."
  , ParameterRecord "delta" 0.01 "conversion coefficient" "conversion from prey encounters to predator growth" "Conversion efficiency should not be treated as mechanism without evidence."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "classic_lotka_volterra" LotkaVolterra 80.0 40.0 9.0 "Baseline mass-action model."
  , ScenarioRecord "logistic_prey_limit" LogisticPrey 80.0 40.0 9.0 "Prey carrying capacity included."
  , ScenarioRecord "type_ii_functional_response" TypeIIResponse 80.0 40.0 9.0 "Predation saturates through handling time."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
