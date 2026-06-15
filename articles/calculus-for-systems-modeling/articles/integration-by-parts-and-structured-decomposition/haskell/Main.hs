module Main where

newtype X = X Double deriving (Show)
newtype DirectIntegral = DirectIntegral Double deriving (Show)
newtype BoundaryTerm = BoundaryTerm Double deriving (Show)
newtype ResidualIntegral = ResidualIntegral Double deriving (Show)
newtype DecompositionResidual = DecompositionResidual Double deriving (Show)

data IntegrationByPartsAudit = IntegrationByPartsAudit
  { intervalStart :: X
  , intervalEnd :: X
  , directIntegral :: DirectIntegral
  , boundaryTerm :: BoundaryTerm
  , residualIntegral :: ResidualIntegral
  , decompositionResidual :: DecompositionResidual
  , method :: String
  } deriving (Show)

u :: X -> Double
u (X x) = 1.0 + x

uPrime :: X -> Double
uPrime _ = 1.0

v :: X -> Double
v (X x) = exp (-0.3 * x) * sin x

vPrime :: X -> Double
vPrime (X x) = exp (-0.3 * x) * (cos x - 0.3 * sin x)

grid :: Double -> Double -> Int -> [Double]
grid a b n = [a + (b-a) * fromIntegral i / fromIntegral n | i <- [0..n]]

trap :: [Double] -> [Double] -> Double
trap values points =
  let pairs = zip3 values (tail values) (zip points (tail points))
      step (y0, y1, (x0, x1)) = 0.5 * (y0 + y1) * (x1 - x0)
  in sum (map step pairs)

audit :: Double -> Double -> Int -> IntegrationByPartsAudit
audit a b n =
  let xs = grid a b n
      direct = trap [u (X x) * vPrime (X x) | x <- xs] xs
      residual = trap [v (X x) * uPrime (X x) | x <- xs] xs
      boundary = u (X b) * v (X b) - u (X a) * v (X a)
      decomposed = boundary - residual
  in IntegrationByPartsAudit
      { intervalStart = X a
      , intervalEnd = X b
      , directIntegral = DirectIntegral direct
      , boundaryTerm = BoundaryTerm boundary
      , residualIntegral = ResidualIntegral residual
      , decompositionResidual = DecompositionResidual (direct - decomposed)
      , method = "trapezoidal comparison"
      }

main :: IO ()
main = print (audit 0.0 4.0 800)
