module Main where

data UrbanModelType = LinkFlow | QueueModel | NetworkEquilibrium | AccessibilityModel | LandUseTransportModel deriving (Show, Eq)
data ModelUse = Teaching | Operations | ScenarioComparison | InfrastructurePlanning | DecisionSupport deriving (Show, Eq)

data ParameterRecord = ParameterRecord
  { parameterName :: String, parameterValue :: Double, parameterUnit :: String, interpretation :: String, warning :: String
  } deriving (Show, Eq)

data ScenarioRecord = ScenarioRecord
  { scenarioName :: String, modelType :: UrbanModelType, modelUse :: ModelUse, demand :: Double, capacity :: Double, scenarioWarning :: String
  } deriving (Show, Eq)

trafficFlow :: Double -> Double -> Double -> Double
trafficFlow density freeFlowSpeed jamDensity = max 0 (freeFlowSpeed * density * (1 - density / jamDensity))

queueStep :: Double -> Double -> Double -> Double -> Double
queueStep queue arrivalRate serviceRate dt = max 0 (queue + (arrivalRate - serviceRate) * dt)

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "q" 1800 "vehicles per hour" "traffic flow" "Flow unit and mode must be documented."
  , ParameterRecord "C" 2000 "vehicles per hour" "capacity" "Capacity depends on design, signals, incidents, weather, and curb use."
  , ParameterRecord "theta" 0.08 "per minute" "accessibility decay" "Accessibility assumptions shape equity interpretation."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "below_capacity_corridor" QueueModel Teaching 1800 2000 "Demand below capacity produces limited queue accumulation."
  , ScenarioRecord "over_capacity_bottleneck" QueueModel ScenarioComparison 2300 2000 "Demand above capacity produces persistent queue and delay."
  , ScenarioRecord "capacity_expansion_with_induced_demand" LandUseTransportModel InfrastructurePlanning 2500 2600 "Capacity expansion should be reviewed with induced demand and land-use feedback."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
  putStrLn ""
  putStrLn ("Example flow at density 35: " ++ show (trafficFlow 35 60 140))
  putStrLn ("Example queue step: " ++ show (queueStep 0 2300 2000 0.01))
