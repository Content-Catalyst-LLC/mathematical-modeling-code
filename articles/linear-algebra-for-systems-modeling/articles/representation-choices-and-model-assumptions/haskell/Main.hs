module Main where

data RepresentationAssumptionAudit = RepresentationAssumptionAudit
  { workflowName :: String
  , matrixShape :: String
  , rowMeaning :: String
  , columnMeaning :: String
  , valueMeaning :: String
  , zeroMeaning :: String
  , missingValueRule :: String
  , rawColumnNorm1 :: Double
  , rawColumnNorm2 :: Double
  , standardizedColumnNorm1 :: Double
  , standardizedColumnNorm2 :: Double
  , representationChangeWarning :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: RepresentationAssumptionAudit
buildAudit =
  RepresentationAssumptionAudit
    "representation_assumption_audit"
    "3x2"
    "infrastructure_zones"
    "annual_demand_and_outage_exposure"
    "mixed_units_before_standardization"
    "zero_would_mean_measured_absence_not_missingness"
    "missing_values_must_not_be_encoded_as_zero_without_flag"
    2345.21
    0.1749
    1.4142
    1.4142
    "Standardization improves comparability but changes interpretation from original units to relative position."
    "Representation choices define what the model can compare, reveal, and hide. Rows, columns, units, zeros, scaling, missingness, and boundaries should be documented before computation."

main :: IO ()
main =
  print buildAudit
