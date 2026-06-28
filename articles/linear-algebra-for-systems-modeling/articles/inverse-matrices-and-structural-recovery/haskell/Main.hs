module Main where
data InverseRecoveryAudit = InverseRecoveryAudit
  { systemName :: String, matrixSize :: Int, determinantValue :: Double,
    invertible :: Bool, rankValue :: Int, nullityValue :: Int,
    recoveredSolution :: String, residualNorm :: Double,
    tolerance :: Double, interpretationWarning :: String } deriving (Show)

main :: IO ()
main = print (InverseRecoveryAudit
  "three_constraint_structural_recovery_system" 3 2.0 True 3 0
  "55.000000,45.000000,35.000000" 0.0 1.0e-10
  "Inverse recovery is algebraic; practical recovery requires conditioning and model review.")
