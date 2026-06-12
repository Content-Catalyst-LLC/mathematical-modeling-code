{-# OPTIONS_GHC -Wall #-}

module Main where

data ModelingStage
  = WorldContext
  | ProblemFraming
  | Abstraction
  | BoundarySelection
  | VariableDesign
  | AssumptionDesign
  | FormalFormulation
  | Computation
  | Calibration
  | Validation
  | UncertaintyReview
  | Interpretation
  | Revision
  deriving (Eq, Show)

data ReviewStatus
  = Draft
  | Active
  | RequiresEvidence
  | RequiresSensitivityTest
  | RequiresValidation
  | AdequateForPurpose
  | NotAdequateForPurpose
  deriving (Eq, Show)

data ModelComponent
  = StateVariable String
  | Parameter String
  | Constraint String
  | Assumption String
  | EvidenceSource String
  | OutputMetric String
  deriving (Eq, Show)

data ModelingRecord = ModelingRecord
  { stage :: ModelingStage
  , component :: ModelComponent
  , statement :: String
  , status :: ReviewStatus
  , reviewQuestion :: String
  } deriving (Eq, Show)

records :: [ModelingRecord]
records =
  [ ModelingRecord
      ProblemFraming
      (OutputMetric "shortage risk")
      "The model is intended to compare reservoir shortage risk across scenarios."
      Active
      "Does this output answer the decision question?"
  , ModelingRecord
      VariableDesign
      (StateVariable "S_t")
      "Reservoir storage at time t represents the system state."
      Active
      "Are units, measurement method, and time scale clear?"
  , ModelingRecord
      AssumptionDesign
      (Assumption "inflow is scenario-based")
      "Inflow is treated as a scenario input rather than a stochastic process."
      RequiresSensitivityTest
      "How does shortage risk change under dry average and wet scenarios?"
  , ModelingRecord
      FormalFormulation
      (Constraint "0 <= S_t <= K")
      "Storage is bounded below by zero and above by capacity."
      Active
      "Does the constraint reflect operating rules as well as physical capacity?"
  , ModelingRecord
      Validation
      (EvidenceSource "observed historical storage")
      "Model outputs should be compared with observed storage before operational use."
      RequiresValidation
      "Are residuals acceptable for the intended use?"
  ]

needsReview :: ModelingRecord -> Bool
needsReview record =
  case status record of
    RequiresEvidence -> True
    RequiresSensitivityTest -> True
    RequiresValidation -> True
    NotAdequateForPurpose -> True
    _ -> False

main :: IO ()
main = do
  putStrLn "Typed modeling process records:"
  mapM_ print records
  putStrLn "\nRecords requiring review:"
  mapM_ print (filter needsReview records)
