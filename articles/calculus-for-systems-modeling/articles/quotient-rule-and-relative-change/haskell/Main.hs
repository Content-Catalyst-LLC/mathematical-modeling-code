module Main where

newtype Time = Time Double deriving (Show)
newtype Numerator = Numerator Double deriving (Show)
newtype Denominator = Denominator Double deriving (Show)
newtype Ratio = Ratio Double deriving (Show)
newtype Rate = Rate Double deriving (Show)

data QuotientAudit = QuotientAudit
  { time :: Time
  , numerator :: Numerator
  , denominator :: Denominator
  , ratio :: Ratio
  , numeratorEffect :: Rate
  , denominatorEffect :: Rate
  , quotientDerivative :: Rate
  , warning :: String
  } deriving (Show)

resourceStock :: Time -> Double
resourceStock (Time t) = 1000.0 * exp (-0.01 * t)

resourceStockRate :: Time -> Double
resourceStockRate t = -0.01 * resourceStock t

population :: Time -> Double
population (Time t) = 100.0 * exp (0.02 * t)

populationRate :: Time -> Double
populationRate t = 0.02 * population t

quotientAudit :: Time -> QuotientAudit
quotientAudit t =
  let f = resourceStock t
      g = population t
      fp = resourceStockRate t
      gp = populationRate t
      ne = fp / g
      de = - (f * gp) / (g * g)
      q = f / g
      warningText = if abs g < 1.0 then "small denominator" else ""
  in QuotientAudit t (Numerator f) (Denominator g) (Ratio q) (Rate ne) (Rate de) (Rate (ne + de)) warningText

main :: IO ()
main = mapM_ (print . quotientAudit . Time) [0.0, 5.0, 10.0, 20.0, 40.0]
