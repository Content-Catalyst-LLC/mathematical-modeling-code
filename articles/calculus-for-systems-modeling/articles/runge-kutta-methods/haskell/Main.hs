module Main where

data RungeKuttaRecord = RungeKuttaRecord
  { stepNumber :: Int
  , timeValue :: Double
  , eulerValue :: Double
  , rk4Value :: Double
  , exactValue :: Double
  , eulerAbsoluteError :: Double
  , rk4AbsoluteError :: Double
  , stepSize :: Double
  , warning :: String
  } deriving (Show)

rateFunction :: Double -> Double -> Double -> Double
rateFunction _ y decayRate =
  -decayRate * y

exactSolution :: Double -> Double -> Double -> Double
exactSolution t y0 decayRate =
  y0 * exp (-decayRate * t)

eulerStep :: Double -> Double -> Double -> Double -> Double
eulerStep t y h decayRate =
  y + h * rateFunction t y decayRate

rk4Step :: Double -> Double -> Double -> Double -> Double
rk4Step t y h decayRate =
  y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
  where
    k1 = rateFunction t y decayRate
    k2 = rateFunction (t + h / 2.0) (y + h * k1 / 2.0) decayRate
    k3 = rateFunction (t + h / 2.0) (y + h * k2 / 2.0) decayRate
    k4 = rateFunction (t + h) (y + h * k3) decayRate

rkAudit :: Double -> Double -> Double -> Double -> [RungeKuttaRecord]
rkAudit y0 decayRate h stopTime =
  go 0 y0 y0
  where
    steps = round (stopTime / h)
    go step eulerY rkY
      | step > steps = []
      | otherwise =
          let t = fromIntegral step * h
              exact = exactSolution t y0 decayRate
              record = RungeKuttaRecord
                step
                t
                eulerY
                rkY
                exact
                (abs (eulerY - exact))
                (abs (rkY - exact))
                h
                "Runge-Kutta estimates depend on rate function, step size, smoothness, stiffness, and benchmark comparison."
              nextEuler = eulerStep t eulerY h decayRate
              nextRk = rk4Step t rkY h decayRate
          in record : go (step + 1) nextEuler nextRk

main :: IO ()
main = mapM_ print (rkAudit 100.0 0.35 0.5 20.0)
