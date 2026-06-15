module ProductRule where

data ProductContribution = ProductContribution
  { factorA :: Double
  , factorB :: Double
  , derivativeA :: Double
  , derivativeB :: Double
  , contributionFromA :: Double
  , contributionFromB :: Double
  , totalDerivative :: Double
  } deriving (Show, Eq)

productRule :: Double -> Double -> Double -> Double -> ProductContribution
productRule a b da db =
  let ca = da * b
      cb = a * db
  in ProductContribution a b da db ca cb (ca + cb)

main :: IO ()
main = print (productRule 120.0 1.5 4.0 0.03)
