module Main where

data StateSpaceGeometryAudit = StateSpaceGeometryAudit
  { systemName :: String
  , stateA :: String
  , stateB :: String
  , differenceVector :: String
  , dotProduct :: Double
  , cosineSimilarity :: Double
  , weightedInnerProduct :: Double
  , normOne :: Double
  , normTwo :: Double
  , normInfinity :: Double
  , euclideanDistance :: Double
  , weightedDistance :: Double
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: StateSpaceGeometryAudit
buildAudit =
  StateSpaceGeometryAudit
    "three_indicator_state_space_geometry_audit"
    "12.000000,4.000000,0.800000"
    "10.000000,5.500000,1.100000"
    "2.000000,-1.500000,-0.300000"
    142.88
    0.988725
    133.04
    3.8
    2.517936
    2.0
    2.517936
    2.33538
    "Distance depends on units, scaling, norm choice, and weights; weighted geometry requires domain justification."

main :: IO ()
main =
  print buildAudit
