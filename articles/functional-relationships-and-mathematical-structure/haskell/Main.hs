{-# OPTIONS_GHC -Wall #-}

module Main where

data RelationshipType
  = Linear
  | Nonlinear
  | Dynamic
  | Stochastic
  | Feedback
  | Constraint
  | Networked
  | Optimization
  deriving (Eq, Show)

data StructureStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data RelationshipRecord = RelationshipRecord
  { key :: String
  , relationshipType :: RelationshipType
  , expression :: String
  , interpretation :: String
  , structuralAssumption :: String
  , status :: StructureStatus
  } deriving (Eq, Show)

relationships :: [RelationshipRecord]
relationships =
  [ RelationshipRecord
      "linear_update"
      Dynamic
      "S[t+1] = S[t] + I[t] - D[t] - lambda*S[t]"
      "Storage changes through inflow, demand, and proportional loss."
      "Loss is proportional and demand is exogenous."
      Active
  , RelationshipRecord
      "constrained_update"
      Constraint
      "S[t+1] = min(K, max(0, raw_next_stock))"
      "Storage is bounded below by zero and above by capacity."
      "Constraint clipping must not hide shortage or overflow."
      RequiresReview
  , RelationshipRecord
      "feedback_demand"
      Feedback
      "D[t+1] = max(0, D[t] - alpha*shortage[t])"
      "Demand adapts when shortage occurs."
      "Feedback is immediate and proportional."
      RequiresValidation
  , RelationshipRecord
      "stochastic_inflow"
      Stochastic
      "I[t] = I_bar * exp(epsilon[t])"
      "Inflow varies multiplicatively around baseline."
      "Random shocks require evidence and uncertainty review."
      RequiresSensitivityTest
  ]

needsReview :: RelationshipRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed functional relationships and structures:"
  mapM_ print relationships

  putStrLn "\nRelationships requiring review:"
  mapM_ print (filter needsReview relationships)
