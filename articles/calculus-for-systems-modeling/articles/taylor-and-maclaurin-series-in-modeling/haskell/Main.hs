module Main where

newtype Center = Center Double deriving (Show)
newtype XValue = XValue Double deriving (Show)
newtype Order = Order Int deriving (Show)
newtype Approximation = Approximation Double deriving (Show)
newtype ReferenceValue = ReferenceValue Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)

data TaylorAudit = TaylorAudit
  { functionName :: String
  , center :: Center
  , xValue :: XValue
  , orderValue :: Order
  , approximation :: Approximation
  , referenceValue :: ReferenceValue
  , absoluteError :: AbsoluteError
  , warning :: String
  } deriving (Show)

factorial :: Int -> Double
factorial n = product [1.0..fromIntegral n]

taylorExpMaclaurin :: Double -> Int -> Double
taylorExpMaclaurin x n =
  sum [(x ** fromIntegral k) / factorial k | k <- [0..n]]

auditExp :: Double -> Int -> TaylorAudit
auditExp x n =
  let approx = taylorExpMaclaurin x n
      reference = exp x
      warn = if abs x <= 2 then "" else "Evaluation is far from the Maclaurin center; review truncation error carefully."
  in TaylorAudit
      { functionName = "exp(x)"
      , center = Center 0.0
      , xValue = XValue x
      , orderValue = Order n
      , approximation = Approximation approx
      , referenceValue = ReferenceValue reference
      , absoluteError = AbsoluteError (abs (reference - approx))
      , warning = warn
      }

main :: IO ()
main = do
  print (auditExp 0.5 2)
  print (auditExp 0.5 5)
  print (auditExp 1.0 10)
  print (auditExp 3.0 10)
