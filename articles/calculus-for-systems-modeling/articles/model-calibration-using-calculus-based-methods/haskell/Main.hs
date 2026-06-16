module Main where

data CalibrationRecord = CalibrationRecord
  { parameterName :: String
  , estimatedValue :: Double
  , lowerBound :: Double
  , upperBound :: Double
  , calibrationRole :: String
  , diagnosticWarning :: String
  } deriving (Show)

records :: [CalibrationRecord]
records =
  [ CalibrationRecord "growth_rate" 0.34 0.22 0.42 "estimated_by_grid_search" "Growth-rate estimates depend on data, loss function, and tested range."
  , CalibrationRecord "carrying_capacity" 105.0 85.0 125.0 "estimated_by_grid_search" "Capacity estimates should be reviewed with residuals and sensitivity."
  , CalibrationRecord "initial_value" 10.0 10.0 10.0 "fixed_from_initial_observation" "Fixed parameters should still be documented."
  , CalibrationRecord "loss_function" 0.0 0.0 0.0 "sum_of_squared_residuals" "Loss-function choice affects calibration interpretation."
  ]

main :: IO ()
main = mapM_ print records
