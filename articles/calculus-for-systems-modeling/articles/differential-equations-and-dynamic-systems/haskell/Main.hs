module Main where

data DynamicRecord = DynamicRecord
  { scenario :: String
  , modelType :: String
  , time :: Double
  , state :: Double
  , rate :: Double
  , growthRate :: Double
  , carryingCapacity :: Maybe Double
  , method :: String
  , warning :: String
  } deriving (Show)

exponentialRate :: Double -> Double -> Double
exponentialRate x r = r * x

logisticRate :: Double -> Double -> Double -> Double
logisticRate x r capacity = r * x * (1 - x / capacity)

simulateExponential :: Double -> Double -> Double -> Int -> [DynamicRecord]
simulateExponential x0 r dt steps = go 0 x0
  where
    go n x
      | n > steps = []
      | otherwise =
          let t = fromIntegral n * dt
              dx = exponentialRate x r
              record = DynamicRecord "exponential_growth" "dx_dt_equals_r_x" t x dx r Nothing "explicit_euler" "Exponential growth assumes no capacity constraint."
          in record : go (n + 1) (x + dt * dx)

simulateLogistic :: Double -> Double -> Double -> Double -> Int -> [DynamicRecord]
simulateLogistic x0 r capacity dt steps = go 0 x0
  where
    go n x
      | n > steps = []
      | otherwise =
          let t = fromIntegral n * dt
              dx = logisticRate x r capacity
              record = DynamicRecord "logistic_growth" "dx_dt_equals_r_x_one_minus_x_over_K" t x dx r (Just capacity) "explicit_euler" "Logistic growth assumes a fixed carrying capacity."
          in record : go (n + 1) (x + dt * dx)

main :: IO ()
main = do
  mapM_ print (take 5 (simulateExponential 10 0.35 0.1 100))
  mapM_ print (take 5 (simulateLogistic 10 0.35 100 0.1 100))
