module Main where

newtype XInput = XInput Double deriving (Show)
newtype YInput = YInput Double deriving (Show)
newtype DX = DX Double deriving (Show)
newtype DY = DY Double deriving (Show)
newtype Output = Output Double deriving (Show)
newtype DifferentialEstimate = DifferentialEstimate Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)

data Feasibility = Feasible | Infeasible deriving (Show)

data TotalDifferentialRecord = TotalDifferentialRecord
  { xInput :: XInput
  , yInput :: YInput
  , dxInput :: DX
  , dyInput :: DY
  , baselineOutput :: Output
  , actualOutput :: Output
  , actualChange :: Output
  , differentialEstimate :: DifferentialEstimate
  , absoluteError :: AbsoluteError
  , feasibility :: Feasibility
  , warning :: String
  } deriving (Show)

f :: Double -> Double -> Double
f x y = 3.0 * x + 2.0 * y + 0.5 * x * y

fx :: Double -> Double -> Double
fx _x y = 3.0 + 0.5 * y

fy :: Double -> Double -> Double
fy x _y = 2.0 + 0.5 * x

totalDifferential :: Double -> Double -> Double -> Double -> Double
totalDifferential x y dx dy = fx x y * dx + fy x y * dy

isFeasible :: Double -> Double -> Double -> Double -> Bool
isFeasible x y dx dy =
  x >= 0 && y >= 0 && x + y <= 10 &&
  x + dx >= 0 && y + dy >= 0 && x + dx + y + dy <= 10

auditCase :: Double -> Double -> Double -> Double -> TotalDifferentialRecord
auditCase x y dx dy =
  let baseline = f x y
      actual = f (x + dx) (y + dy)
      change = actual - baseline
      estimate = totalDifferential x y dx dy
      errorValue = abs (change - estimate)
      feasible = isFeasible x y dx dy
  in TotalDifferentialRecord
      (XInput x)
      (YInput y)
      (DX dx)
      (DY dy)
      (Output baseline)
      (Output actual)
      (Output change)
      (DifferentialEstimate estimate)
      (AbsoluteError errorValue)
      (if feasible then Feasible else Infeasible)
      (if feasible then "" else "Displacement is outside the feasible region.")

main :: IO ()
main = do
  print (auditCase 4.0 3.0 0.2 (-0.1))
  print (auditCase 4.0 3.0 1.0 1.0)
  print (auditCase 8.0 1.0 1.0 1.0)
