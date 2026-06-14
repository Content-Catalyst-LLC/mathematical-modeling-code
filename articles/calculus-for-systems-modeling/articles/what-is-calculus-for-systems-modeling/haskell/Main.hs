{-# OPTIONS_GHC -Wall #-}

module Main where

data ModelState = ModelState
  { time :: Double
  , stock :: Double
  } deriving (Show)

data Parameters = Parameters
  { rate :: Double
  , capacity :: Double
  , dt :: Double
  } deriving (Show)

derivative :: Parameters -> ModelState -> Double
derivative params state =
  rate params * stock state * (1.0 - stock state / capacity params)

stepModel :: Parameters -> ModelState -> ModelState
stepModel params state =
  let change = derivative params state * dt params
  in ModelState
      { time = time state + dt params
      , stock = max 0.0 (stock state + change)
      }

simulate :: Int -> Parameters -> ModelState -> [ModelState]
simulate steps params initialState =
  take (steps + 1) (iterate (stepModel params) initialState)

main :: IO ()
main = do
  let params = Parameters { rate = 0.20, capacity = 100.0, dt = 0.1 }
  let initialState = ModelState { time = 0.0, stock = 10.0 }
  mapM_ print (take 12 (simulate 300 params initialState))
