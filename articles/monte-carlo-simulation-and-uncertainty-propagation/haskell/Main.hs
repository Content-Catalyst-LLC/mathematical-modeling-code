{-# OPTIONS_GHC -Wall #-}

module Main where

data MonteCarloComponent
  = InputUncertainty
  | SamplingDesign
  | RandomSeedProtocol
  | OutputDistribution
  | RiskMetric
  | ConvergenceDiagnostic
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data MonteCarloRecord = MonteCarloRecord
  { key :: String
  , component :: MonteCarloComponent
  , uncertaintyStructure :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

monteCarloRegister :: [MonteCarloRecord]
monteCarloRegister =
  [ MonteCarloRecord
      "input_distributions"
      InputUncertainty
      "bounded distributions for stock, growth, extraction, and shocks"
      "Uncertain inputs are represented by explicit distributions."
      "Distribution justification."
      RequiresReview
  , MonteCarloRecord
      "sampling_protocol"
      SamplingDesign
      "pseudo-random independent draws with recorded seed"
      "Replications propagate uncertainty through the model."
      "Sampling adequacy."
      Active
  , MonteCarloRecord
      "threshold_metric"
      RiskMetric
      "P(final_stock <= depletion_threshold)"
      "Risk is summarized as a depletion probability."
      "Threshold appropriateness."
      RequiresValidation
  , MonteCarloRecord
      "convergence_diagnostic"
      ConvergenceDiagnostic
      "running mean and threshold probability by replication count"
      "Estimates should stabilize with more replications."
      "Monte Carlo convergence."
      RequiresSensitivityTest
  ]

needsReview :: MonteCarloRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed Monte Carlo model records:"
  mapM_ print monteCarloRegister

  putStrLn "\nMonte Carlo records requiring review:"
  mapM_ print (filter needsReview monteCarloRegister)
