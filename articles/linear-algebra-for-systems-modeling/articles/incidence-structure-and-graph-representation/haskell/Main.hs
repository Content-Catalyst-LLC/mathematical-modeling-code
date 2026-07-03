module Main where

data IncidenceStructureAudit = IncidenceStructureAudit
  { graphName :: String
  , nodeCount :: Int
  , edgeCount :: Int
  , directedConvention :: String
  , signedIncidence :: Bool
  , nonzeroIncidenceEntries :: Int
  , incidenceDensity :: Double
  , maxAbsoluteNodeBalance :: Double
  , laplacianTrace :: Double
  , rankEstimate :: Int
  , representationWarning :: String
  } deriving (Show)

buildAudit :: IncidenceStructureAudit
buildAudit =
  IncidenceStructureAudit
    "synthetic_infrastructure_incidence_graph"
    4
    5
    "B[v,e] = -1 at source/tail and +1 at target/head."
    True
    10
    0.5
    9.0
    10.0
    3
    "Incidence structure depends on node definitions, edge definitions, sign convention, edge direction, weight semantics, data provenance, and conservation assumptions."

main :: IO ()
main =
  print buildAudit
