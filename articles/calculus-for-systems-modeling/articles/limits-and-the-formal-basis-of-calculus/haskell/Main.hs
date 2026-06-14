{-# OPTIONS_GHC -Wall #-}

module Main where

newtype Location = Location Double deriving (Show)
newtype StepSize = StepSize Double deriving (Show)
newtype Estimate = Estimate Double deriving (Show)
newtype Exact = Exact Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)

data Method
  = ForwardDifference
  | CentralDifference
  | RichardsonCentral
  deriving (Show)

data LimitExperiment = LimitExperiment
  { method :: Method
  , location :: Location
  , stepSize :: StepSize
  , estimate :: Estimate
  , exactValue :: Exact
  , absoluteError :: AbsoluteError
  } deriving (Show)

systemResponse :: Location -> Double
systemResponse (Location x) =
  exp (0.2 * x)

exactDerivative :: Location -> Exact
exactDerivative (Location x) =
  Exact (0.2 * exp (0.2 * x))

forwardDifference :: Location -> StepSize -> Estimate
forwardDifference loc@(Location x) (StepSize h) =
  Estimate ((systemResponse (Location (x + h)) - systemResponse loc) / h)

centralDifference :: Location -> StepSize -> Estimate
centralDifference (Location x) (StepSize h) =
  Estimate ((systemResponse (Location (x + h)) - systemResponse (Location (x - h))) / (2 * h))

richardsonCentral :: Estimate -> Estimate -> Estimate
richardsonCentral (Estimate centralH) (Estimate centralH2) =
  Estimate ((4 * centralH2 - centralH) / 3)

runExperiment :: Method -> Location -> StepSize -> LimitExperiment
runExperiment m loc h@(StepSize step) =
  let est =
        case m of
          ForwardDifference -> forwardDifference loc h
          CentralDifference -> centralDifference loc h
          RichardsonCentral ->
            richardsonCentral (centralDifference loc h) (centralDifference loc (StepSize (step / 2)))
      Estimate e = est
      exact@(Exact v) = exactDerivative loc
  in LimitExperiment
      { method = m
      , location = loc
      , stepSize = h
      , estimate = est
      , exactValue = exact
      , absoluteError = AbsoluteError (abs (e - v))
      }

main :: IO ()
main = do
  let loc = Location 5.0
  let steps = map StepSize [1.0, 0.5, 0.25, 0.125, 0.0625]
  mapM_ (print . runExperiment ForwardDifference loc) steps
  mapM_ (print . runExperiment CentralDifference loc) steps
  mapM_ (print . runExperiment RichardsonCentral loc) steps
