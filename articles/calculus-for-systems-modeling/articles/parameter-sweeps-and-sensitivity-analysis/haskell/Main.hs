module Main where

data SensitivityRecord = SensitivityRecord
  { parameterName :: String
  , baselineValue :: Double
  , testedRange :: String
  , sensitivityType :: String
  , outputMetric :: String
  , interpretationWarning :: String
  } deriving (Show)

records :: [SensitivityRecord]
records =
  [ SensitivityRecord "growth_rate" 0.35 "0.18 to 0.55" "grid_sweep_and_local_sensitivity" "final_state_value" "Growth-rate sensitivity depends on time horizon and baseline assumptions."
  , SensitivityRecord "carrying_capacity" 100.0 "80 to 150" "grid_sweep_and_local_sensitivity" "final_state_value" "Capacity sensitivity should not be generalized beyond the tested range."
  , SensitivityRecord "initial_value" 10.0 "context-dependent" "scenario_sensitivity" "trajectory_shape" "Initial conditions can affect transient behavior and threshold crossing."
  , SensitivityRecord "solver_settings" 0.0 "method-dependent" "computational_sensitivity" "numerical_result" "Sensitivity results should be checked against numerical reliability diagnostics."
  ]

main :: IO ()
main = mapM_ print records
