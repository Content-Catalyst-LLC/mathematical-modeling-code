module Main where

data DelayRecord = DelayRecord
  { stepNumber :: Int
  , timeValue :: Double
  , currentState :: Double
  , delayedState :: Double
  , derivativeValue :: Double
  , targetValue :: Double
  , absoluteGap :: Double
  , warning :: String
  } deriving (Show)

delayedLookup :: [Double] -> Int -> Int -> Double -> Double
delayedLookup states stepValue delayStepsValue initialValue =
  let delayedIndex = stepValue - delayStepsValue
  in if delayedIndex < 0 then initialValue else states !! delayedIndex

simulateDelayedAdjustment ::
  Double ->
  Double ->
  Double ->
  Double ->
  Double ->
  Int ->
  [DelayRecord]
simulateDelayedAdjustment initialState target adjustmentRate delayTime dt steps =
  go 0 [initialState]
  where
    delayStepsValue = round (delayTime / dt)

    go stepValue states
      | stepValue > steps = []
      | otherwise =
          let time = fromIntegral stepValue * dt
              current = last states
              delayed = delayedLookup states stepValue delayStepsValue initialState
              derivative = adjustmentRate * (target - delayed)
              nextState = current + dt * derivative
              record = DelayRecord
                stepValue
                time
                current
                delayed
                derivative
                target
                (abs (current - target))
                "Delayed adjustment depends on delay length, history function, time step, and feedback strength."
          in record : go (stepValue + 1) (states ++ [nextState])

main :: IO ()
main =
  mapM_ print (
    simulateDelayedAdjustment
      80
      100
      0.2
      5
      0.1
      120
  )
