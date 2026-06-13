{-# OPTIONS_GHC -Wall #-}

module Main where

data StructuralLayer
  = ModelFamily
  | FunctionalForm
  | BoundaryChoice
  | AggregationChoice
  | ScaleChoice
  | RegimeBehavior
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresComparison
  | RequiresValidation
  | Revise
  deriving (Eq, Show)

data StructuralRecord = StructuralRecord
  { key :: String
  , layer :: StructuralLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

structuralRegister :: [StructuralRecord]
structuralRegister =
  [ StructuralRecord
      "model_family_choice"
      ModelFamily
      "Compares plausible mathematical model families."
      "Does the conclusion depend on the model family?"
      RequiresComparison
  , StructuralRecord
      "functional_form"
      FunctionalForm
      "Reviews whether equations impose the right relationship."
      "Does the equation form distort system behavior?"
      RequiresReview
  , StructuralRecord
      "boundary_choice"
      BoundaryChoice
      "Documents what is included and excluded."
      "Could excluded drivers change the conclusion?"
      RequiresReview
  , StructuralRecord
      "aggregation_choice"
      AggregationChoice
      "Reviews whether averaging hides heterogeneity."
      "Does aggregation conceal subgroup or spatial risk?"
      RequiresReview
  , StructuralRecord
      "threshold_regime"
      RegimeBehavior
      "Reviews whether behavior changes near critical thresholds."
      "Could regime shift invalidate the baseline structure?"
      RequiresValidation
  ]

needsReview :: StructuralRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed structural uncertainty records:"
  mapM_ print structuralRegister

  putStrLn "\nStructural records requiring review:"
  mapM_ print (filter needsReview structuralRegister)
