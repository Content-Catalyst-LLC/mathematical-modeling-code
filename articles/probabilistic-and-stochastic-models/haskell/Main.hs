{-# OPTIONS_GHC -Wall #-}

module Main where

data ProbabilityComponent
  = RandomVariable
  | DistributionChoice
  | ParameterUncertainty
  | DerivedRiskMeasure
  | ConditionalStatement
  | SimulationSetting
  | ValidationDiagnostic
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresSensitivityTest
  | Revise
  deriving (Eq, Show)

data ProbabilityRecord = ProbabilityRecord
  { key :: String
  , component :: ProbabilityComponent
  , expression :: String
  , interpretation :: String
  , reviewFocus :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

probabilityRegister :: [ProbabilityRecord]
probabilityRegister =
  [ ProbabilityRecord
      "demand_distribution"
      RandomVariable
      "D ~ Lognormal(mu, sigma)"
      "Demand is positive and right-skewed."
      "Tail behavior and evidence."
      RequiresReview
  , ProbabilityRecord
      "supply_distribution"
      DistributionChoice
      "S ~ Normal(mean, sd), truncated at zero"
      "Supply varies around a planned level."
      "Support and truncation."
      RequiresReview
  , ProbabilityRecord
      "shortage_amount"
      DerivedRiskMeasure
      "Q = max(0, D - S - reserve)"
      "Shortage is positive when demand exceeds available supply."
      "Severity and probability."
      Active
  , ProbabilityRecord
      "simulation_count"
      SimulationSetting
      "M"
      "Monte Carlo sample size."
      "Stability of estimated risk."
      RequiresSensitivityTest
  ]

needsReview :: ProbabilityRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed probability model records:"
  mapM_ print probabilityRegister

  putStrLn "\nProbability records requiring review:"
  mapM_ print (filter needsReview probabilityRegister)
