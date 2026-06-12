{-# OPTIONS_GHC -Wall #-}

module Main where

data AssumptionType
  = BoundaryAssumption
  | ScaleAssumption
  | FunctionalFormAssumption
  | ParameterAssumption
  | UncertaintyAssumption
  | ComputationalAssumption
  | InterpretiveAssumption
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresSensitivityTest
  | RequiresValidation
  | Revise
  deriving (Eq, Show)

data ModelDesignObject
  = StateVariable String
  | Parameter String
  | Constraint String
  | Assumption String
  | OutputMetric String
  | Simplification String
  deriving (Eq, Show)

data DesignRecord = DesignRecord
  { designObject :: ModelDesignObject
  , assumptionType :: AssumptionType
  , statement :: String
  , riskIfFalse :: String
  , status :: ReviewStatus
  , reviewQuestion :: String
  } deriving (Eq, Show)

records :: [DesignRecord]
records =
  [ DesignRecord
      (Simplification "aggregate stock")
      BoundaryAssumption
      "The resource system is represented by one aggregate stock."
      "Spatial variation, subgroup access, or local shortage may be hidden."
      RequiresReview
      "Does aggregate storage preserve the structure needed for the intended use?"
  , DesignRecord
      (Parameter "K")
      ParameterAssumption
      "Capacity is treated as fixed within each scenario."
      "Usable capacity may depend on operating rules or infrastructure condition."
      RequiresSensitivityTest
      "How do conclusions change under lower and higher capacity?"
  , DesignRecord
      (Assumption "proportional losses")
      FunctionalFormAssumption
      "Losses are proportional to current stock."
      "Losses may depend on season, temperature, leakage, or surface area."
      RequiresSensitivityTest
      "Should losses be process-based rather than proportional?"
  , DesignRecord
      (OutputMetric "shortage risk")
      InterpretiveAssumption
      "Shortage periods are treated as a useful summary of model risk."
      "Severity, duration, and affected users may be hidden."
      RequiresValidation
      "Does this output metric represent the decision need?"
  ]

needsReview :: DesignRecord -> Bool
needsReview record =
  case status record of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed assumption and model design records:"
  mapM_ print records
  putStrLn "\nRecords requiring review:"
  mapM_ print (filter needsReview records)
