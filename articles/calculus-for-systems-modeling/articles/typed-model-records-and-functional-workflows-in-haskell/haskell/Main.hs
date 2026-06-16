module Main where

import Text.Printf (printf)

data SolverStatus
  = Converged
  | Warning String
  | Failed String
  | NotEvaluated
  deriving (Show, Eq)

data ModelUse
  = TeachingExample
  | CalibrationStudy
  | ScenarioExploration
  | GovernanceReview
  deriving (Show, Eq)

data ModelParameters = ModelParameters
  { growthRate :: Double
  , carryingCapacity :: Double
  , initialStock :: Double
  , timeStep :: Double
  , horizon :: Double
  , parameterNote :: String
  } deriving (Show, Eq)

data ModelState = ModelState
  { modelTime :: Double
  , stock :: Double
  } deriving (Show, Eq)

data DiagnosticRecord = DiagnosticRecord
  { diagnosticName :: String
  , diagnosticStatus :: SolverStatus
  , diagnosticMessage :: String
  , reviewRequired :: Bool
  } deriving (Show, Eq)

data ModelOutput = ModelOutput
  { outputUse :: ModelUse
  , outputParameters :: ModelParameters
  , finalState :: ModelState
  , diagnostics :: [DiagnosticRecord]
  , interpretationWarning :: String
  } deriving (Show, Eq)

validateParameters :: ModelParameters -> [String]
validateParameters params =
  concat
    [ if growthRate params <= 0 then ["growthRate must be positive"] else []
    , if carryingCapacity params <= 0 then ["carryingCapacity must be positive"] else []
    , if initialStock params <= 0 then ["initialStock must be positive"] else []
    , if timeStep params <= 0 then ["timeStep must be positive"] else []
    , if horizon params <= 0 then ["horizon must be positive"] else []
    ]

stepLogistic :: ModelParameters -> ModelState -> ModelState
stepLogistic params state =
  let x = stock state
      r = growthRate params
      k = carryingCapacity params
      dt = timeStep params
      dx = r * x * (1 - x / k)
  in ModelState
      { modelTime = modelTime state + dt
      , stock = x + dt * dx
      }

simulate :: ModelParameters -> [ModelState]
simulate params =
  takeWhile
    (\state -> modelTime state <= horizon params + 1.0e-9)
    (iterate (stepLogistic params) initial)
  where
    initial = ModelState 0.0 (initialStock params)

buildDiagnostics :: ModelParameters -> [String] -> [ModelState] -> [DiagnosticRecord]
buildDiagnostics params validationMessages states =
  let final = last states
      validationDiagnostic =
        if null validationMessages
          then DiagnosticRecord "parameter_validation" Converged "All basic parameter checks passed." False
          else DiagnosticRecord "parameter_validation" (Warning (unwords validationMessages)) "Parameter validation requires review." True
      capacityDiagnostic =
        if stock final <= carryingCapacity params
          then DiagnosticRecord "capacity_check" Converged "Final stock remains within carrying capacity." False
          else DiagnosticRecord "capacity_check" (Warning "Final stock exceeds carrying capacity.") "Capacity interpretation requires review." True
  in [validationDiagnostic, capacityDiagnostic]

buildOutput :: ModelParameters -> ModelOutput
buildOutput params =
  let states = simulate params
      validationMessages = validateParameters params
      diagnosticRecords = buildDiagnostics params validationMessages states
  in ModelOutput
      { outputUse = GovernanceReview
      , outputParameters = params
      , finalState = last states
      , diagnostics = diagnosticRecords
      , interpretationWarning = "Typed records improve structural review but do not prove empirical validity."
      }

csvHeader :: String
csvHeader = "model_use,growth_rate,carrying_capacity,initial_stock,time_step,horizon,final_time,final_stock,warning"

csvRow :: ModelOutput -> String
csvRow output =
  let params = outputParameters output
      final = finalState output
  in printf "%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s"
      (show (outputUse output))
      (growthRate params)
      (carryingCapacity params)
      (initialStock params)
      (timeStep params)
      (horizon params)
      (modelTime final)
      (stock final)
      (interpretationWarning output)

main :: IO ()
main = do
  let params =
        ModelParameters
          { growthRate = 0.35
          , carryingCapacity = 100.0
          , initialStock = 10.0
          , timeStep = 0.25
          , horizon = 20.0
          , parameterNote = "Synthetic teaching example for typed model governance."
          }
  let output = buildOutput params
  putStrLn csvHeader
  putStrLn (csvRow output)
  putStrLn ""
  putStrLn "Diagnostics:"
  mapM_ print (diagnostics output)
