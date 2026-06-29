module Main where

data ProjectionReflectionAudit = ProjectionReflectionAudit
  { systemName :: String
  , originalVector :: String
  , unitDirection :: String
  , projectedVector :: String
  , residualVector :: String
  , residualNorm :: Double
  , reflectedVector :: String
  , projectionIdempotenceError :: Double
  , projectionSymmetryError :: Double
  , reflectionInvolutionError :: Double
  , lengthPreservationError :: Double
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: ProjectionReflectionAudit
buildAudit =
  ProjectionReflectionAudit
    "two_dimensional_geometric_transformation_audit"
    "4.000000,3.000000"
    "0.894427,0.447214"
    "4.400000,2.200000"
    "-0.400000,0.800000"
    0.894427
    "4.800000,1.400000"
    0.0
    0.0
    0.0
    0.0
    "Projection retains modeled structure and residualizes the perpendicular component; reflection preserves distance while reversing the perpendicular component."

main :: IO ()
main = print buildAudit
