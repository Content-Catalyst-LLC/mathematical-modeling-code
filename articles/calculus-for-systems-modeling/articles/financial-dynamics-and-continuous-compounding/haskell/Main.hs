module Main where

data RateConvention
  = NominalRate
  | RealRate
  | EffectiveRate
  | ContinuousRate
  | VariableRate
  deriving (Show, Eq)

data FinancialModelType
  = FutureValue
  | PresentValue
  | NetPresentValue
  | DebtDynamics
  | PortfolioCompounding
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
  , modelType :: FinancialModelType
  , rateConvention :: RateConvention
  , finalValue :: Double
  , scenarioWarning :: String
  } deriving (Show, Eq)

continuousFutureValue :: Double -> Double -> Double -> Double
continuousFutureValue v0 r t = v0 * exp (r * t)

continuousPresentValue :: Double -> Double -> Double -> Double
continuousPresentValue fv r t = fv * exp (negate r * t)

parameterRecords :: [ParameterRecord]
parameterRecords =
  [ ParameterRecord "V0" 1000.0 "currency units" "initial value or principal" "Initial value must match the modeled account, asset, or debt balance."
  , ParameterRecord "r" 0.05 "per year" "interest, return, or discount rate" "Rate convention must be documented."
  , ParameterRecord "t" 30.0 "years" "time horizon" "Long horizons amplify small rate differences."
  ]

scenarioRecords :: [ScenarioRecord]
scenarioRecords =
  [ ScenarioRecord "continuous_compounding_case" FutureValue ContinuousRate (continuousFutureValue 1000.0 0.05 30.0) "Continuous compounding accumulates value exponentially."
  , ScenarioRecord "discounted_future_value" PresentValue ContinuousRate (continuousPresentValue 5000.0 0.05 30.0) "Discounting translates future value into present value."
  , ScenarioRecord "debt_dynamics_case" DebtDynamics NominalRate 1800.0 "Debt balance depends on interest, payments, and time."
  ]

main :: IO ()
main = do
  putStrLn "Parameter records:"
  mapM_ print parameterRecords
  putStrLn ""
  putStrLn "Scenario records:"
  mapM_ print scenarioRecords
