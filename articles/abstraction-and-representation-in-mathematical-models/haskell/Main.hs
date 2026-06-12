{-# OPTIONS_GHC -Wall #-}

module Main where

data RepresentationForm
  = Equation
  | Graph
  | ProbabilityModel
  | OptimizationModel
  | Simulation
  | Diagram
  | DataTable
  deriving (Eq, Show)

data AbstractionStatus
  = PreservesRelevantStructure
  | RequiresReview
  | KnownIdealization
  | PotentialDistortion
  deriving (Eq, Show)

data ModelObject
  = StateVariable String
  | Parameter String
  | Assumption String
  | Constraint String
  | ProxyVariable String
  | OutputMetric String
  deriving (Eq, Show)

data RepresentationRecord = RepresentationRecord
  { modelObject :: ModelObject
  , representationForm :: RepresentationForm
  , meaning :: String
  , preservedStructure :: String
  , omittedDetail :: String
  , status :: AbstractionStatus
  , reviewQuestion :: String
  } deriving (Eq, Show)

records :: [RepresentationRecord]
records =
  [ RepresentationRecord
      (StateVariable "S_t")
      Equation
      "Aggregate storage at time t."
      "Accumulation and depletion."
      "Spatial distribution, quality, ownership, and access."
      PreservesRelevantStructure
      "Is aggregate storage sufficient for the intended use?"
  , RepresentationRecord
      (Parameter "K")
      Equation
      "Maximum storage capacity."
      "Upper feasibility bound."
      "Operating rules, safety reserves, and infrastructure condition."
      RequiresReview
      "Is physical capacity equivalent to usable capacity?"
  , RepresentationRecord
      (Assumption "well-mixed system")
      Simulation
      "The system is treated as internally homogeneous."
      "Aggregate dynamic behavior."
      "Local heterogeneity and spatial variation."
      KnownIdealization
      "Does heterogeneity affect conclusions?"
  , RepresentationRecord
      (ProxyVariable "shortage risk")
      DataTable
      "Periods with shortage are used as a risk indicator."
      "Failure frequency under scenarios."
      "Severity distribution, affected users, and recovery time."
      PotentialDistortion
      "Does this proxy represent the risk stakeholders care about?"
  ]

needsReview :: RepresentationRecord -> Bool
needsReview record =
  case status record of
    PreservesRelevantStructure -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed abstraction and representation records:"
  mapM_ print records
  putStrLn "\nRecords requiring representational review:"
  mapM_ print (filter needsReview records)
