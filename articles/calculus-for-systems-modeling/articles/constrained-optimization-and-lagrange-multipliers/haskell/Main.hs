module Main where

data State = State Double Double deriving (Show)
data Target = Target Double deriving (Show)
data Gradient = Gradient Double Double deriving (Show)
data Audit = Audit
  { state :: State
  , objectiveValue :: Double
  , constraintValue :: Double
  , constraintTarget :: Double
  , constraintResidual :: Double
  , lambdaValue :: Double
  , stationarityResidualNorm :: Double
  , feasible :: Bool
  , warning :: String
  } deriving (Show)

objective :: State -> Double
objective (State x y) = x * x + 2.0 * y * y

constraint :: State -> Double
constraint (State x y) = x + y

gradObjective :: State -> Gradient
gradObjective (State x y) = Gradient (2.0 * x) (4.0 * y)

gradConstraint :: State -> Gradient
gradConstraint _ = Gradient 1.0 1.0

solveBudgetConstraint :: Target -> (State, Double)
solveBudgetConstraint (Target target) =
  let y = target / 3.0
      x = 2.0 * target / 3.0
      lambda = 2.0 * x
  in (State x y, lambda)

stationarityNorm :: Gradient -> Gradient -> Double -> Double
stationarityNorm (Gradient fx fy) (Gradient gx gy) lambda =
  sqrt ((fx - lambda * gx)^2 + (fy - lambda * gy)^2)

auditSolution :: Target -> Audit
auditSolution target@(Target targetValue) =
  let (candidate, lambda) = solveBudgetConstraint target
      cValue = constraint candidate
      cResidual = cValue - targetValue
      feasibleValue = abs cResidual <= 1.0e-9
      residualNorm = stationarityNorm (gradObjective candidate) (gradConstraint candidate) lambda
      warningText =
        if not feasibleValue
        then "Candidate solution violates the constraint."
        else if residualNorm > 1.0e-8
             then "Stationarity residual is large."
             else "Multiplier interpretation is local and unit-dependent."
  in Audit candidate (objective candidate) cValue targetValue cResidual lambda residualNorm feasibleValue warningText

main :: IO ()
main = do
  print (auditSolution (Target 12.0))
  print (auditSolution (Target 18.0))
  print (auditSolution (Target 24.0))
