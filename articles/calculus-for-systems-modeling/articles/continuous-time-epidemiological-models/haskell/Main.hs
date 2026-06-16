module Main where

data EpidemicModelType
  = SIR
  | SEIR
  | SIRS
  | SEIRS
  | AgeStructured
  deriving (Show, Eq)

data ModelUse
  = Teaching
  | ScenarioComparison
  | Preparedness
  | OperationalAnalysis
  | DecisionSupport
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
  , modelType :: EpidemicModelType
  , modelUse :: ModelUse
  , reproductionNumber :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

basicReproductionNumber :: Double -> Double -> Double
basicReproductionNumber beta gamma = beta / gamma

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "beta" 0.32 "per day" "transmission parameter" "Transmission combines contact, infectiousness, behavior, setting, and reporting context."
  , ParameterRecord "gamma" 0.10 "per day" "recovery or removal rate" "Recovery rate should be tied to infectious period assumptions."
  , ParameterRecord "sigma" 0.20 "per day" "progression from exposed to infectious" "Latency and incubation assumptions should be distinguished where needed."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "baseline_sir" SIR Teaching (basicReproductionNumber 0.32 0.10) "Baseline SIR scenario depends on homogeneous mixing assumptions."
  , ScenarioRecord "latent_period_seir" SEIR ScenarioComparison (basicReproductionNumber 0.32 0.10) "Exposed compartment delays infectious growth."
  , ScenarioRecord "reduced_transmission_sir" SIR ScenarioComparison (basicReproductionNumber 0.22 0.10) "Reduced transmission should be tied to a mechanism."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
