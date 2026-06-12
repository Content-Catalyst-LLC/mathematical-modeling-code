module Main where

data LogisticModel = LogisticModel
  { modelName :: String
  , initialState :: Double
  , growthRate :: Double
  , carryingCapacity :: Double
  , timeStep :: Double
  , steps :: Int
  } deriving (Show)

derivative :: Double -> Double -> Double -> Double
derivative x r k = r * x * (1.0 - x / k)

rk4Step :: LogisticModel -> Double -> Double
rk4Step model x =
  let dt = timeStep model
      r = growthRate model
      k = carryingCapacity model
      k1 = derivative x r k
      k2 = derivative (x + 0.5 * dt * k1) r k
      k3 = derivative (x + 0.5 * dt * k2) r k
      k4 = derivative (x + dt * k3) r k
  in max 0.0 (x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4))

simulate :: LogisticModel -> [Double]
simulate model = take (steps model + 1) $ iterate (rk4Step model) (initialState model)

main :: IO ()
main = do
  let model = LogisticModel "haskell_baseline" 10.0 0.35 100.0 0.1 160
  let states = simulate model
  putStrLn $ "Haskell scenario=" ++ modelName model ++ " final_state=" ++ show (last states)
