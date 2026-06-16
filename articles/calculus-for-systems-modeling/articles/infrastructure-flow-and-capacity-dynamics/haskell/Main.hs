module Main where

data InfrastructureType
  = Transport
  | Water
  | Energy
  | Health
  | Digital
  | SupplyChain
  deriving (Show, Eq)

data CapacityStatus
  = SpareCapacity
  | NearCapacity
  | OverCapacity
  | Bottlenecked
  | DecayedCapacity
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
  , infrastructureType :: InfrastructureType
  , capacityStatus :: CapacityStatus
  , utilizationRatio :: Double
  , finalQueue :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

utilization :: Double -> Double -> Double
utilization arrival capacity = arrival / capacity

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "lambda" 95.0 "units per hour" "arrival or demand rate" "Peak and average demand should be documented separately."
  , ParameterRecord "mu" 100.0 "units per hour" "service capacity" "Nominal capacity may differ from effective capacity."
  , ParameterRecord "buffer_capacity" 300.0 "units" "maximum buffer or storage capacity" "Buffers can saturate under sustained imbalance."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "baseline_spare_capacity" Transport SpareCapacity (utilization 75.0 100.0) 0.0 "Spare capacity keeps queues low."
  , ScenarioRecord "near_capacity_operation" Transport NearCapacity (utilization 95.0 100.0) 0.0 "Near-capacity operation creates high delay sensitivity."
  , ScenarioRecord "over_capacity_backlog" Transport OverCapacity (utilization 115.0 100.0) 360.0 "Arrival rate above capacity causes backlog accumulation."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
