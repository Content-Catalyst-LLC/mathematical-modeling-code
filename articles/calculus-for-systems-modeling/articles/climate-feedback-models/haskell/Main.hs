module Main where

data SignConvention
  = RestoringPositive
  | ClimateFeedbackSign
  deriving (Show, Eq)

data ClimateModelType
  = OneBoxEnergyBalance
  | TwoBoxEnergyBalance
  | CarbonCycleFeedback
  | FeedbackSweep
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
  , modelType :: ClimateModelType
  , finalTime :: Double
  , finalTemperature :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

oneBoxTemperature :: Double -> Double -> Double -> Double -> Double
oneBoxTemperature forcing feedback heatCapacity time =
  let equilibrium = forcing / feedback
  in equilibrium * (1 - exp (-(feedback / heatCapacity) * time))

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "F" 3.7 "W m^-2" "forcing from doubled carbon dioxide in a simplified scenario" "Forcing depends on the forcing agent and scenario."
  , ParameterRecord "lambda" 1.2 "W m^-2 K^-1" "net restoring feedback strength using restoring-positive convention" "Sign convention must be documented."
  , ParameterRecord "C" 8.0 "W yr m^-2 K^-1" "effective surface heat capacity" "Heat capacity summarizes ocean and atmosphere response."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "one_box_baseline" OneBoxEnergyBalance 80.0 (oneBoxTemperature 3.7 1.2 8.0 80.0) "Baseline forcing-feedback adjustment."
  , ScenarioRecord "weak_feedback_high_sensitivity" FeedbackSweep 80.0 (oneBoxTemperature 3.7 0.9 8.0 80.0) "Weaker restoring feedback produces larger response."
  , ScenarioRecord "strong_feedback_low_sensitivity" FeedbackSweep 80.0 (oneBoxTemperature 3.7 1.6 8.0 80.0) "Stronger restoring feedback produces smaller response."
  ]

main :: IO ()
main = do
  putStrLn "Sign convention:"
  print RestoringPositive
  putStrLn ""
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
