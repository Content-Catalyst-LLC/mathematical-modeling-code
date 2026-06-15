module Main where

newtype Parameter = Parameter Double deriving (Show)
newtype State = State Double deriving (Show)
newtype PartialState = PartialState Double deriving (Show)
newtype PartialParameter = PartialParameter Double deriving (Show)
newtype Sensitivity = Sensitivity Double deriving (Show)

data ImplicitAudit = ImplicitAudit
  { parameter :: Parameter
  , equilibriumState :: State
  , constraintValue :: Double
  , statePartial :: PartialState
  , parameterPartial :: PartialParameter
  , implicitDerivative :: Sensitivity
  , warning :: String
  } deriving (Show)

equilibriumStateValue :: Parameter -> Double
equilibriumStateValue (Parameter p) =
  (-p + sqrt (p * p + 40.0)) / 2.0

constraint :: State -> Parameter -> Double
constraint (State x) (Parameter p) =
  x * x + p * x - 10.0

partialState :: State -> Parameter -> Double
partialState (State x) (Parameter p) =
  2.0 * x + p

partialParameter :: State -> Parameter -> Double
partialParameter (State x) _ =
  x

implicitSensitivity :: State -> Parameter -> Double
implicitSensitivity x p =
  let gx = partialState x p
      gp = partialParameter x p
  in -gp / gx

auditParameter :: Parameter -> ImplicitAudit
auditParameter p =
  let xValue = equilibriumStateValue p
      x = State xValue
      gx = partialState x p
      gp = partialParameter x p
      sens = implicitSensitivity x p
      warningText = if abs gx < 1.0e-8 then "regularity failure" else ""
  in ImplicitAudit p x (constraint x p) (PartialState gx) (PartialParameter gp) (Sensitivity sens) warningText

main :: IO ()
main = mapM_ (print . auditParameter . Parameter) [-3.0, -1.0, 0.0, 1.0, 3.0]
