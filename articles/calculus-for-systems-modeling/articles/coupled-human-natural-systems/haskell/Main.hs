module Main where

data CoupledModelType = ResourceGovernanceFeedback | CityWatershed | EnergyClimate | AgricultureSoil | CoastalRisk deriving (Show, Eq)
data ModelUse = Teaching | ScenarioComparison | CommunityPlanning | PolicyAnalysis | DecisionSupport deriving (Show, Eq)

data ParameterRecord = ParameterRecord
  { parameterName :: String, parameterValue :: Double, parameterUnit :: String, interpretation :: String, warning :: String
  } deriving (Show, Eq)

data ScenarioRecord = ScenarioRecord
  { scenarioName :: String, modelType :: CoupledModelType, modelUse :: ModelUse, humanPressure :: Double, naturalStock :: Double, scenarioWarning :: String
  } deriving (Show, Eq)

regeneration :: Double -> Double -> Double -> Double
regeneration stock growthRate carryingCapacity = growthRate * stock * (1 - stock / carryingCapacity)

extraction :: Double -> Double -> Double -> Double
extraction efficiency effort stock = efficiency * effort * stock

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "r" 0.08 "per year" "natural regeneration rate" "Regeneration may vary with habitat, climate, age structure, and system state."
  , ParameterRecord "K" 100 "stock units" "carrying capacity" "Carrying capacity may change with climate, land use, pollution, or habitat loss."
  , ParameterRecord "G" 0.60 "index" "governance strength" "Governance quality includes legitimacy, enforcement, resources, and trust."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "baseline_coupled_resource" ResourceGovernanceFeedback Teaching 12 80 "Coupled outcome depends on regeneration, extraction, stress, governance, adaptation, and vulnerability."
  , ScenarioRecord "city_watershed" CityWatershed ScenarioComparison 14 70 "Water security depends on demand, recharge, infrastructure, pricing, governance, and drought."
  , ScenarioRecord "energy_climate" EnergyClimate PolicyAnalysis 20 60 "Energy-climate scenarios require emissions, uptake, warming, impacts, adaptation, and justice review."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
  putStrLn ""
  putStrLn ("Example regeneration: " ++ show (regeneration 80 0.08 100))
  putStrLn ("Example extraction: " ++ show (extraction 0.003 12 80))
