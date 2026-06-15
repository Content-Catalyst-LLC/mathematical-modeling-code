module Main where

newtype Center = Center Double deriving (Show)
newtype XValue = XValue Double deriving (Show)
newtype TermCount = TermCount Int deriving (Show)
newtype PartialSum = PartialSum Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)

data ConvergenceStatus
  = InsideRadius
  | OutsideRadius
  deriving (Show)

data PowerSeriesAudit = PowerSeriesAudit
  { functionName :: String
  , center :: Center
  , xValue :: XValue
  , nTerms :: TermCount
  , partialSum :: PartialSum
  , referenceValue :: Maybe Double
  , absoluteError :: Maybe AbsoluteError
  , convergenceStatus :: ConvergenceStatus
  , warning :: String
  } deriving (Show)

geometricPowerSeries :: Double -> Int -> Double
geometricPowerSeries x termCount =
  sum [x ** fromIntegral n | n <- [0..(termCount - 1)]]

auditGeometric :: Double -> Int -> PowerSeriesAudit
auditGeometric x termCount =
  let partial = geometricPowerSeries x termCount
      converges = abs x < 1
      reference = if converges then Just (1.0 / (1.0 - x)) else Nothing
      err = fmap (\ref -> AbsoluteError (abs (ref - partial))) reference
  in PowerSeriesAudit
      { functionName = "1/(1-x)"
      , center = Center 0.0
      , xValue = XValue x
      , nTerms = TermCount termCount
      , partialSum = PartialSum partial
      , referenceValue = reference
      , absoluteError = err
      , convergenceStatus = if converges then InsideRadius else OutsideRadius
      , warning = if converges then "" else "Power series does not converge for this x value."
      }

main :: IO ()
main = do
  print (auditGeometric 0.25 5)
  print (auditGeometric 0.25 10)
  print (auditGeometric 0.75 20)
  print (auditGeometric 1.25 10)
