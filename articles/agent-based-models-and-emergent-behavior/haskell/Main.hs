{-# OPTIONS_GHC -Wall #-}

module Main where

data ABMComponent
  = AgentState
  | BehaviorRule
  | InteractionStructure
  | EnvironmentDefinition
  | ScheduleRule
  | EmergenceDiagnostic
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data ABMRecord = ABMRecord
  { key :: String
  , component :: ABMComponent
  , ruleOrStructure :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

abmRegister :: [ABMRecord]
abmRegister =
  [ ABMRecord
      "agent_state"
      AgentState
      "adopted in {0,1}"
      "Each agent is either non-adopted or adopted."
      "State simplification."
      RequiresReview
  , ABMRecord
      "threshold_rule"
      BehaviorRule
      "adopt if adopted_neighbors_share >= threshold"
      "Agents adopt when local exposure exceeds threshold."
      "Behavioral evidence."
      RequiresReview
  , ABMRecord
      "ring_network"
      InteractionStructure
      "two neighbors on each side"
      "Agents interact in a local network."
      "Interaction validity."
      RequiresValidation
  , ABMRecord
      "ensemble_replication"
      ValidationDiagnostic
      "multiple random seeds"
      "Results are summarized across repeated runs."
      "Stochastic robustness."
      Active
  ]

needsReview :: ABMRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed agent-based model records:"
  mapM_ print abmRegister

  putStrLn "\nABM records requiring review:"
  mapM_ print (filter needsReview abmRegister)
