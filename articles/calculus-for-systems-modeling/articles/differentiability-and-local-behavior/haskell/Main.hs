{-# OPTIONS_GHC -Wall #-}

module Main where

newtype Location = Location Double deriving (Show)
newtype StepSize = StepSize Double deriving (Show)
newtype Estimate = Estimate Double deriving (Show)
newtype OneSidedGap = OneSidedGap Double deriving (Show)

data DifferentiabilityFlag
  = LocallySmooth
  | PossibleKink
  | BoundaryOnly
  | NeedsReview
  deriving (Show)

data DerivativeDiagnostic = DerivativeDiagnostic
  { location :: Location
  , stepSize :: StepSize
  , forwardEstimate :: Estimate
  , backwardEstimate :: Estimate
  , oneSidedGap :: OneSidedGap
  , flag :: DifferentiabilityFlag
  } deriving (Show)

absResponse :: Location -> Double
absResponse (Location x) =
  abs x

forwardDifference :: (Location -> Double) -> Location -> StepSize -> Estimate
forwardDifference f loc@(Location x) (StepSize h) =
  Estimate ((f (Location (x + h)) - f loc) / h)

backwardDifference :: (Location -> Double) -> Location -> StepSize -> Estimate
backwardDifference f loc@(Location x) (StepSize h) =
  Estimate ((f loc - f (Location (x - h))) / h)

classify :: OneSidedGap -> DifferentiabilityFlag
classify (OneSidedGap gap)
  | gap > 0.5 = PossibleKink
  | otherwise = LocallySmooth

diagnose :: Location -> StepSize -> DerivativeDiagnostic
diagnose loc h =
  let fwd@(Estimate a) = forwardDifference absResponse loc h
      bwd@(Estimate b) = backwardDifference absResponse loc h
      gap = OneSidedGap (abs (a - b))
  in DerivativeDiagnostic
      { location = loc
      , stepSize = h
      , forwardEstimate = fwd
      , backwardEstimate = bwd
      , oneSidedGap = gap
      , flag = classify gap
      }

main :: IO ()
main = do
  let loc = Location 0.0
  let steps = map StepSize [1.0, 0.5, 0.25, 0.125, 0.0625]
  mapM_ (print . diagnose loc) steps
