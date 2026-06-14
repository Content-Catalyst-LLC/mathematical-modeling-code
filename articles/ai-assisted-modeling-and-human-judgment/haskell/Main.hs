{-# OPTIONS_GHC -Wall #-}

module Main where

data ModelingStage
  = ProblemFraming
  | ScenarioDesign
  | Computation
  | Validation
  | Communication
  | Governance
  deriving (Eq, Show)

data AIRole
  = IdeaGenerator
  | CodeAssistant
  | DiagnosticAide
  | DocumentationAssistant
  | ReviewCompanion
  deriving (Eq, Show)

data ArtifactType
  = ScenarioList
  | ModelScript
  | DiagnosticReport
  | PublicSummary
  | UseLimitStatement
  deriving (Eq, Show)

data ReviewStatus
  = Exploratory
  | Draft
  | RequiresReview
  | Approved
  | Retired
  deriving (Eq, Show)

data AIAssistanceRecord = AIAssistanceRecord
  { key :: String
  , stage :: ModelingStage
  , aiRole :: AIRole
  , artifactType :: ArtifactType
  , provenanceRequired :: Bool
  , humanReviewRequired :: Bool
  , status :: ReviewStatus
  } deriving (Eq, Show)

aiAssistanceRegister :: [AIAssistanceRecord]
aiAssistanceRegister =
  [ AIAssistanceRecord "scenario_drafting" ScenarioDesign IdeaGenerator ScenarioList True True RequiresReview
  , AIAssistanceRecord "code_generation" Computation CodeAssistant ModelScript True True RequiresReview
  , AIAssistanceRecord "diagnostic_summary" Validation DiagnosticAide DiagnosticReport True True RequiresReview
  , AIAssistanceRecord "communication_draft" Communication DocumentationAssistant PublicSummary True True RequiresReview
  , AIAssistanceRecord "governance_template" Governance ReviewCompanion UseLimitStatement True True Draft
  ]

requiresHumanReview :: AIAssistanceRecord -> Bool
requiresHumanReview item = humanReviewRequired item || status item == RequiresReview

main :: IO ()
main = do
  putStrLn "Typed AI assistance records:"
  mapM_ print aiAssistanceRegister

  putStrLn "\nRecords requiring human review:"
  mapM_ print (filter requiresHumanReview aiAssistanceRegister)
