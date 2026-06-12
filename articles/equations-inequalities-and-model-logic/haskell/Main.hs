{-# OPTIONS_GHC -Wall #-}

module Main where

data StatementType
  = Equation
  | Inequality
  | DomainRule
  | Definition
  | ConditionalRule
  | ObjectiveRule
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data FormalStatement = FormalStatement
  { key :: String
  , statementType :: StatementType
  , expression :: String
  , interpretation :: String
  , condition :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

statements :: [FormalStatement]
statements =
  [ FormalStatement
      "storage_balance"
      Equation
      "S[t+1] = S[t] + I[t] - D[t] - lambda*S[t]"
      "Storage changes through inflow, demand, and proportional loss."
      "0 <= S[t], 0 <= lambda <= 1"
      Active
  , FormalStatement
      "storage_bounds"
      Inequality
      "0 <= S[t] <= K"
      "Storage is bounded by nonnegativity and capacity."
      "K > 0"
      RequiresReview
  , FormalStatement
      "shortage_definition"
      Definition
      "Q[t] = max(0, D[t] + lambda*S[t] - I[t] - S[t])"
      "Shortage is positive when demand and loss exceed available resources."
      "Q[t] >= 0"
      RequiresValidation
  , FormalStatement
      "low_storage_rule"
      ConditionalRule
      "if S[t] < T then reduce demand"
      "Conditional response activates below a threshold."
      "0 <= T <= K"
      RequiresSensitivityTest
  ]

needsReview :: FormalStatement -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed equations, inequalities, and model logic:"
  mapM_ print statements

  putStrLn "\nFormal statements requiring review:"
  mapM_ print (filter needsReview statements)
