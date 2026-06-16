module Main where

data VisualizationRecord = VisualizationRecord
  { figureId :: String
  , visualType :: String
  , modelObject :: String
  , xAxis :: String
  , yAxis :: String
  , scaleNote :: String
  , uncertaintyNote :: String
  , interpretationWarning :: String
  } deriving (Show)

records :: [VisualizationRecord]
records =
  [ VisualizationRecord "logistic_growth_scenario_trajectories" "trajectory_plot" "logistic_solution" "time" "state value" "Linear axes; time horizon 0 to 20." "Scenario lines are parameter contrasts, not probability intervals." "The figure shows model-implied trajectories under selected assumptions, not empirical forecasts."
  , VisualizationRecord "phase_portrait_review" "phase_portrait" "two_state_dynamic_system" "state x" "state y" "State-space window should be documented." "Initial condition selection affects visible trajectories." "Phase portraits show local and geometric behavior, not automatic empirical validity."
  , VisualizationRecord "vector_field_review" "vector_field" "spatial_flow_field" "x coordinate" "y coordinate" "Arrow scaling should be documented." "Magnitude and direction can be visually distorted by normalization." "Vector fields require unit and boundary interpretation."
  ]

main :: IO ()
main = mapM_ print records
