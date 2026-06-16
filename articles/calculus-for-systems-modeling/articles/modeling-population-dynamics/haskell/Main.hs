module Main where

data ModelType
  = Exponential
  | Logistic
  deriving (Show, Eq)

data SourceStatus
  = SyntheticTeaching
  | Measured
  | Estimated
  | Calibrated
  | Scenario
  deriving (Show, Eq)

data ParameterRecord = ParameterRecord
  { parameterName :: String
  , parameterValue :: Double
  , parameterUnit :: String
  , sourceStatus :: SourceStatus
  , interpretation :: String
  , warning :: String
  } deriving (Show, Eq)

data ScenarioRecord = ScenarioRecord
  { scenarioName :: String
  , modelType :: ModelType
  , initialPopulation :: Double
  , growthRate :: Double
  , carryingCapacity :: Maybe Double
  , finalTime :: Double
  , finalPopulation :: Double
  } deriving (Show, Eq)

exponentialPopulation :: Double -> Double -> Double -> Double
exponentialPopulation n0 r t = n0 * exp (r * t)

logisticPopulation :: Double -> Double -> Double -> Double -> Double
logisticPopulation n0 r k t =
  k / (1 + ((k - n0) / n0) * exp (-r * t))

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "N0" 100.0 "individuals" SyntheticTeaching "initial population" "Initial values should be measured or estimated with uncertainty in empirical use."
  , ParameterRecord "r" 0.08 "per year" SyntheticTeaching "intrinsic growth rate" "Growth rates may vary over time and across conditions."
  , ParameterRecord "K" 1000.0 "individuals" SyntheticTeaching "carrying capacity" "Carrying capacity is assumption-bearing and may change over time."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  let n0 = 100.0
      r = 0.08
      k = 1000.0
      t = 40.0
  in
    [ ScenarioRecord "exponential_baseline" Exponential n0 r Nothing t (exponentialPopulation n0 r t)
    , ScenarioRecord "logistic_capacity_limited" Logistic n0 r (Just k) t (logisticPopulation n0 r k t)
    ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
