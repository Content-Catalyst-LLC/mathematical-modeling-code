{-# OPTIONS_GHC -Wall #-}

module Main where

data ComplexityFeature
  = FeedbackLoops
  | CascadingDependency
  | AdaptiveBehavior
  | DeepUncertainty
  | RobustnessUnderUncertainty
  deriving (Eq, Show)

data ComplexityModelFamily
  = SystemDynamics
  | NetworkModel
  | AgentBasedModel
  | ScenarioModeling
  | RobustDecisionAnalysis
  deriving (Eq, Show)

data ModelRole
  = DynamicExplanation
  | InterdependenceAnalysis
  | EmergenceAnalysis
  | DeepUncertaintyReview
  | DecisionSupport
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresRevision
  | Archive
  deriving (Eq, Show)

data ComplexityModelRecord = ComplexityModelRecord
  { key :: String
  , role :: ModelRole
  , family :: ComplexityModelFamily
  , feature :: ComplexityFeature
  , decisionContext :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

complexityRegister :: [ComplexityModelRecord]
complexityRegister =
  [ ComplexityModelRecord "feedback_model" DynamicExplanation SystemDynamics FeedbackLoops "Understanding nonlinear policy resistance" Active
  , ComplexityModelRecord "network_model" InterdependenceAnalysis NetworkModel CascadingDependency "Identifying systemic risk and fragile bridges" RequiresReview
  , ComplexityModelRecord "agent_model" EmergenceAnalysis AgentBasedModel AdaptiveBehavior "Testing heterogeneous response and emergence" RequiresReview
  , ComplexityModelRecord "scenario_model" DeepUncertaintyReview ScenarioModeling DeepUncertainty "Comparing plausible futures" RequiresReview
  , ComplexityModelRecord "robustness_model" DecisionSupport RobustDecisionAnalysis RobustnessUnderUncertainty "Choosing strategies across uncertainty" RequiresReview
  ]

needsReview :: ComplexityModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    Archive -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed complexity model records:"
  mapM_ print complexityRegister

  putStrLn "\nComplexity model records requiring review:"
  mapM_ print (filter needsReview complexityRegister)
