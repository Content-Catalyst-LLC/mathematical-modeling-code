module Main where

data StabilityRecord = StabilityRecord
  { scenario :: String
  , equilibrium :: Double
  , derivativeValue :: Double
  , stability :: String
  , domainMin :: Double
  , domainMax :: Double
  , warning :: String
  } deriving (Show)

classifyScalarStability :: Double -> String
classifyScalarStability derivativeValue
  | derivativeValue < (-1e-8) = "locally_stable"
  | derivativeValue > 1e-8 = "locally_unstable"
  | otherwise = "inconclusive_by_linearization"

logisticDerivative :: Double -> Double -> Double -> Double
logisticDerivative x growth carrying =
  growth * (1 - 2 * x / carrying)

bistableRate :: Double -> Double -> Double
bistableRate x threshold =
  x * (1 - x) * (x - threshold)

numericalDerivative :: (Double -> Double) -> Double -> Double
numericalDerivative rateFunction x =
  let h = 1e-5
  in (rateFunction (x + h) - rateFunction (x - h)) / (2 * h)

logisticRecords :: [StabilityRecord]
logisticRecords =
  [ let d = logisticDerivative eq 0.6 100
    in StabilityRecord "logistic_growth" eq d (classifyScalarStability d) 0 100 "Logistic stability assumes fixed carrying capacity and smooth density limitation."
  | eq <- [0, 100]
  ]

bistableRecords :: [StabilityRecord]
bistableRecords =
  [ let threshold = 0.4
        d = numericalDerivative (\x -> bistableRate x threshold) eq
    in StabilityRecord "bistable_threshold" eq d (classifyScalarStability d) 0 1 "Threshold stability depends on the assumed threshold and domain."
  | eq <- [0, 0.4, 1]
  ]

main :: IO ()
main =
  mapM_ print (logisticRecords ++ bistableRecords)
