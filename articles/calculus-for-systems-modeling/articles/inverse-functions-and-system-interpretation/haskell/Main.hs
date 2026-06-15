module Main where

newtype Output = Output Double deriving (Show)
newtype Input = Input Double deriving (Show)
newtype Sensitivity = Sensitivity Double deriving (Show)
newtype Residual = Residual Double deriving (Show)

data InverseAudit = InverseAudit
  { targetOutput :: Output
  , recoveredInput :: Input
  , forwardCheck :: Output
  , residualValue :: Residual
  , forwardSensitivity :: Sensitivity
  , inverseSensitivity :: Sensitivity
  , warning :: String
  } deriving (Show)

forwardModel :: Input -> Double
forwardModel (Input x) = log (1.0 + x)

forwardDerivative :: Input -> Double
forwardDerivative (Input x) = 1.0 / (1.0 + x)

inverseModel :: Output -> Double
inverseModel (Output y) = exp y - 1.0

inverseAudit :: Output -> InverseAudit
inverseAudit y@(Output target) =
  let xValue = inverseModel y
      x = Input xValue
      yCheck = forwardModel x
      derivative = forwardDerivative x
      invSensitivity = 1.0 / derivative
      residual = yCheck - target
      warningText =
        if xValue <= (-1.0) then "recovered input outside domain"
        else if abs derivative < 1.0e-6 then "small forward derivative"
        else if abs residual > 1.0e-8 then "forward check residual"
        else ""
  in InverseAudit y x (Output yCheck) (Residual residual) (Sensitivity derivative) (Sensitivity invSensitivity) warningText

main :: IO ()
main = mapM_ (print . inverseAudit . Output) [0.0, 0.5, 1.0, 1.5, 2.0]
