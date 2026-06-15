module Main where

newtype Input = Input Double deriving (Show)
newtype Output = Output Double deriving (Show)
newtype Derivative = Derivative Double deriving (Show)
newtype Elasticity = Elasticity Double deriving (Show)

data ElasticityValue
  = Defined Elasticity
  | Undefined String
  deriving (Show)

data SensitivityAudit = SensitivityAudit
  { input :: Input
  , output :: Output
  , derivative :: Derivative
  , elasticity :: ElasticityValue
  , responseClass :: String
  , warning :: String
  } deriving (Show)

responseFunction :: Double -> Double
responseFunction x = 10.0 * sqrt (x + 1.0)

analyticDerivative :: Double -> Double
analyticDerivative x = 5.0 / sqrt (x + 1.0)

classifyElasticity :: ElasticityValue -> String
classifyElasticity (Undefined _) = "elasticity undefined"
classifyElasticity (Defined (Elasticity e))
  | abs e < 1.0 = "inelastic local response"
  | abs e == 1.0 = "unit elastic local response"
  | otherwise = "elastic local response"

auditPoint :: Input -> SensitivityAudit
auditPoint i@(Input x) =
  let y = responseFunction x
      d = analyticDerivative x
      e =
        if x == 0.0 || y == 0.0
        then Undefined "elasticity requires nonzero input and output"
        else Defined (Elasticity ((x / y) * d))
      warningText =
        if x == 0.0
        then "input is zero; proportional input change requires care"
        else ""
  in SensitivityAudit i (Output y) (Derivative d) e (classifyElasticity e) warningText

main :: IO ()
main = mapM_ (print . auditPoint . Input) [0.0, 0.5, 1.0, 4.0, 9.0, 24.0]
