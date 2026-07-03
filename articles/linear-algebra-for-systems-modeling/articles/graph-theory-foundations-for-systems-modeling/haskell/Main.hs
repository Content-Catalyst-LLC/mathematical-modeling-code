module Main where

data GraphStructureAudit = GraphStructureAudit
  { graphName :: String
  , nodeCount :: Int
  , edgeCount :: Int
  , directed :: Bool
  , weighted :: Bool
  , componentCount :: Int
  , maxDegree :: Int
  , minDegree :: Int
  , averageDegree :: Double
  , hasCycle :: Bool
  , graphDensity :: Double
  , representationWarning :: String
  } deriving (Show)

buildAudit :: GraphStructureAudit
buildAudit =
  GraphStructureAudit
    "synthetic_infrastructure_graph_foundations"
    5
    6
    False
    True
    1
    3
    2
    2.4
    True
    0.6
    "Graph conclusions depend on node definitions, edge definitions, graph boundary, direction conventions, weight semantics, missing edges, time period, and data provenance."

main :: IO ()
main =
  print buildAudit
