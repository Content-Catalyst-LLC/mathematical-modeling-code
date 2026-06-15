module Main where

newtype X = X Double deriving (Show)
newtype U = U Double deriving (Show)
newtype Scale = Scale Double deriving (Show)
newtype Accumulation = Accumulation Double deriving (Show)

data SubstitutionAudit = SubstitutionAudit
  { originalStart :: X
  , originalEnd :: X
  , transformedStart :: U
  , transformedEnd :: U
  , directAccumulation :: Accumulation
  , transformedAccumulation :: Accumulation
  , residual :: Double
  , method :: String
  } deriving (Show)

g :: X -> U
g (X x) = U (x*x + 1.0)

gPrime :: X -> Scale
gPrime (X x) = Scale (2.0*x)

f :: U -> Double
f (U u) = sqrt u

integrandX :: X -> Double
integrandX x =
  let Scale s = gPrime x
  in f (g x) * s

trap :: [Double] -> [Double] -> Double
trap values points =
  let pairs = zip3 values (tail values) (zip points (tail points))
      step (v0, v1, (p0, p1)) = 0.5 * (v0 + v1) * (p1 - p0)
  in sum (map step pairs)

grid :: Double -> Double -> Int -> [Double]
grid a b n = [a + (b-a) * fromIntegral i / fromIntegral n | i <- [0..n]]

audit :: Double -> Double -> Int -> SubstitutionAudit
audit a b n =
  let xs = grid a b n
      direct = trap [integrandX (X x) | x <- xs] xs
      U ua = g (X a)
      U ub = g (X b)
      us = grid ua ub n
      transformed = trap [f (U u) | u <- us] us
  in SubstitutionAudit
      { originalStart = X a
      , originalEnd = X b
      , transformedStart = U ua
      , transformedEnd = U ub
      , directAccumulation = Accumulation direct
      , transformedAccumulation = Accumulation transformed
      , residual = direct - transformed
      , method = "trapezoidal comparison"
      }

main :: IO ()
main = print (audit 1.0 3.0 400)
