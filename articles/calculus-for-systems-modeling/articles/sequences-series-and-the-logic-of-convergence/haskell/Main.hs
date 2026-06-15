module Main where

newtype TermCount = TermCount Int deriving (Show)
newtype PartialSum = PartialSum Double deriving (Show)
newtype LastTerm = LastTerm Double deriving (Show)
newtype ReferenceValue = ReferenceValue Double deriving (Show)
newtype EstimatedError = EstimatedError Double deriving (Show)

data SeriesAudit = SeriesAudit
  { seriesName :: String
  , nTerms :: TermCount
  , lastTerm :: LastTerm
  , partialSum :: PartialSum
  , referenceValue :: Maybe ReferenceValue
  , estimatedError :: Maybe EstimatedError
  , classification :: String
  , warning :: String
  } deriving (Show)

geometricTerms :: Double -> Double -> Int -> [Double]
geometricTerms a r nTerms = [a * (r ** fromIntegral n) | n <- [0..(nTerms - 1)]]

harmonicTerms :: Int -> [Double]
harmonicTerms nTerms = [1.0 / fromIntegral n | n <- [1..nTerms]]

auditGeometric :: Double -> Double -> Int -> SeriesAudit
auditGeometric a r nTerms =
  let terms = geometricTerms a r nTerms
      partial = sum terms
      lastValue = last terms
  in if abs r < 1
     then
       let reference = a / (1 - r)
           err = reference - partial
       in SeriesAudit
          { seriesName = "geometric"
          , nTerms = TermCount nTerms
          , lastTerm = LastTerm lastValue
          , partialSum = PartialSum partial
          , referenceValue = Just (ReferenceValue reference)
          , estimatedError = Just (EstimatedError err)
          , classification = "convergent geometric series"
          , warning = ""
          }
     else
       SeriesAudit
          { seriesName = "geometric"
          , nTerms = TermCount nTerms
          , lastTerm = LastTerm lastValue
          , partialSum = PartialSum partial
          , referenceValue = Nothing
          , estimatedError = Nothing
          , classification = "divergent or inconclusive"
          , warning = "geometric ratio does not support convergence"
          }

auditHarmonic :: Int -> SeriesAudit
auditHarmonic nTerms =
  let terms = harmonicTerms nTerms
  in SeriesAudit
      { seriesName = "harmonic"
      , nTerms = TermCount nTerms
      , lastTerm = LastTerm (last terms)
      , partialSum = PartialSum (sum terms)
      , referenceValue = Nothing
      , estimatedError = Nothing
      , classification = "divergent despite terms approaching zero"
      , warning = "small last term does not imply finite accumulated total"
      }

main :: IO ()
main = do
  print (auditGeometric 10.0 0.6 25)
  print (auditGeometric 10.0 1.05 25)
  print (auditHarmonic 10000)
