module Main where

data LeontiefSystemAudit = LeontiefSystemAudit
  { modelName :: String
  , sectors :: Int
  , method :: String
  , coefficientBasis :: String
  , spectralRadius :: Double
  , conditionNumber :: Double
  , productiveSystemFlag :: Bool
  , maximumOutputMultiplier :: Double
  , highestMultiplierSector :: String
  , totalOutputRequired :: Double
  , totalShockOutputChange :: Double
  , emissionsForFinalDemand :: Double
  , assumptionWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: LeontiefSystemAudit
buildAudit =
  LeontiefSystemAudit
    "synthetic_leontief_intersectoral_dependence_audit"
    4
    "demand_driven_leontief_system"
    "sector_input_per_unit_output"
    0.331
    2.41
    True
    1.47
    "manufacturing"
    319.8
    36.2
    150.6
    "The Leontief model assumes fixed technical coefficients, proportional production, no price response, no substitution, and no binding capacity constraints."
    "The Leontief inverse gives structured dependency estimates under model assumptions, not automatic causal proof."

main :: IO ()
main =
  print buildAudit
