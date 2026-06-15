module Main where

data State = State Double Double deriving (Show)
data Displacement = Displacement Double Double deriving (Show)
data Gradient = Gradient Double Double deriving (Show)
data Hessian = Hessian Double Double Double Double deriving (Show)
data Classification = PositiveDefinite | NegativeDefinite | Indefinite | Inconclusive deriving (Show)

fModel :: State -> Double
fModel (State x y) = x * x + x * y + 3.0 * y * y + 0.2 * x * x * y

gradient :: State -> Gradient
gradient (State x y) = Gradient (2.0 * x + y + 0.4 * x * y) (x + 6.0 * y + 0.2 * x * x)

hessian :: State -> Hessian
hessian (State x y) = Hessian (2.0 + 0.4 * y) (1.0 + 0.4 * x) (1.0 + 0.4 * x) 6.0

determinant :: Hessian -> Double
determinant (Hessian h11 h12 h21 h22) = h11 * h22 - h12 * h21

classify :: Hessian -> Classification
classify h@(Hessian h11 _ _ _) =
  let detValue = determinant h
  in if detValue > 0 && h11 > 0
     then PositiveDefinite
     else if detValue > 0 && h11 < 0
          then NegativeDefinite
          else if detValue < 0
               then Indefinite
               else Inconclusive

firstOrderChange :: Gradient -> Displacement -> Double
firstOrderChange (Gradient gx gy) (Displacement dx dy) = gx * dx + gy * dy

quadraticTerm :: Hessian -> Displacement -> Double
quadraticTerm (Hessian h11 h12 _ h22) (Displacement dx dy) =
  0.5 * (h11 * dx * dx + 2.0 * h12 * dx * dy + h22 * dy * dy)

auditCase :: State -> Displacement -> String
auditCase state@(State x y) disp@(Displacement dx dy) =
  let g = gradient state
      h = hessian state
      baseline = fModel state
      actual = fModel (State (x + dx) (y + dy))
      actualChange = actual - baseline
      firstOrder = firstOrderChange g disp
      secondOrder = firstOrder + quadraticTerm h disp
      classValue = classify h
      warning =
        case classValue of
          Indefinite -> "Hessian is indefinite; local structure is saddle-like."
          Inconclusive -> "Hessian classification is inconclusive."
          _ -> ""
  in show (state, disp, g, h, determinant h, classValue, firstOrder, secondOrder, actualChange, abs (actualChange - firstOrder), abs (actualChange - secondOrder), warning)

main :: IO ()
main = do
  putStrLn (auditCase (State 2.0 1.0) (Displacement 0.1 (-0.05)))
  putStrLn (auditCase (State 2.0 1.0) (Displacement 0.5 0.5))
  putStrLn (auditCase (State (-5.0) 0.0) (Displacement 0.2 0.1))
