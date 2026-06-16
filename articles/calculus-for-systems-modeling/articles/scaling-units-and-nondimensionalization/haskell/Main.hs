module Main where

data Dimension
  = Stock
  | TimeDimension
  | InverseTime
  | Length
  | Dimensionless
  deriving (Show, Eq)

data UnitRecord = UnitRecord
  { quantityName :: String
  , quantityValue :: Double
  , unitLabel :: String
  , dimension :: Dimension
  , sourceNote :: String
  , unitWarning :: String
  } deriving (Show, Eq)

data ScaleRecord = ScaleRecord
  { scaleName :: String
  , scaleValue :: Double
  , scaleUnit :: String
  , scaleInterpretation :: String
  , scaleWarning :: String
  } deriving (Show, Eq)

data NondimensionalRecord = NondimensionalRecord
  { dimensionlessName :: String
  , dimensionalValue :: Double
  , referenceScale :: Double
  , dimensionlessValue :: Double
  , dimensionlessInterpretation :: String
  } deriving (Show, Eq)

unitRecords :: [UnitRecord]
unitRecords =
  [ UnitRecord "population_stock" 40.0 "state units" Stock "synthetic teaching value" "Synthetic value; do not treat as empirical measurement."
  , UnitRecord "carrying_capacity" 100.0 "state units" Stock "synthetic teaching capacity" "Capacity scale controls normalized interpretation."
  , UnitRecord "growth_rate" 0.35 "per time unit" InverseTime "synthetic teaching rate" "Rate units must match the time variable."
  ]

scaleRecords :: [ScaleRecord]
scaleRecords =
  [ ScaleRecord "stock_scale" 100.0 "state units" "carrying capacity used to normalize population stock" "Changing the capacity scale changes dimensionless stock."
  , ScaleRecord "time_scale" (1 / 0.35) "time units" "inverse growth rate used as characteristic response time" "Changing the growth-rate scale changes dimensionless time."
  ]

nondimensionalRecords :: [NondimensionalRecord]
nondimensionalRecords =
  [ NondimensionalRecord "scaled_stock" 40.0 100.0 (40.0 / 100.0) "population stock as fraction of carrying capacity"
  , NondimensionalRecord "scaled_time" 20.0 (1 / 0.35) (0.35 * 20.0) "time measured in characteristic growth-time units"
  ]

main :: IO ()
main = do
  putStrLn "Unit records:"
  mapM_ print unitRecords
  putStrLn ""
  putStrLn "Scale records:"
  mapM_ print scaleRecords
  putStrLn ""
  putStrLn "Nondimensional records:"
  mapM_ print nondimensionalRecords
