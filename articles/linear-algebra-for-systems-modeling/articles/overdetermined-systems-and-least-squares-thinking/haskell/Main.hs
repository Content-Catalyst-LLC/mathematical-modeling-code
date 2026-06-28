module Main where

data LeastSquaresAudit = LeastSquaresAudit
  { systemName :: String
  , rowCount :: Int
  , columnCount :: Int
  , overdetermined :: Bool
  , rankValue :: Int
  , solution :: String
  , fittedValues :: String
  , residuals :: String
  , residualNorm :: Double
  , solverMethod :: String
  , interpretationWarning :: String
  } deriving (Show)

buildAudit :: LeastSquaresAudit
buildAudit =
  LeastSquaresAudit
    "four_observation_linear_calibration"
    4
    2
    True
    2
    "0.850000,1.040000"
    "1.890000,2.930000,3.970000,5.010000"
    "0.110000,-0.030000,0.130000,0.090000"
    0.191311
    "normal equations teaching record; QR or SVD preferred for robust workflows"
    "Least squares minimizes residuals, but residual meaning depends on model purpose."

main :: IO ()
main =
  print buildAudit
