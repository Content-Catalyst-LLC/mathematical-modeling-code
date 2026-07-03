module Main where

data CompressionNoiseAudit = CompressionNoiseAudit
  { modelName :: String
  , rows :: Int
  , columns :: Int
  , method :: String
  , preprocessing :: String
  , retainedRank :: Int
  , retainedEnergyRatio :: Double
  , discardedEnergyRatio :: Double
  , compressionRatio :: Double
  , relativeReconstructionError :: Double
  , maximumRowResidual :: Double
  , highestResidualRow :: Int
  , noiseWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: CompressionNoiseAudit
buildAudit =
  CompressionNoiseAudit
    "synthetic_compression_noise_audit"
    9
    6
    "svd_low_rank_compression"
    "centered_and_standardized"
    2
    0.962
    0.038
    1.6875
    0.195
    1.43
    8
    "Discarded components are not automatically noise; they may contain weak signals, localized structure, subgroup patterns, anomalies, or early warning behavior."
    "Compression preserves selected structure while losing or distorting other information."

main :: IO ()
main =
  print buildAudit
