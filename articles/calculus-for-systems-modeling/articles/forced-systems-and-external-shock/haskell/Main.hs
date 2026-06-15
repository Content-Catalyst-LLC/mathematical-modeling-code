module Main where

data ShockRecord = ShockRecord
  { stepNumber :: Int
  , timeValue :: Double
  , baselineState :: Double
  , forcedState :: Double
  , shockValue :: Double
  , absoluteDeviation :: Double
  , warning :: String
  } deriving (Show)

restoringRate :: Double -> Double -> Double -> Double
restoringRate x equilibrium recoveryRate =
  -recoveryRate * (x - equilibrium)

impulseShock :: Double -> Double -> Double -> Double
impulseShock time shockTime shockMagnitude =
  if abs (time - shockTime) < 1e-12 then shockMagnitude else 0

simulateForcedSystem ::
  Double ->
  Double ->
  Double ->
  Double ->
  Double ->
  Double ->
  Int ->
  [ShockRecord]
simulateForcedSystem initialState equilibrium recoveryRate shockTime shockMagnitude dt steps =
  go 0 initialState initialState
  where
    go step baseline forced
      | step > steps = []
      | otherwise =
          let time = fromIntegral step * dt
              shock = impulseShock time shockTime shockMagnitude
              record = ShockRecord
                step
                time
                baseline
                forced
                shock
                (abs (forced - baseline))
                "Shock response depends on forcing form, timing, magnitude, recovery rate, and numerical step size."
              nextBaseline = baseline + dt * restoringRate baseline equilibrium recoveryRate
              shockedForced = if shock /= 0 then forced + shock else forced
              nextForced = shockedForced + dt * restoringRate shockedForced equilibrium recoveryRate
          in record : go (step + 1) nextBaseline nextForced

main :: IO ()
main =
  mapM_ print (
    simulateForcedSystem
      100
      100
      0.15
      10
      (-30)
      0.1
      120
  )
