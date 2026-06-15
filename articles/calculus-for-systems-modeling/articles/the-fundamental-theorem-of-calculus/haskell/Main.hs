module Main where

newtype Time = Time Double deriving (Show)
newtype State = State Double deriving (Show)
newtype Rate = Rate Double deriving (Show)
newtype Accumulation = Accumulation Double deriving (Show)
newtype Residual = Residual Double deriving (Show)

data FTCAudit = FTCAudit
  { intervalStart :: Time
  , intervalEnd :: Time
  , stateStart :: State
  , stateEnd :: State
  , endpointDifference :: Accumulation
  , accumulatedRate :: Accumulation
  , residual :: Residual
  , method :: String
  } deriving (Show)

stateValue :: Time -> State
stateValue (Time t) =
  State (50.0 + 2.0 * t + 3.0 * sin t)

rateValue :: Time -> Rate
rateValue (Time t) =
  Rate (2.0 + 3.0 * cos t)

trapStep :: Time -> Time -> Double
trapStep a@(Time t0) b@(Time t1) =
  let Rate r0 = rateValue a
      Rate r1 = rateValue b
      dt = t1 - t0
  in 0.5 * (r0 + r1) * dt

integrateRate :: [Time] -> Accumulation
integrateRate [] = Accumulation 0.0
integrateRate [_] = Accumulation 0.0
integrateRate times =
  let pairs = zip times (tail times)
  in Accumulation (sum [trapStep a b | (a,b) <- pairs])

audit :: [Time] -> FTCAudit
audit times =
  let a = head times
      b = last times
      State s0 = stateValue a
      State s1 = stateValue b
      endpoint = s1 - s0
      Accumulation acc = integrateRate times
  in FTCAudit
      { intervalStart = a
      , intervalEnd = b
      , stateStart = State s0
      , stateEnd = State s1
      , endpointDifference = Accumulation endpoint
      , accumulatedRate = Accumulation acc
      , residual = Residual (endpoint - acc)
      , method = "trapezoidal approximation"
      }

main :: IO ()
main = do
  let times = map Time [0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0]
  print (audit times)
