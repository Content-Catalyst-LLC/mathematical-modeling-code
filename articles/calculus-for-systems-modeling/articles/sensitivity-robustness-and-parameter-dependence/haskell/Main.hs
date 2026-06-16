module Main where

data RobustnessStatus
  = Stable
  | Sensitive
  | Fragile
  | Untested
  deriving (Show, Eq)

data ParameterRecord = ParameterRecord
  { parameterName :: String
  , baselineValue :: Double
  , lowerBound :: Double
  , upperBound :: Double
  , unitLabel :: String
  , sourceNote :: String
  } deriving (Show, Eq)

data SensitivityRecord = SensitivityRecord
  { sensitivityParameter :: String
  , baselineOutput :: Double
  , lowOutput :: Double
  , highOutput :: Double
  , sensitivityScore :: Double
  , elasticityEstimate :: Double
  , robustnessStatus :: RobustnessStatus
  , warningNote :: String
  } deriving (Show, Eq)

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "growth_rate" 0.35 0.20 0.50 "per time unit" "synthetic teaching range"
  , ParameterRecord "carrying_capacity" 100.0 75.0 125.0 "state units" "synthetic teaching range"
  , ParameterRecord "initial_stock" 10.0 5.0 20.0 "state units" "synthetic teaching range"
  ]

sensitivityRecords :: [SensitivityRecord]
sensitivityRecords =
  [ SensitivityRecord "growth_rate" 99.2 85.8 99.7 46.3 0.163 Sensitive "Conclusion may depend on growth-rate assumptions."
  , SensitivityRecord "carrying_capacity" 99.2 74.5 124.0 0.99 0.998 Sensitive "Capacity scale strongly affects final stock interpretation."
  , SensitivityRecord "initial_stock" 99.2 98.3 99.6 0.087 0.009 Stable "Output variation is limited across this synthetic range."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Sensitivity records:"
  mapM_ print sensitivityRecords
