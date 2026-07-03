module Main where

data InfrastructureNetworkAudit = InfrastructureNetworkAudit
  { networkName :: String
  , nodeCount :: Int
  , edgeCount :: Int
  , layerCount :: Int
  , criticalAssetCount :: Int
  , interdependencyEdgeCount :: Int
  , totalBaselineCapacity :: Double
  , disruptedAsset :: String
  , remainingCapacityAfterDisruption :: Double
  , capacityLossFraction :: Double
  , governanceWarning :: String
  } deriving (Show)

buildAudit :: InfrastructureNetworkAudit
buildAudit =
  InfrastructureNetworkAudit
    "synthetic_multilayer_infrastructure_network"
    6
    7
    6
    5
    3
    400.0
    "power_substation"
    160.0
    0.60
    "Infrastructure network results depend on asset definitions, edge definitions, layer boundaries, capacity units, dependency rules, hazard scenarios, operating conditions, data provenance, security constraints, and social vulnerability interpretation."

main :: IO ()
main =
  print buildAudit
