module Main where

data EnergyModelType = ZeroDimensional | OneLayer | TwoLayer | SurfaceBalance | BuildingBalance deriving (Show, Eq)
data ModelUse = Teaching | ScenarioComparison | DesignAnalysis | ClimateInterpretation | DecisionSupport deriving (Show, Eq)

data ParameterRecord = ParameterRecord
  { parameterName :: String
  , parameterValue :: Double
  , parameterUnit :: String
  , interpretation :: String
  , warning :: String
  } deriving (Show, Eq)

data ScenarioRecord = ScenarioRecord
  { scenarioName :: String
  , modelType :: EnergyModelType
  , modelUse :: ModelUse
  , equilibriumTemperature :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

equilibriumTemperatureCalc :: Double -> Double -> Double
equilibriumTemperatureCalc forcing feedback = forcing / feedback

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "F" 3.7 "W m^-2" "external forcing" "Forcing assumptions should be documented as historical, scenario-based, or experimental."
  , ParameterRecord "lambda" 1.2 "W m^-2 K^-1" "feedback parameter" "Feedback terms can hide multiple physical processes."
  , ParameterRecord "C" 10.0 "W yr m^-2 K^-1" "effective heat capacity" "Heat capacity must match the modeled reservoir."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "baseline_one_layer" OneLayer Teaching (equilibriumTemperatureCalc 3.7 1.2) "One-layer model approaches equilibrium according to heat capacity and feedback."
  , ScenarioRecord "stronger_feedback" OneLayer ScenarioComparison (equilibriumTemperatureCalc 3.7 1.8) "Stronger feedback reduces equilibrium response."
  , ScenarioRecord "surface_energy_balance" SurfaceBalance ScenarioComparison 0.0 "Surface energy balance requires radiation, sensible heat, latent heat, ground heat, and storage records."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
