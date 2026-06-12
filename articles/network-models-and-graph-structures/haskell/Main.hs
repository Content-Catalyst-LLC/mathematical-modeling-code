{-# OPTIONS_GHC -Wall #-}

module Main where

data NetworkComponent
  = NodeDefinition
  | EdgeDefinition
  | EdgeWeight
  | DirectionRule
  | CentralityDiagnostic
  | ProcessRule
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data NetworkRecord = NetworkRecord
  { key :: String
  , component :: NetworkComponent
  , expression :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

networkRegister :: [NetworkRecord]
networkRegister =
  [ NetworkRecord "node_definition" NodeDefinition "V" "Nodes represent infrastructure assets." "Boundary and scale." RequiresReview
  , NetworkRecord "directed_dependency_edge" EdgeDefinition "source -> target" "Directed edge indicates dependency." "Direction and evidence quality." RequiresReview
  , NetworkRecord "edge_weight" EdgeWeight "w_ij" "Weight represents dependency strength." "Weight estimation and validation." RequiresValidation
  , NetworkRecord "centrality_diagnostic" CentralityDiagnostic "in_degree, out_degree, reachability" "Diagnostics identify structurally important nodes." "Practical meaning of centrality." Active
  ]

needsReview :: NetworkRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed network model records:"
  mapM_ print networkRegister
  putStrLn "\nNetwork records requiring review:"
  mapM_ print (filter needsReview networkRegister)
