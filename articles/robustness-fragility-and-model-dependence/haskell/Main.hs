{-# OPTIONS_GHC -Wall #-}

module Main where

data DependenceLayer
  = ParameterDependence
  | StructuralDependence
  | ScenarioDependence
  | ThresholdFragility
  | DataDependence
  | MetricDependence
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresStressTest
  | RequiresComparison
  | Revise
  deriving (Eq, Show)

data RobustnessRecord = RobustnessRecord
  { key :: String
  , layer :: DependenceLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

robustnessRegister :: [RobustnessRecord]
robustnessRegister =
  [ RobustnessRecord
      "parameter_dependence"
      ParameterDependence
      "Reviews whether conclusions depend on parameter ranges."
      "Do parameter changes reverse the conclusion?"
      RequiresReview
  , RobustnessRecord
      "structural_dependence"
      StructuralDependence
      "Compares alternative mathematical structures."
      "Do plausible model forms disagree?"
      RequiresComparison
  , RobustnessRecord
      "scenario_dependence"
      ScenarioDependence
      "Reviews whether conclusions depend on future assumptions."
      "Does the recommendation hold under stress?"
      RequiresStressTest
  , RobustnessRecord
      "threshold_fragility"
      ThresholdFragility
      "Measures whether small changes reverse action."
      "How close is the output to decision reversal?"
      RequiresReview
  , RobustnessRecord
      "data_dependence"
      DataDependence
      "Reviews sensitivity to calibration windows and samples."
      "Does evidence transfer responsibly?"
      RequiresReview
  ]

needsReview :: RobustnessRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed robustness records:"
  mapM_ print robustnessRegister

  putStrLn "\nRobustness records requiring review:"
  mapM_ print (filter needsReview robustnessRegister)
