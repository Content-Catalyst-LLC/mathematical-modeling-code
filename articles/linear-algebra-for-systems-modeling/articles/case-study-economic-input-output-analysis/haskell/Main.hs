module Main where

data EconomicInputOutputAudit = EconomicInputOutputAudit
  { workflowName :: String
  , economyName :: String
  , sectorCount :: Int
  , finalDemandTotal :: Double
  , grossOutputTotal :: Double
  , highestMultiplierSector :: String
  , highestOutputMultiplier :: Double
  , shockSector :: String
  , shockAmount :: Double
  , grossOutputChangeTotal :: Double
  , conditionEstimate :: Double
  , solvabilityWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: EconomicInputOutputAudit
buildAudit =
  EconomicInputOutputAudit
    "economic_input_output_audit"
    "synthetic_three_sector_economy"
    3
    450.0
    763.099081201887
    "manufacturing"
    1.951825177111
    "manufacturing"
    25.0
    48.795629500869
    2.147504345667
    "The Leontief matrix must be invertible and checked for numerical stability and plausibility."
    "Input-output results depend on fixed coefficients, aggregation, domestic/import boundaries, price basis, final-demand assumptions, and capacity limits."

main :: IO ()
main =
  print buildAudit
