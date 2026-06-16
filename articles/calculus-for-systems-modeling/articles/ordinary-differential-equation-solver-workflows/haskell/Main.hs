module Main where

data SolverRecord = SolverRecord
  { stepNumber :: Int
  , timeValue :: Double
  , solverValue :: Double
  , exactValue :: Double
  , absoluteError :: Double
  , solverMethod :: String
  , stepSize :: Double
  , warning :: String
  } deriving (Show)

rateFunction :: Double -> Double -> Double -> Double
rateFunction _ y decayRate =
  -decayRate * y

exactSolution :: Double -> Double -> Double -> Double
exactSolution t y0 decayRate =
  y0 * exp (-decayRate * t)

rk4Step :: Double -> Double -> Double -> Double -> Double
rk4Step t y h decayRate =
  y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
  where
    k1 = rateFunction t y decayRate
    k2 = rateFunction (t + h / 2.0) (y + h * k1 / 2.0) decayRate
    k3 = rateFunction (t + h / 2.0) (y + h * k2 / 2.0) decayRate
    k4 = rateFunction (t + h) (y + h * k3) decayRate

solverAudit :: Double -> Double -> Double -> Double -> [SolverRecord]
solverAudit y0 decayRate h stopTime =
  go 0 y0
  where
    steps = round (stopTime / h)
    go step y
      | step > steps = []
      | otherwise =
          let t = fromIntegral step * h
              exact = exactSolution t y0 decayRate
              record = SolverRecord
                step
                t
                y
                exact
                (abs (y - exact))
                "fixed_step_rk4"
                h
                "ODE solver outputs depend on equation, initial condition, method, tolerances, step size, stiffness, and diagnostics."
              nextY = rk4Step t y h decayRate
          in record : go (step + 1) nextY

main :: IO ()
main = mapM_ print (solverAudit 100.0 0.35 0.5 20.0)
