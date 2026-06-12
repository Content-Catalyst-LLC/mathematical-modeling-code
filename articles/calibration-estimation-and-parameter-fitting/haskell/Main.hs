{-# OPTIONS_GHC -Wall #-}

module Main where

data CalibrationLayer
  = Evidence
  | ParameterSpace
  | LossFunction
  | Optimization
  | ResidualDiagnostic
  | ParameterUncertainty
  | Validation
  | Governance
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresUncertaintyCheck
  | Revise
  deriving (Eq, Show)

data CalibrationRecord = CalibrationRecord
  { key :: String
  , layer :: CalibrationLayer
  , modelingRole :: String
  , diagnosticFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

calibrationRegister :: [CalibrationRecord]
calibrationRegister =
  [ CalibrationRecord
      "calibration_data"
      Evidence
      "Provides observations for fitting."
      "Data relevance and measurement error."
      RequiresReview
  , CalibrationRecord
      "objective_function"
      LossFunction
      "Defines model-data mismatch."
      "Loss-function appropriateness."
      RequiresReview
  , CalibrationRecord
      "parameter_bounds"
      ParameterSpace
      "Constrains fitted values to plausible ranges."
      "Parameter bound justification."
      RequiresReview
  , CalibrationRecord
      "residual_diagnostics"
      ResidualDiagnostic
      "Checks post-fit error patterns."
      "Residual structure."
      Active
  , CalibrationRecord
      "validation_split"
      Validation
      "Checks fitted model beyond calibration data."
      "Generalization."
      RequiresValidation
  ]

needsReview :: CalibrationRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed calibration records:"
  mapM_ print calibrationRegister

  putStrLn "\nCalibration records requiring review:"
  mapM_ print (filter needsReview calibrationRegister)
