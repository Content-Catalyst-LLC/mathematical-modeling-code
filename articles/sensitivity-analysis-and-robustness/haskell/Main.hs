{-# OPTIONS_GHC -Wall #-}

module Main where

data SensitivityLayer
  = LocalSensitivity
  | GlobalSensitivity
  | Robustness
  | DecisionSupport
  | ModelForm
  | DataQuality
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresUncertaintyCheck
  | Revise
  deriving (Eq, Show)

data SensitivityRecord = SensitivityRecord
  { key :: String
  , layer :: SensitivityLayer
  , modelingRole :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

sensitivityRegister :: [SensitivityRecord]
sensitivityRegister =
  [ SensitivityRecord
      "parameter_sweep"
      LocalSensitivity
      "Varies individual parameters across plausible ranges."
      "Influential parameters."
      Active
  , SensitivityRecord
      "threshold_fragility"
      DecisionSupport
      "Reviews whether outputs cross a decision threshold."
      "Decision reversal."
      RequiresValidation
  , SensitivityRecord
      "scenario_stress"
      Robustness
      "Tests model behavior under adverse scenario conditions."
      "Stress robustness."
      RequiresReview
  , SensitivityRecord
      "structural_dependence"
      ModelForm
      "Reviews whether conclusions depend on model structure."
      "Model-form uncertainty."
      RequiresReview
  , SensitivityRecord
      "evidence_priority"
      DataQuality
      "Identifies high-sensitivity inputs that need better evidence."
      "Evidence priority."
      RequiresUncertaintyCheck
  ]

needsReview :: SensitivityRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed sensitivity records:"
  mapM_ print sensitivityRegister

  putStrLn "\nSensitivity records requiring review:"
  mapM_ print (filter needsReview sensitivityRegister)
