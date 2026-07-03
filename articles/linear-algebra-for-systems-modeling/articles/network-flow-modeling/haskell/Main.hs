module Main where

data NetworkFlowAudit = NetworkFlowAudit
  { graphName :: String
  , nodeCount :: Int
  , edgeCount :: Int
  , sourceNode :: String
  , sinkNode :: String
  , totalSourceOutflow :: Double
  , totalSinkInflow :: Double
  , capacityViolations :: Int
  , saturatedEdgeCount :: Int
  , maxAbsoluteTransshipmentImbalance :: Double
  , totalFlowCost :: Double
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: NetworkFlowAudit
buildAudit =
  NetworkFlowAudit
    "synthetic_capacitated_flow_network"
    5
    6
    "source"
    "sink"
    16.0
    16.0
    0
    2
    0.0
    82.0
    "Network flow results depend on node definitions, edge definitions, capacity units, flow units, cost semantics, source-sink choices, conservation assumptions, time scale, solver settings, uncertainty, and data provenance."

main :: IO ()
main =
  print buildAudit
