{-# OPTIONS_GHC -Wall #-}

module Main where

data ScientificDomain
  = Physics
  | Chemistry
  | Biology
  | Ecology
  | EarthSystems
  | Epidemiology
  | ScientificComputing
  deriving (Eq, Show)

data ModelRole
  = Explanation
  | Prediction
  | Measurement
  | Simulation
  | ModelComparison
  | UncertaintyQuantification
  deriving (Eq, Show)

data ModelFamily
  = Algebraic
  | DifferentialEquation
  | Statistical
  | Stochastic
  | Network
  | Spatial
  | Computational
  deriving (Eq, Show)

data ReviewStatus
  = Active
  | RequiresReview
  | RequiresValidation
  | RequiresUncertaintyReview
  | Revise
  deriving (Eq, Show)

data ScientificModelRecord = ScientificModelRecord
  { key :: String
  , domain :: ScientificDomain
  , role :: ModelRole
  , family :: ModelFamily
  , evidenceQuestion :: String
  , status :: ReviewStatus
  } deriving (Eq, Show)

scientificRegister :: [ScientificModelRecord]
scientificRegister =
  [ ScientificModelRecord
      "mechanism_model"
      Ecology
      Explanation
      DifferentialEquation
      "Can resource limitation explain observed slowing growth?"
      Active
  , ScientificModelRecord
      "forecast_model"
      Biology
      Prediction
      Computational
      "What range of population outcomes is plausible after ten years?"
      RequiresUncertaintyReview
  , ScientificModelRecord
      "measurement_model"
      ScientificComputing
      Measurement
      Statistical
      "How does measurement noise affect interpretation?"
      RequiresReview
  , ScientificModelRecord
      "comparison_model"
      ScientificComputing
      ModelComparison
      Statistical
      "Does a logistic model explain observations better than exponential growth?"
      RequiresValidation
  ]

needsReview :: ScientificModelRecord -> Bool
needsReview item =
  case status item of
    Active -> False
    _ -> True

main :: IO ()
main = do
  putStrLn "Typed scientific model records:"
  mapM_ print scientificRegister

  putStrLn "\nScientific model records requiring review:"
  mapM_ print (filter needsReview scientificRegister)
