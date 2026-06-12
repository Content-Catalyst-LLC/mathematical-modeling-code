{-# OPTIONS_GHC -Wall #-}

module Main where

data RelationshipType
  = Identity
  | LinearRelationship
  | NonlinearRelationship
  | InequalityConstraint
  | ObjectiveFunction
  | RatioDefinition
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data AlgebraicRelationship = AlgebraicRelationship
  { key :: String
  , relationshipType :: RelationshipType
  , expression :: String
  , interpretation :: String
  , domainOrConstraint :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

relationships :: [AlgebraicRelationship]
relationships =
  [ AlgebraicRelationship
      "total_cost"
      Identity
      "C = c_a*x_a + c_b*x_b"
      "Total cost is the sum of option-specific costs."
      "x_a >= 0, x_b >= 0"
      Active
  , AlgebraicRelationship
      "budget_constraint"
      InequalityConstraint
      "c_a*x_a + c_b*x_b <= B"
      "Total modeled cost must not exceed budget."
      "B > 0"
      RequiresReview
  , AlgebraicRelationship
      "benefit_objective"
      ObjectiveFunction
      "V = b_a*x_a + b_b*x_b"
      "Total modeled benefit is additive across allocations."
      "benefit units must be comparable"
      RequiresValidation
  , AlgebraicRelationship
      "benefit_per_cost"
      RatioDefinition
      "r = V / C"
      "Benefit per unit cost."
      "C > 0"
      RequiresSensitivityTest
  ]

needsReview :: AlgebraicRelationship -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed algebraic relationships:"
  mapM_ print relationships

  putStrLn "\nRelationships requiring review:"
  mapM_ print (filter needsReview relationships)
