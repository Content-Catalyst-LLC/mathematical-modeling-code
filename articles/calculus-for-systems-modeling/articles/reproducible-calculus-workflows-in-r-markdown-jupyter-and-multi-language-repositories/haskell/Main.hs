module Main where

data ArtifactOrigin
  = SourceArtifact
  | GeneratedArtifact
  deriving (Show, Eq)

data ArtifactType
  = CSV
  | JSONFile
  | Markdown
  | Notebook
  | Script
  | Schema
  deriving (Show, Eq)

data WorkflowArtifact = WorkflowArtifact
  { artifactName :: String
  , artifactType :: ArtifactType
  , artifactPath :: String
  , artifactOrigin :: ArtifactOrigin
  , reviewRole :: String
  , interpretationWarning :: String
  } deriving (Show, Eq)

data RunRecord = RunRecord
  { workflowName :: String
  , command :: String
  , expectedArtifacts :: Int
  , reviewRequired :: Bool
  , runWarning :: String
  } deriving (Show, Eq)

artifacts :: [WorkflowArtifact]
artifacts =
  [ WorkflowArtifact "parameter_records" CSV "data/parameter_records.csv" SourceArtifact "documents parameter names, units, values, ranges, and sources" "Parameter records do not prove empirical correctness."
  , WorkflowArtifact "workflow_artifacts" JSONFile "outputs/json/workflow_artifacts.json" GeneratedArtifact "stores structured reproducibility metadata" "Structured metadata must remain synchronized with generated outputs."
  , WorkflowArtifact "reproducibility_audit" Markdown "outputs/reports/reproducibility_audit.md" GeneratedArtifact "summarizes run status, artifacts, and warnings" "Audit summaries support review but do not replace inspection."
  , WorkflowArtifact "governance_queue" Markdown "outputs/reports/governance_queue.md" GeneratedArtifact "collects unresolved warnings requiring human review" "Governance queues support judgment but do not replace it."
  ]

runRecord :: RunRecord
runRecord =
  RunRecord
    "typed_reproducibility_workflow"
    "make smoke"
    (length artifacts)
    True
    "Reproducibility supports auditability but does not prove model validity."

main :: IO ()
main = do
  putStrLn "Workflow artifacts:"
  mapM_ print artifacts
  putStrLn ""
  putStrLn "Run record:"
  print runRecord
