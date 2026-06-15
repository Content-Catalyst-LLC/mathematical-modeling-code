module Main where

newtype XInput = XInput Double deriving (Show)
newtype YInput = YInput Double deriving (Show)
newtype DirectionX = DirectionX Double deriving (Show)
newtype DirectionY = DirectionY Double deriving (Show)
newtype UnitX = UnitX Double deriving (Show)
newtype UnitY = UnitY Double deriving (Show)
newtype GradientX = GradientX Double deriving (Show)
newtype GradientY = GradientY Double deriving (Show)
newtype DirectionalDerivative = DirectionalDerivative Double deriving (Show)
newtype StepSize = StepSize Double deriving (Show)
newtype AbsoluteError = AbsoluteError Double deriving (Show)

data Feasibility = Feasible | Infeasible deriving (Show)

data DirectionalDerivativeRecord = DirectionalDerivativeRecord
  { xInput :: XInput
  , yInput :: YInput
  , directionX :: DirectionX
  , directionY :: DirectionY
  , unitX :: UnitX
  , unitY :: UnitY
  , gradientX :: GradientX
  , gradientY :: GradientY
  , derivativeValue :: DirectionalDerivative
  , stepSize :: StepSize
  , absoluteError :: AbsoluteError
  , feasibility :: Feasibility
  , warning :: String
  } deriving (Show)

f :: Double -> Double -> Double
f x y = 3.0 * x + 2.0 * y + 0.5 * x * y

gradient :: Double -> Double -> (Double, Double)
gradient x y = (3.0 + 0.5 * y, 2.0 + 0.5 * x)

normalize :: Double -> Double -> (Double, Double)
normalize vx vy =
  let normValue = sqrt (vx * vx + vy * vy)
  in if normValue == 0 then error "Direction vector must be nonzero." else (vx / normValue, vy / normValue)

directionalDerivative :: Double -> Double -> Double -> Double -> Double
directionalDerivative x y ux uy =
  let (gx, gy) = gradient x y
  in gx * ux + gy * uy

isFeasible :: Double -> Double -> Double -> Double -> Double -> Bool
isFeasible x y ux uy step =
  x >= 0 && y >= 0 && x + y <= 10 &&
  x + step * ux >= 0 && y + step * uy >= 0 &&
  x + step * ux + y + step * uy <= 10

auditDirection :: Double -> Double -> Double -> Double -> Double -> DirectionalDerivativeRecord
auditDirection x y vx vy step =
  let (ux, uy) = normalize vx vy
      (gx, gy) = gradient x y
      derivative = directionalDerivative x y ux uy
      baseline = f x y
      actual = f (x + step * ux) (y + step * uy)
      actualChange = actual - baseline
      estimatedChange = step * derivative
      errorValue = abs (actualChange - estimatedChange)
      feasible = isFeasible x y ux uy step
  in DirectionalDerivativeRecord
      (XInput x)
      (YInput y)
      (DirectionX vx)
      (DirectionY vy)
      (UnitX ux)
      (UnitY uy)
      (GradientX gx)
      (GradientY gy)
      (DirectionalDerivative derivative)
      (StepSize step)
      (AbsoluteError errorValue)
      (if feasible then Feasible else Infeasible)
      (if feasible then "" else "Direction and step move outside the feasible region.")

main :: IO ()
main = do
  print (auditDirection 4.0 3.0 1.0 1.0 0.25)
  print (auditDirection 4.0 3.0 2.0 (-1.0) 0.25)
  print (auditDirection 8.0 1.0 1.0 1.0 1.0)
