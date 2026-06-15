module Main where

newtype Cutoff = Cutoff Double deriving (Show)
newtype TruncatedValue = TruncatedValue Double deriving (Show)
newtype ReferenceValue = ReferenceValue Double deriving (Show)
newtype TailError = TailError Double deriving (Show)

data ImproperIntegralAudit = ImproperIntegralAudit
  { cutoff :: Cutoff
  , truncatedValue :: TruncatedValue
  , referenceValue :: ReferenceValue
  , tailError :: TailError
  , method :: String
  , interpretation :: String
  } deriving (Show)

f :: Double -> Double
f x = exp (-0.4 * x)

reference :: Double
reference = 1.0 / 0.4

trap :: Double -> Double -> Int -> Double
trap a b n =
  let dx = (b-a) / fromIntegral n
      xs = [a + dx * fromIntegral i | i <- [0..n]]
      pairs = zip xs (tail xs)
      step (x0,x1) = 0.5 * (f x0 + f x1) * (x1-x0)
  in sum (map step pairs)

audit :: Double -> ImproperIntegralAudit
audit c =
  let truncated = trap 0.0 c 4000
      err = reference - truncated
  in ImproperIntegralAudit
      { cutoff = Cutoff c
      , truncatedValue = TruncatedValue truncated
      , referenceValue = ReferenceValue reference
      , tailError = TailError err
      , method = "trapezoidal truncation audit"
      , interpretation = "exponential decay produces finite infinite-horizon accumulation"
      }

main :: IO ()
main = mapM_ print (map audit [2.0,4.0,8.0,12.0,20.0])
