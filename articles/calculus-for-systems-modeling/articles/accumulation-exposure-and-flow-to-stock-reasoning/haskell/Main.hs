module Main where

newtype Duration = Duration Double deriving (Show)
newtype Flow = Flow Double deriving (Show)
newtype Stock = Stock Double deriving (Show)
newtype ExposureIntensity = ExposureIntensity Double deriving (Show)
newtype Exposure = Exposure Double deriving (Show)
newtype PopulationWeight = PopulationWeight Double deriving (Show)

data FlowRecord = FlowRecord
  { duration :: Duration
  , inflow :: Flow
  , outflow :: Flow
  , exposureIntensity :: ExposureIntensity
  , populationWeight :: PopulationWeight
  } deriving (Show)

data StockExposureAudit = StockExposureAudit
  { initialStock :: Stock
  , cumulativeInflow :: Stock
  , cumulativeOutflow :: Stock
  , netAccumulation :: Stock
  , endingStock :: Stock
  , cumulativeExposure :: Exposure
  , populationWeightedExposure :: Double
  , grossActivity :: Double
  } deriving (Show)

records :: [FlowRecord]
records =
  [ FlowRecord (Duration 1.0) (Flow 12.0) (Flow 6.0) (ExposureIntensity 20.0) (PopulationWeight 1000.0)
  , FlowRecord (Duration 1.0) (Flow 10.0) (Flow 7.0) (ExposureIntensity 18.0) (PopulationWeight 1100.0)
  , FlowRecord (Duration 1.0) (Flow 9.0)  (Flow 8.0) (ExposureIntensity 15.0) (PopulationWeight 1050.0)
  , FlowRecord (Duration 1.0) (Flow 8.0)  (Flow 9.0) (ExposureIntensity 13.0) (PopulationWeight 980.0)
  , FlowRecord (Duration 1.0) (Flow 7.0)  (Flow 9.0) (ExposureIntensity 11.0) (PopulationWeight 960.0)
  ]

stockContribution :: FlowRecord -> (Double, Double)
stockContribution row =
  let Duration dt = duration row
      Flow i = inflow row
      Flow o = outflow row
  in (i * dt, o * dt)

exposureContribution :: FlowRecord -> (Double, Double)
exposureContribution row =
  let Duration dt = duration row
      ExposureIntensity c = exposureIntensity row
      PopulationWeight p = populationWeight row
  in (c * dt, c * p * dt)

audit :: Stock -> [FlowRecord] -> StockExposureAudit
audit (Stock initial) rows =
  let inflows = map (fst . stockContribution) rows
      outflows = map (snd . stockContribution) rows
      exposures = map (fst . exposureContribution) rows
      popExposures = map (snd . exposureContribution) rows
      cumulativeIn = sum inflows
      cumulativeOut = sum outflows
      net = cumulativeIn - cumulativeOut
      gross = cumulativeIn + cumulativeOut
  in StockExposureAudit
      { initialStock = Stock initial
      , cumulativeInflow = Stock cumulativeIn
      , cumulativeOutflow = Stock cumulativeOut
      , netAccumulation = Stock net
      , endingStock = Stock (initial + net)
      , cumulativeExposure = Exposure (sum exposures)
      , populationWeightedExposure = sum popExposures
      , grossActivity = gross
      }

main :: IO ()
main = print (audit (Stock 50.0) records)
