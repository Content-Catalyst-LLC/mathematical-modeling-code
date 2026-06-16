module Main where

data SymbolicRecord = SymbolicRecord
  { item :: String
  , expression :: String
  , interpretation :: String
  , warning :: String
  } deriving (Show)

records :: [SymbolicRecord]
records =
  [ SymbolicRecord "rate_expression" "r*x*(1 - x/K)" "Logistic growth rate expression." "Assumes documented domain conditions including K not equal to zero."
  , SymbolicRecord "first_derivative" "r - 2*r*x/K" "Marginal growth effect declines as x increases." "Derivative interpretation depends on positive-domain assumptions."
  , SymbolicRecord "second_derivative" "-2*r/K" "Curvature is negative when r and K are positive." "Curvature describes model structure, not empirical validity."
  , SymbolicRecord "equilibria" "x = 0 or x = K" "Equilibria occur where the rate expression equals zero." "Equilibria require domain and stability review."
  , SymbolicRecord "limit_at_capacity" "0" "Growth rate approaches zero as x approaches carrying capacity." "Boundary behavior should be checked against modeled assumptions."
  ]

main :: IO ()
main = mapM_ print records
