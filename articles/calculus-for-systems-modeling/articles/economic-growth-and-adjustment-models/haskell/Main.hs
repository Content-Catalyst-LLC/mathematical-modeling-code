module Main where

data GrowthModelType
  = ExponentialGrowth
  | LogisticConstraint
  | CapitalAccumulation
  | TargetAdjustment
  | ShockAdjustment
  deriving (Show, Eq)

data OutputMeasure
  = OutputIndex
  | RealGDP
  | PerCapitaOutput
  | SectorOutput
  | WelfareProxy
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
  , growthModelType :: GrowthModelType
  , outputMeasure :: OutputMeasure
  , finalOutput :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

exponentialOutput :: Double -> Double -> Double -> Double
exponentialOutput y0 g t = y0 * exp (g * t)

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "Y0" 100.0 "index" "initial output index" "Output measure and price basis must be documented."
  , ParameterRecord "g" 0.025 "per year" "baseline output growth rate" "Growth-rate assumptions compound strongly over time."
  , ParameterRecord "delta" 0.05 "per year" "depreciation rate" "Depreciation should include maintenance and obsolescence assumptions."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "constant_growth_projection" ExponentialGrowth OutputIndex (exponentialOutput 100.0 0.025 40.0) "Constant proportional growth compounds over time."
  , ScenarioRecord "capacity_constrained_growth" LogisticConstraint OutputIndex 225.0 "Growth slows near a defined capacity or saturation limit."
  , ScenarioRecord "capital_accumulation_case" CapitalAccumulation OutputIndex 180.0 "Investment and depreciation shape long-run output capacity."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
