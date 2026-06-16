module Main where

data NumericalAuditRecord = NumericalAuditRecord
  { stepSize :: Double
  , solverMethod :: String
  , diagnosticType :: String
  , diagnosticResult :: String
  , interpretationWarning :: String
  } deriving (Show)

records :: [NumericalAuditRecord]
records =
  [ NumericalAuditRecord 1.0 "fixed_step_rk4" "step_size_refinement" "baseline coarse step" "Coarse numerical outputs should not be treated as verified."
  , NumericalAuditRecord 0.5 "fixed_step_rk4" "step_size_refinement" "refined comparison" "Refinement tests numerical behavior, not empirical validity."
  , NumericalAuditRecord 0.25 "fixed_step_rk4" "convergence_review" "additional refinement" "Convergence should be documented with assumptions and solver settings."
  , NumericalAuditRecord 0.125 "fixed_step_rk4" "diagnostic_review" "fine refinement" "Numerical confidence remains separate from model validity."
  ]

main :: IO ()
main = mapM_ print records
