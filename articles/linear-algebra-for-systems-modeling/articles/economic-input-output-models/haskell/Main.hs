module Main where

data InputOutputAudit = InputOutputAudit
  { modelName :: String
  , sectors :: Int
  , method :: String
  , coefficientBasis :: String
  , conditionNumber :: Double
  , maximumOutputMultiplier :: Double
  , highestMultiplierSector :: String
  , totalBaselineOutput :: Double
  , totalShockOutputChange :: Double
  , totalEmissionsForFinalDemand :: Double
  , assumptionWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: InputOutputAudit
buildAudit =
  InputOutputAudit
    "synthetic_economic_input_output_audit"
    4
    "demand_driven_leontief_input_output_system"
    "sector_input_per_unit_output"
    2.41
    1.47
    "manufacturing"
    319.8
    36.2
    150.6
    "The model assumes fixed technical coefficients, proportional production, no price response, no substitution, and no binding capacity constraints."
    "Input-output multipliers are model-derived dependency estimates, not automatic causal proof."

main :: IO ()
main =
  print buildAudit
