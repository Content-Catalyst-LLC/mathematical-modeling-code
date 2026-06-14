{-# OPTIONS_GHC -Wall #-}

module Main where

data ModelStage
  = Framing
  | DataReview
  | Design
  | Validation
  | Communication
  | Deployment
  | Monitoring
  | Governance
  deriving (Eq, Show)

data FailureMode
  = BoundaryFailure
  | DataBias
  | ValidationGap
  | FalsePrecision
  | ScopeCreep
  | AccountabilityGap
  deriving (Eq, Show)

data EthicalIssue
  = HiddenConsequences
  | UnequalError
  | UnsupportedAuthority
  | Overconfidence
  | Misuse
  | ResponsibilityShifting
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresRevision
  | Retire
  deriving (Eq, Show)

data ModelEthicsRecord = ModelEthicsRecord
  { key :: String
  , stage :: ModelStage
  , failureMode :: FailureMode
  , ethicalIssue :: EthicalIssue
  , useLimitRequired :: Bool
  , status :: ReviewStatus
  } deriving (Eq, Show)

ethicsRegister :: [ModelEthicsRecord]
ethicsRegister =
  [ ModelEthicsRecord "boundary_failure" Design BoundaryFailure HiddenConsequences True RequiresReview
  , ModelEthicsRecord "data_bias" DataReview DataBias UnequalError True RequiresReview
  , ModelEthicsRecord "validation_gap" Validation ValidationGap UnsupportedAuthority True RequiresReview
  , ModelEthicsRecord "false_precision" Communication FalsePrecision Overconfidence True RequiresReview
  , ModelEthicsRecord "scope_creep" Deployment ScopeCreep Misuse True RequiresRevision
  , ModelEthicsRecord "accountability_gap" Governance AccountabilityGap ResponsibilityShifting True RequiresRevision
  ]

needsReview :: ModelEthicsRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    Retire -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed model ethics records:"
  mapM_ print ethicsRegister

  putStrLn "\nModel ethics records requiring review:"
  mapM_ print (filter needsReview ethicsRegister)
