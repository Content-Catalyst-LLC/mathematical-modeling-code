module Main where

data LinearRecord = LinearRecord
  { scenario :: String
  , time :: Double
  , analyticalState :: Double
  , eulerState :: Double
  , absoluteError :: Double
  , inputRate :: Double
  , lossRate :: Double
  , equilibrium :: Double
  , initialState :: Double
  , method :: String
  , warning :: String
  } deriving (Show)

eqValue :: Double -> Double -> Double
eqValue input loss = input / loss

analyticalSolution :: Double -> Double -> Double -> Double -> Double
analyticalSolution t y0 input loss =
  let eq = eqValue input loss
  in eq + (y0 - eq) * exp (-loss * t)

rateLaw :: Double -> Double -> Double -> Double
rateLaw y input loss = input - loss * y

simulateLinearInputLoss :: Double -> Double -> Double -> Double -> Int -> [LinearRecord]
simulateLinearInputLoss y0 input loss dt steps = go 0 y0
  where
    eq = eqValue input loss
    go n y
      | n > steps = []
      | otherwise =
          let t = fromIntegral n * dt
              analytical = analyticalSolution t y0 input loss
              dy = rateLaw y input loss
              record = LinearRecord "input_loss_balance" t analytical y (abs (analytical - y)) input loss eq y0 "analytical_vs_explicit_euler" "Assumes constant input and proportional loss."
          in record : go (n + 1) (y + dt * dy)

main :: IO ()
main =
  mapM_ print (take 10 (simulateLinearInputLoss 20 12 0.4 0.1 100))
