module Main where
data ModelType = Exponential | Logistic | AlleeEffect | Harvesting | Stochastic | Structured | Spatial deriving (Show, Eq)
data SourceStatus = SyntheticTeaching | Measured | Estimated | Calibrated | Scenario deriving (Show, Eq)
data ParameterRecord = ParameterRecord { parameterName :: String, parameterValue :: Double, parameterUnit :: String, sourceStatus :: SourceStatus, interpretation :: String, warning :: String } deriving (Show, Eq)
data ScenarioRecord = ScenarioRecord { scenarioName :: String, modelType :: ModelType, finalTime :: Double, finalPopulation :: Double, scenarioWarning :: String } deriving (Show, Eq)
exponentialPopulation n0 r t = n0 * exp (r * t)
logisticPopulation n0 r k t = k / (1 + ((k - n0) / n0) * exp (-r * t))
parameterRecords = [ParameterRecord "N0" 100 "individuals" SyntheticTeaching "initial population" "Initial values should include uncertainty.", ParameterRecord "r" 0.08 "per year" SyntheticTeaching "intrinsic growth rate" "Growth rates may vary.", ParameterRecord "K" 1000 "individuals" SyntheticTeaching "carrying capacity" "K is assumption-bearing.", ParameterRecord "A" 75 "individuals" SyntheticTeaching "Allee threshold" "Thresholds may be hard to identify."]
scenarioRecords = let n0=100; r=0.08; k=1000; t=40 in [ScenarioRecord "exponential_baseline" Exponential t (exponentialPopulation n0 r t) "unconstrained baseline", ScenarioRecord "logistic_capacity_limited" Logistic t (logisticPopulation n0 r k t) "capacity-limited assumption"]
main = do
  putStrLn "Parameter records:"; mapM_ print parameterRecords
  putStrLn ""; putStrLn "Scenario records:"; mapM_ print scenarioRecords
