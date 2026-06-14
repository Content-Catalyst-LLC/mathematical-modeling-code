{-# OPTIONS_GHC -Wall #-}

module Main where

newtype Location = Location Double deriving (Show)
newtype StepSize = StepSize Double deriving (Show)
newtype Estimate = Estimate Double deriving (Show)
newtype ExactValue = ExactValue Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)

data ApproximationRun = ApproximationRun
  { location :: Location
  , stepSize :: StepSize
  , estimate :: Estimate
  , exactValue :: ExactValue
  , absoluteError :: AbsoluteError
  } deriving (Show)

systemResponse :: Location -> Double
systemResponse (Location x) =
  exp (0.2 * x)

exactDerivative :: Location -> ExactValue
exactDerivative (Location x) =
  ExactValue (0.2 * exp (0.2 * x))

differenceQuotient :: Location -> StepSize -> Estimate
differenceQuotient loc@(Location x) (StepSize h) =
  Estimate ((systemResponse (Location (x + h)) - systemResponse loc) / h)

runApproximation :: Location -> StepSize -> ApproximationRun
runApproximation loc step =
  let est@(Estimate e) = differenceQuotient loc step
      exact@(ExactValue v) = exactDerivative loc
  in ApproximationRun
      { location = loc
      , stepSize = step
      , estimate = est
      , exactValue = exact
      , absoluteError = AbsoluteError (abs (e - v))
      }

main :: IO ()
main = do
  let locationValue = Location 5.0
  let steps = map StepSize [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
  mapM_ (print . runApproximation locationValue) steps
