module Main where

newtype Time = Time Double deriving (Show)
newtype Rate = Rate Double deriving (Show)
newtype Accumulation = Accumulation Double deriving (Show)

data IntegralAudit = IntegralAudit
  { intervalStart :: Time
  , intervalEnd :: Time
  , signedAccumulation :: Accumulation
  , absoluteAccumulation :: Accumulation
  , method :: String
  , interpretation :: String
  } deriving (Show)

netRate :: Time -> Rate
netRate (Time t) =
  Rate (4.0 * sin (t / 2.0) + 1.0)

trapStep :: Time -> Time -> (Rate -> Double) -> Double
trapStep a@(Time t0) b@(Time t1) transform =
  let dt = t1 - t0
      r0 = transform (netRate a)
      r1 = transform (netRate b)
  in 0.5 * (r0 + r1) * dt

signedValue :: Rate -> Double
signedValue (Rate r) = r

absoluteValue :: Rate -> Double
absoluteValue (Rate r) = abs r

integrate :: [Time] -> (Rate -> Double) -> Accumulation
integrate [] _ = Accumulation 0.0
integrate [_] _ = Accumulation 0.0
integrate times transform =
  let pairs = zip times (tail times)
      total = sum [trapStep a b transform | (a,b) <- pairs]
  in Accumulation total

audit :: [Time] -> IntegralAudit
audit times =
  IntegralAudit
    { intervalStart = head times
    , intervalEnd = last times
    , signedAccumulation = integrate times signedValue
    , absoluteAccumulation = integrate times absoluteValue
    , method = "trapezoidal approximation"
    , interpretation = "signed accumulation estimates net change; absolute accumulation estimates total activity"
    }

main :: IO ()
main = do
  let times = map Time [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]
  print (audit times)
