module Main where

data PhaseRecord = PhaseRecord
  { x :: Double
  , y :: Double
  , dxdt :: Double
  , dydt :: Double
  , speed :: Double
  , warning :: String
  } deriving (Show)

predatorPreyRates ::
  Double ->
  Double ->
  Double ->
  Double ->
  Double ->
  Double ->
  (Double, Double)
predatorPreyRates xValue yValue alpha beta delta gamma =
  let dx = alpha * xValue - beta * xValue * yValue
      dy = delta * xValue * yValue - gamma * yValue
  in (dx, dy)

buildRecord :: Double -> Double -> PhaseRecord
buildRecord xValue yValue =
  let alpha = 0.7
      beta = 0.05
      delta = 0.02
      gamma = 0.5
      (dx, dy) = predatorPreyRates xValue yValue alpha beta delta gamma
      s = sqrt (dx * dx + dy * dy)
  in PhaseRecord
      xValue
      yValue
      dx
      dy
      s
      "Vector-field values depend on parameter values, state ranges, and the assumed interaction structure."

phaseRecords :: [PhaseRecord]
phaseRecords =
  [ buildRecord xValue yValue
  | xValue <- [0,5..60]
  , yValue <- [0,3..30]
  ]

main :: IO ()
main =
  mapM_ print (take 20 phaseRecords)
