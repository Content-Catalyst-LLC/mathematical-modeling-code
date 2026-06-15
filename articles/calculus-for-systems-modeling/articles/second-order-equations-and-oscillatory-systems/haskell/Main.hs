module Main where

data OscillationRecord = OscillationRecord
  { scenario :: String
  , time :: Double
  , position :: Double
  , velocity :: Double
  , accelerationValue :: Double
  , dampingRatio :: Double
  , naturalFrequency :: Double
  , forcingValue :: Double
  , method :: String
  , warning :: String
  } deriving (Show)

forcingFunction :: Double -> Double -> Double -> Double
forcingFunction t amplitude frequency = amplitude * cos (frequency * t)

acceleration :: Double -> Double -> Double -> Double -> Double -> Double -> Double -> Double
acceleration x v t damping natural forcingAmplitude forcingFrequency =
  let force = forcingFunction t forcingAmplitude forcingFrequency
      dampingTerm = 2 * damping * natural * v
      restoring = natural * natural * x
  in force - dampingTerm - restoring

simulateOscillator :: String -> Double -> Double -> Double -> Double -> Double -> Double -> Double -> Int -> [OscillationRecord]
simulateOscillator label x0 v0 damping natural forcingAmplitude forcingFrequency dt steps =
  go 0 x0 v0
  where
    go n x v
      | n > steps = []
      | otherwise =
          let t = fromIntegral n * dt
              a = acceleration x v t damping natural forcingAmplitude forcingFrequency
              force = forcingFunction t forcingAmplitude forcingFrequency
              record = OscillationRecord label t x v a damping natural force "explicit_euler_first_order_system" "Explicit Euler is transparent but can distort oscillatory systems if the step size is too large."
              vNext = v + dt * a
              xNext = x + dt * vNext
          in record : go (n + 1) xNext vNext

main :: IO ()
main = do
  mapM_ print (take 10 (simulateOscillator "underdamped_unforced" 1 0 0.2 1 0 1 0.02 500))
  mapM_ print (take 10 (simulateOscillator "forced_near_resonance" 1 0 0.1 1 0.2 1 0.02 500))
