module Main where
newtype XInput = XInput Double deriving (Show)
newtype YInput = YInput Double deriving (Show)
newtype Output = Output Double deriving (Show)
data Feasibility = Feasible | Infeasible deriving (Show)
data MultivariableRecord = MultivariableRecord { xInput :: XInput, yInput :: YInput, output :: Output, feasibility :: Feasibility, warning :: String } deriving (Show)
systemResponse :: Double -> Double -> Double
systemResponse x y = 3.0 * x + 2.0 * y + 0.5 * x * y
isFeasible :: Double -> Double -> Bool
isFeasible x y = x >= 0 && y >= 0 && x + y <= 10
makeRecord :: Double -> Double -> MultivariableRecord
makeRecord x y = let feasible = isFeasible x y in MultivariableRecord (XInput x) (YInput y) (Output (systemResponse x y)) (if feasible then Feasible else Infeasible) (if feasible then "" else "Input combination is outside the feasible region.")
main :: IO ()
main = do
  print (makeRecord 2.0 4.0)
  print (makeRecord 8.0 8.0)
  print (makeRecord 6.0 3.0)
