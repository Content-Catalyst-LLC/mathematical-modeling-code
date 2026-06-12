{-# OPTIONS_GHC -Wall #-}

module Main where

data RepositoryLayer
  = Documentation
  | DataLayer
  | CodeLayer
  | Metadata
  | Reproducibility
  | Validation
  | Governance
  | Licensing
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresArchiveCheck
  | Revise
  deriving (Eq, Show)

data RepositoryRecord = RepositoryRecord
  { key :: String
  , layer :: RepositoryLayer
  , artifact :: String
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

repositoryRegister :: [RepositoryRecord]
repositoryRegister =
  [ RepositoryRecord
      "readme"
      Documentation
      "README.md"
      "Explains project purpose, structure, setup, and run commands."
      "Usability and onboarding."
      RequiresReview
  , RepositoryRecord
      "data_provenance"
      DataLayer
      "data provenance notes"
      "Documents sources, transformations, units, and constraints."
      "Evidence traceability."
      RequiresReview
  , RepositoryRecord
      "run_manifest"
      Reproducibility
      "reproducibility_manifest.json"
      "Records execution context and output hashes."
      "Rerun capability."
      Active
  , RepositoryRecord
      "model_card"
      Governance
      "model_repository_card.json"
      "Summarizes purpose, assumptions, validation, and use limits."
      "Decision-support governance."
      RequiresValidation
  ]

needsReview :: RepositoryRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed model repository records:"
  mapM_ print repositoryRegister

  putStrLn "\nRepository records requiring review:"
  mapM_ print (filter needsReview repositoryRegister)
