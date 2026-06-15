module Main where

newtype Time = Time Double deriving (Show)
newtype Flow = Flow Double deriving (Show)
newtype Stock = Stock Double deriving (Show)

data RecoveryRecord = RecoveryRecord
  { time :: Time
  , netFlow :: Flow
  , recoveredStock :: Stock
  , method :: String
  , warning :: String
  } deriving (Show)

netFlowValue :: Time -> Flow
netFlowValue (Time t) =
  let inflow = 12.0 + 0.5 * t
      outflow = 7.0 + 0.2 * t
  in Flow (inflow - outflow)

trapStep :: Time -> Time -> Stock -> Stock
trapStep t0@(Time a) t1@(Time b) (Stock s) =
  let Flow r0 = netFlowValue t0
      Flow r1 = netFlowValue t1
      dt = b - a
      accumulated = 0.5 * (r0 + r1) * dt
  in Stock (s + accumulated)

recover :: [Time] -> Stock -> [RecoveryRecord]
recover [] _ = []
recover [_] _ = []
recover times initial =
  let firstRecord = RecoveryRecord
        { time = head times
        , netFlow = netFlowValue (head times)
        , recoveredStock = initial
        , method = "initial condition"
        , warning = "baseline determines recovered level"
        }
      step records [] = records
      step records [_] = records
      step records (a:b:rest) =
        let previousStock = recoveredStock (last records)
            newStock = trapStep a b previousStock
            record = RecoveryRecord
              { time = b
              , netFlow = netFlowValue b
              , recoveredStock = newStock
              , method = "trapezoidal accumulation"
              , warning = ""
              }
        in step (records ++ [record]) (b:rest)
  in step [firstRecord] times

main :: IO ()
main = do
  let times = map Time [0.0,1.0,2.0,3.0,4.0,5.0,6.0]
  mapM_ print (recover times (Stock 100.0))
