module Main where

data PageRankAudit = PageRankAudit
  { graphName :: String
  , nodeCount :: Int
  , edgeCount :: Int
  , dampingFactor :: Double
  , tolerance :: Double
  , iterations :: Int
  , converged :: Bool
  , maxRankNode :: String
  , maxRankScore :: Double
  , minRankNode :: String
  , minRankScore :: Double
  , rankSum :: Double
  , danglingNodeCount :: Int
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: PageRankAudit
buildAudit =
  PageRankAudit
    "synthetic_directed_network_influence_model"
    5
    8
    0.85
    1.0e-10
    42
    True
    "power"
    0.246
    "transport"
    0.144
    1.0
    0
    "PageRank scores depend on node definitions, directed-edge meaning, transition normalization, dangling-node handling, damping factor, teleportation vector, convergence tolerance, graph boundary, and data provenance."

main :: IO ()
main =
  print buildAudit
