{-# OPTIONS_GHC -Wall #-}
module Main where

data RawScenario = RawScenario String Double Double Double Double deriving (Show)
data ValidScenario = ValidScenario String Double Double Double Double deriving (Show)
data ValidationResult = Valid ValidScenario | Invalid String deriving (Show)

validateScenario :: RawScenario -> ValidationResult
validateScenario (RawScenario n initial rate capacity timeHorizon)
  | initial < 0 = Invalid "initial_state must be nonnegative"
  | rate < 0 = Invalid "rate must be nonnegative"
  | capacity <= 0 = Invalid "capacity must be positive"
  | timeHorizon < 0 = Invalid "time_horizon must be nonnegative"
  | initial > capacity = Invalid "initial_state exceeds capacity"
  | otherwise = Valid (ValidScenario n initial rate capacity timeHorizon)

main :: IO ()
main = do
  let scenarios =
        [ RawScenario "baseline" 10.0 0.20 100.0 20.0
        , RawScenario "invalid_negative_state" (-5.0) 0.20 100.0 20.0
        , RawScenario "outside_capacity" 120.0 0.20 100.0 20.0
        ]
  mapM_ (print . validateScenario) scenarios
