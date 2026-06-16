module Main where

data StiffnessRecord = StiffnessRecord
  { stepSize :: Double
  , eigenvalue :: Double
  , methodName :: String
  , diagnosticType :: String
  , stabilityStatus :: String
  , interpretationWarning :: String
  } deriving (Show)

records :: [StiffnessRecord]
records =
  [ StiffnessRecord 0.1 (-50.0) "explicit_euler" "amplification_factor_review" "unstable_for_test_problem" "Explicit methods may require very small steps on stiff systems."
  , StiffnessRecord 0.1 (-50.0) "implicit_euler" "amplification_factor_review" "stable_for_test_problem" "Implicit stability does not remove accuracy review."
  , StiffnessRecord 0.025 (-50.0) "explicit_euler" "step_size_refinement" "review_required" "A smaller explicit step may improve stability but increase runtime."
  , StiffnessRecord 0.025 (-50.0) "implicit_euler" "stiff_solver_review" "review_required" "Solver diagnostics should be preserved with stiff simulations."
  ]

main :: IO ()
main = mapM_ print records
