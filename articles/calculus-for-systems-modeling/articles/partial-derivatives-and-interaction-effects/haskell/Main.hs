module Main where

newtype XInput = XInput Double deriving (Show)
newtype YInput = YInput Double deriving (Show)
newtype Output = Output Double deriving (Show)
newtype PartialX = PartialX Double deriving (Show)
newtype PartialY = PartialY Double deriving (Show)
newtype CrossPartialXY = CrossPartialXY Double deriving (Show)

data Feasibility = Feasible | Infeasible deriving (Show)

data PartialDerivativeRecord = PartialDerivativeRecord
  { xInput :: XInput
  , yInput :: YInput
  , output :: Output
  , partialX :: PartialX
  , partialY :: PartialY
  , crossPartialXY :: CrossPartialXY
  , feasibility :: Feasibility
  , warning :: String
  } deriving (Show)

systemResponse :: Double -> Double -> Double
systemResponse x y = 3.0 * x + 2.0 * y + 0.5 * x * y

partialXValue :: Double -> Double -> Double
partialXValue _x y = 3.0 + 0.5 * y

partialYValue :: Double -> Double -> Double
partialYValue x _y = 2.0 + 0.5 * x

crossPartial :: Double -> Double -> Double
crossPartial _x _y = 0.5

isFeasible :: Double -> Double -> Bool
isFeasible x y = x >= 0 && y >= 0 && x + y <= 10

makeRecord :: Double -> Double -> PartialDerivativeRecord
makeRecord x y =
  let feasible = isFeasible x y
  in PartialDerivativeRecord
      (XInput x)
      (YInput y)
      (Output (systemResponse x y))
      (PartialX (partialXValue x y))
      (PartialY (partialYValue x y))
      (CrossPartialXY (crossPartial x y))
      (if feasible then Feasible else Infeasible)
      (if feasible then "" else "Input combination is outside the feasible region.")

main :: IO ()
main = do
  print (makeRecord 2.0 4.0)
  print (makeRecord 8.0 8.0)
  print (makeRecord 6.0 3.0)
