module Main where

data EulerRecord = EulerRecord
  { stepNumber :: Int
  , timeValue :: Double
  , eulerValue :: Double
  , exactValue :: Double
  , absoluteError :: Double
  , stepSize :: Double
  , stabilityMultiplier :: Double
  , stabilityStatus :: String
  , warning :: String
  } deriving (Show)

rateFunction :: Double -> Double -> Double -> Double
rateFunction _ y decayRate =
  -decayRate * y

exactSolution :: Double -> Double -> Double -> Double
exactSolution t y0 decayRate =
  y0 * exp (-decayRate * t)

eulerAudit :: Double -> Double -> Double -> Double -> [EulerRecord]
eulerAudit y0 decayRate h stopTime =
  go 0 y0
  where
    steps = round (stopTime / h)
    multiplier = 1.0 - h * decayRate
    status = if abs multiplier <= 1.0 then "stable_for_simple_decay" else "unstable_risk"
    go step y
      | step > steps = []
      | otherwise =
          let t = fromIntegral step * h
              exact = exactSolution t y0 decayRate
              record = EulerRecord
                step
                t
                y
                exact
                (abs (y - exact))
                h
                multiplier
                status
                "Euler estimates depend on time step, rate function, initial condition, stability, and accumulated error."
              nextY = y + h * rateFunction t y decayRate
          in record : go (step + 1) nextY

main :: IO ()
main = mapM_ print (eulerAudit 100.0 0.35 0.1 20.0)
