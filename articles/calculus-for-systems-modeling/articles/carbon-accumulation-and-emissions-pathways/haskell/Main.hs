module Main where

data PathwayType
  = ConstantEmissions
  | LinearDecline
  | ExponentialDecline
  | Overshoot
  | NetZero
  deriving (Show, Eq)

data AccountingBoundary
  = GlobalCO2
  | NationalCO2
  | SectorCO2
  | NetEmissions
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
  , pathwayType :: PathwayType
  , accountingBoundary :: AccountingBoundary
  , cumulativeEmissions :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

linearDecline :: Double -> Int -> [Double]
linearDecline e0 years =
  [ max 0 (e0 * (1 - fromIntegral y / fromIntegral years)) | y <- [0..years] ]

exponentialDecline :: Double -> Double -> Int -> [Double]
exponentialDecline e0 rate years =
  [ e0 * exp (-rate * fromIntegral y) | y <- [0..years] ]

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "E0" 40.0 "GtCO2 per year" "initial annual emissions" "Accounting boundary must be documented."
  , ParameterRecord "budget" 500.0 "GtCO2" "illustrative remaining carbon budget" "Carbon budgets depend on temperature goal, probability framing, and uncertainty."
  , ParameterRecord "removal_rate" 5.0 "GtCO2 per year" "illustrative negative-emissions rate" "Removal feasibility, permanence, scale, and governance must be reviewed."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  let constant = replicate 31 40.0
      linear = linearDecline 40.0 30
      exponential = exponentialDecline 40.0 0.08 30
  in
    [ ScenarioRecord "constant_emissions" ConstantEmissions GlobalCO2 (sum constant) "Constant emissions continue accumulating carbon."
    , ScenarioRecord "linear_decline_to_zero" LinearDecline GlobalCO2 (sum linear) "Linear decline still accumulates until net zero."
    , ScenarioRecord "exponential_decline" ExponentialDecline GlobalCO2 (sum exponential) "Early reductions reduce cumulative burden."
    ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
