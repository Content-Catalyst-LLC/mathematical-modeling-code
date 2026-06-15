module Main where

newtype Location = Location Double deriving (Show)
newtype StepSize = StepSize Double deriving (Show)
newtype Estimate = Estimate Double deriving (Show)
newtype Exact = Exact Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)
newtype Elasticity = Elasticity Double deriving (Show)

data RateMethod = ForwardDifference | BackwardDifference | CentralDifference deriving (Show)

data RateDiagnostic = RateDiagnostic
  { method :: RateMethod
  , location :: Location
  , stepSize :: StepSize
  , estimate :: Estimate
  , exactValue :: Exact
  , absoluteError :: AbsoluteError
  , elasticityValue :: Elasticity
  } deriving (Show)

systemResponse :: Location -> Double
systemResponse (Location x) = exp (0.2 * x)

exactDerivative :: Location -> Exact
exactDerivative (Location x) = Exact (0.2 * exp (0.2 * x))

forwardDifference :: Location -> StepSize -> Estimate
forwardDifference loc@(Location x) (StepSize h) =
  Estimate ((systemResponse (Location (x + h)) - systemResponse loc) / h)

backwardDifference :: Location -> StepSize -> Estimate
backwardDifference loc@(Location x) (StepSize h) =
  Estimate ((systemResponse loc - systemResponse (Location (x - h))) / h)

centralDifference :: Location -> StepSize -> Estimate
centralDifference (Location x) (StepSize h) =
  Estimate ((systemResponse (Location (x + h)) - systemResponse (Location (x - h))) / (2 * h))

elasticity :: Location -> Estimate -> Elasticity
elasticity loc@(Location x) (Estimate d) = Elasticity ((x / systemResponse loc) * d)

diagnose :: RateMethod -> Location -> StepSize -> RateDiagnostic
diagnose m loc h =
  let est@(Estimate e) =
        case m of
          ForwardDifference -> forwardDifference loc h
          BackwardDifference -> backwardDifference loc h
          CentralDifference -> centralDifference loc h
      exact@(Exact v) = exactDerivative loc
  in RateDiagnostic m loc h est exact (AbsoluteError (abs (e - v))) (elasticity loc est)

main :: IO ()
main = do
  let loc = Location 5.0
  let steps = map StepSize [1.0, 0.5, 0.25, 0.125]
  mapM_ (print . diagnose ForwardDifference loc) steps
  mapM_ (print . diagnose BackwardDifference loc) steps
  mapM_ (print . diagnose CentralDifference loc) steps
