module Main where

data EigenstructureAudit = EigenstructureAudit
  { systemName :: String
  , matrixEntries :: String
  , traceValue :: Double
  , determinantValue :: Double
  , eigenvalueOne :: Double
  , eigenvalueTwo :: Double
  , spectralRadius :: Double
  , dominantEigenvalue :: Double
  , stabilityClassification :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: EigenstructureAudit
buildAudit =
  EigenstructureAudit
    "two_sector_mode_audit"
    "0.820000,0.120000;0.180000,0.760000"
    1.58
    0.6016
    0.94
    0.64
    0.94
    0.94
    "asymptotically_damped_discrete_time"
    "Eigenvalues describe modes of the specified matrix; interpretation depends on construction, units, scaling, and domain meaning."

main :: IO ()
main =
  print buildAudit
