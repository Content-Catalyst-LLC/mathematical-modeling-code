module Main where

data State = State Double Double deriving (Show)
data Displacement = Displacement Double Double deriving (Show)
data Output = Output Double Double deriving (Show)
data Jacobian = Jacobian Double Double Double Double deriving (Show)

fModel :: State -> Output
fModel (State x y) = Output (x * x + y) (x * y + 3.0 * y)

jacobian :: State -> Jacobian
jacobian (State x y) = Jacobian (2.0 * x) 1.0 y (x + 3.0)

determinant :: Jacobian -> Double
determinant (Jacobian j11 j12 j21 j22) = j11 * j22 - j12 * j21

applyJacobian :: Jacobian -> Displacement -> Output
applyJacobian (Jacobian j11 j12 j21 j22) (Displacement dx dy) =
  Output (j11 * dx + j12 * dy) (j21 * dx + j22 * dy)

outputDifference :: Output -> Output -> Output
outputDifference (Output a b) (Output c d) = Output (a - c) (b - d)

errorNorm :: Output -> Output -> Double
errorNorm (Output a b) (Output c d) = sqrt ((a - c)^2 + (b - d)^2)

auditCase :: State -> Displacement -> String
auditCase state@(State x y) disp@(Displacement dx dy) =
  let j = jacobian state
      baseline = fModel state
      actual = fModel (State (x + dx) (y + dy))
      actualChange = outputDifference actual baseline
      approximateChange = applyJacobian j disp
      detValue = determinant j
      err = errorNorm actualChange approximateChange
      warning = if abs detValue > 1.0e-8 then "" else "Jacobian is singular or near singular."
  in show (state, disp, j, detValue, approximateChange, actualChange, err, warning)

main :: IO ()
main = do
  putStrLn (auditCase (State 2.0 1.0) (Displacement 0.1 (-0.05)))
  putStrLn (auditCase (State 2.0 1.0) (Displacement 0.5 0.5))
  putStrLn (auditCase (State 0.0 0.0) (Displacement 0.1 0.1))
