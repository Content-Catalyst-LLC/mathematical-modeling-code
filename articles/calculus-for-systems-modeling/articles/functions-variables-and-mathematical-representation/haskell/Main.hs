{-# OPTIONS_GHC -Wall #-}

module Main where

newtype Input = Input Double deriving (Show)
newtype Output = Output Double deriving (Show)
newtype Intercept = Intercept Double deriving (Show)
newtype Slope = Slope Double deriving (Show)
newtype Capacity = Capacity Double deriving (Show)
newtype Rate = Rate Double deriving (Show)
newtype Midpoint = Midpoint Double deriving (Show)

data FunctionalForm
  = Linear Intercept Slope
  | Logistic Capacity Rate Midpoint
  deriving (Show)

evaluate :: FunctionalForm -> Input -> Output
evaluate (Linear (Intercept a) (Slope b)) (Input x) =
  Output (a + b * x)

evaluate (Logistic (Capacity k) (Rate r) (Midpoint c)) (Input x) =
  Output (k / (1.0 + exp (-r * (x - c))))

main :: IO ()
main = do
  let x = Input 4.0
  let linearModel = Linear (Intercept 10.0) (Slope 2.0)
  let logisticModel = Logistic (Capacity 100.0) (Rate 0.75) (Midpoint 5.0)

  print linearModel
  print (evaluate linearModel x)
  print logisticModel
  print (evaluate logisticModel x)
