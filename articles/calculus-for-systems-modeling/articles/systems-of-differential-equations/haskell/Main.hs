module Main where

data CoupledRecord = CoupledRecord
  { scenario :: String
  , time :: Double
  , prey :: Double
  , predator :: Double
  , preyRate :: Double
  , predatorRate :: Double
  , alpha :: Double
  , beta :: Double
  , delta :: Double
  , gamma :: Double
  , method :: String
  , warning :: String
  } deriving (Show)

predatorPreyRates :: Double -> Double -> Double -> Double -> Double -> Double -> (Double, Double)
predatorPreyRates prey predator a b d g =
  let preyRateValue = a * prey - b * prey * predator
      predatorRateValue = d * prey * predator - g * predator
  in (preyRateValue, predatorRateValue)

simulatePredatorPrey :: Double -> Double -> Double -> Double -> Double -> Double -> Double -> Int -> [CoupledRecord]
simulatePredatorPrey prey0 predator0 a b d g dt steps =
  go 0 prey0 predator0
  where
    go n preyState predatorState
      | n > steps = []
      | otherwise =
          let t = fromIntegral n * dt
              (preyRateValue, predatorRateValue) =
                predatorPreyRates preyState predatorState a b d g
              record =
                CoupledRecord
                  "predator_prey_coupled_system"
                  t
                  preyState
                  predatorState
                  preyRateValue
                  predatorRateValue
                  a
                  b
                  d
                  g
                  "explicit_euler"
                  "Predator-prey terms are illustrative and assume continuous well-mixed interaction."
              preyNext = max 0 (preyState + dt * preyRateValue)
              predatorNext = max 0 (predatorState + dt * predatorRateValue)
          in record : go (n + 1) preyNext predatorNext

main :: IO ()
main =
  mapM_ print (take 10 (simulatePredatorPrey 40 9 0.7 0.05 0.02 0.5 0.01 2000))
