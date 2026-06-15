module Main where

newtype Input = Input Double deriving (Show)
newtype Value = Value Double deriving (Show)
newtype FirstDerivative = FirstDerivative Double deriving (Show)
newtype SecondDerivative = SecondDerivative Double deriving (Show)
newtype Curvature = Curvature Double deriving (Show)

data CurvatureAudit = CurvatureAudit
  { input :: Input
  , value :: Value
  , first :: FirstDerivative
  , second :: SecondDerivative
  , curvatureValue :: Curvature
  , concavity :: String
  , warning :: String
  } deriving (Show)

logistic :: Double -> Double
logistic x = 1.0 / (1.0 + exp (-x))

firstDerivative :: Double -> Double
firstDerivative x =
  let y = logistic x
  in y * (1.0 - y)

secondDerivative :: Double -> Double
secondDerivative x =
  let y = logistic x
  in y * (1.0 - y) * (1.0 - 2.0 * y)

curvature :: Double -> Double
curvature x =
  let fp = firstDerivative x
      fpp = secondDerivative x
  in abs fpp / ((1.0 + fp * fp) ** 1.5)

classifyConcavity :: Double -> String
classifyConcavity value
  | value > 1.0e-8 = "concave up"
  | value < -1.0e-8 = "concave down"
  | otherwise = "near zero curvature candidate"

auditPoint :: Input -> CurvatureAudit
auditPoint i@(Input x) =
  let y = logistic x
      fp = firstDerivative x
      fpp = secondDerivative x
      kappa = curvature x
      warningText = if abs fpp < 1.0e-8 then "possible inflection candidate" else ""
  in CurvatureAudit i (Value y) (FirstDerivative fp) (SecondDerivative fpp) (Curvature kappa) (classifyConcavity fpp) warningText

main :: IO ()
main = mapM_ (print . auditPoint . Input) [-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0]
