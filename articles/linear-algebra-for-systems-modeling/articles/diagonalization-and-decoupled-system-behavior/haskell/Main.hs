module Main where

data DiagonalizationAudit = DiagonalizationAudit
  { systemName :: String
  , matrixEntries :: String
  , eigenvectorMatrix :: String
  , diagonalMatrix :: String
  , reconstructionErrorFrobenius :: Double
  , spectralRadius :: Double
  , dominantEigenvalue :: Double
  , stabilityClassification :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: DiagonalizationAudit
buildAudit =
  DiagonalizationAudit
    "two_mode_diagonalization_audit"
    "0.796667,0.123333;0.246667,0.673333"
    "1.000000,1.000000;1.000000,-2.000000"
    "0.920000,0.000000;0.000000,0.550000"
    0.0
    0.92
    0.92
    "all_modes_decay_discrete_time"
    "Diagonalization decouples representation, not necessarily real-world independence; interpretation depends on matrix construction and diagnostics."

main :: IO ()
main =
  print buildAudit
