module Main where

newtype TermCount = TermCount Int deriving (Show)
newtype PartialSum = PartialSum Double deriving (Show)
newtype LastTerm = LastTerm Double deriving (Show)
newtype EstimatedError = EstimatedError Double deriving (Show)

data TestResult
  = Converges
  | Diverges
  | Inconclusive
  | Conditional
  deriving (Show)

data ConvergenceTestAudit = ConvergenceTestAudit
  { seriesName :: String
  , testUsed :: String
  , nTerms :: TermCount
  , partialSum :: PartialSum
  , lastTerm :: LastTerm
  , testResult :: TestResult
  , estimatedError :: Maybe EstimatedError
  , stoppingRule :: String
  , warning :: String
  } deriving (Show)

geometricTerms :: Double -> Double -> Int -> [Double]
geometricTerms a r nTerms =
  [a * (r ** fromIntegral n) | n <- [0..(nTerms - 1)]]

pSeriesTerms :: Double -> Int -> [Double]
pSeriesTerms p nTerms =
  [1.0 / (fromIntegral n ** p) | n <- [1..nTerms]]

auditGeometric :: Double -> Double -> Int -> ConvergenceTestAudit
auditGeometric a r nTerms =
  let terms = geometricTerms a r nTerms
      partial = sum terms
      lastValue = last terms
  in if abs r < 1
     then
       let reference = a / (1 - r)
       in ConvergenceTestAudit
          { seriesName = "geometric"
          , testUsed = "geometric-series test"
          , nTerms = TermCount nTerms
          , partialSum = PartialSum partial
          , lastTerm = LastTerm lastValue
          , testResult = Converges
          , estimatedError = Just (EstimatedError (reference - partial))
          , stoppingRule = "fixed term count with geometric tail check"
          , warning = ""
          }
     else
       ConvergenceTestAudit
          { seriesName = "geometric"
          , testUsed = "geometric-series test"
          , nTerms = TermCount nTerms
          , partialSum = PartialSum partial
          , lastTerm = LastTerm lastValue
          , testResult = Diverges
          , estimatedError = Nothing
          , stoppingRule = "fixed term count; no finite infinite-total claim"
          , warning = "ratio magnitude is not below one"
          }

auditPSeries :: Double -> Int -> ConvergenceTestAudit
auditPSeries p nTerms =
  let terms = pSeriesTerms p nTerms
      result = if p > 1 then Converges else Diverges
      note = if p > 1 then "" else "p-series diverges for p less than or equal to one"
  in ConvergenceTestAudit
      { seriesName = "p-series"
      , testUsed = "p-series test"
      , nTerms = TermCount nTerms
      , partialSum = PartialSum (sum terms)
      , lastTerm = LastTerm (last terms)
      , testResult = result
      , estimatedError = Nothing
      , stoppingRule = "fixed term count with p-series classification"
      , warning = note
      }

main :: IO ()
main = do
  print (auditGeometric 10.0 0.6 25)
  print (auditGeometric 10.0 1.05 25)
  print (auditPSeries 1.25 10000)
  print (auditPSeries 0.75 10000)
