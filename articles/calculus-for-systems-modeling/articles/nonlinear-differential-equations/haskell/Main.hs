module Main where

data NonlinearRecord = NonlinearRecord
  { scenario :: String
  , time :: Double
  , state :: Double
  , rate :: Double
  , parameterA :: Double
  , parameterB :: Double
  , parameterC :: Double
  , method :: String
  , warning :: String
  } deriving (Show)

logisticRate :: Double -> Double -> Double -> Double
logisticRate x growth carrying =
  growth * x * (1 - x / carrying)

bistableRate :: Double -> Double -> Double
bistableRate x threshold =
  x * (1 - x) * (x - threshold)

simulateScalar ::
  String ->
  Double ->
  Double ->
  Int ->
  (Double -> Double) ->
  (Double, Double, Double) ->
  String ->
  [NonlinearRecord]
simulateScalar label x0 dt steps rateFunction parameters warningText =
  go 0 x0
  where
    (pa, pb, pc) = parameters
    go n x
      | n > steps = []
      | otherwise =
          let t = fromIntegral n * dt
              r = rateFunction x
              record =
                NonlinearRecord label t x r pa pb pc "explicit_euler" warningText
              xNext = x + dt * r
          in record : go (n + 1) xNext

main :: IO ()
main = do
  mapM_ print (take 10 logisticRecords)
  mapM_ print (take 10 thresholdRecords)
  where
    logisticRecords =
      simulateScalar "logistic_growth" 10 0.05 300 (\x -> logisticRate x 0.6 100) (0.6, 100, 0) "Logistic growth assumes a fixed carrying capacity and smooth density limitation."
    thresholdRecords =
      simulateScalar "bistable_threshold" 0.35 0.05 300 (\x -> bistableRate x 0.4) (0.4, 0, 0) "Threshold behavior is illustrative and should not be interpreted without evidence for the threshold."
