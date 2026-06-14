{-# OPTIONS_GHC -Wall #-}
module Main where

data FutureModelingArea = ModelArchitecture | ComputationalWorkflow | OperationalModeling | UncertaintyAnalysis | GovernanceAndLegitimacy deriving (Eq, Show)
data ReviewClass = GovernancePriority | UncertaintyPriority | StrategicPriority | Monitor deriving (Eq, Show)

data FutureDirectionRecord = FutureDirectionRecord
  { key :: String
  , directionName :: String
  , modelingArea :: FutureModelingArea
  , complexityRelevance :: Double
  , technicalMaturity :: Double
  , governanceNeed :: Double
  , uncertaintyPressure :: Double
  , humanJudgmentNeed :: Double
  } deriving (Eq, Show)

futureDirections :: [FutureDirectionRecord]
futureDirections =
  [ FutureDirectionRecord "hybrid_models" "Hybrid modeling and model ensembles" ModelArchitecture 0.88 0.70 0.74 0.72 0.80
  , FutureDirectionRecord "ai_assistance" "AI-assisted modeling" ComputationalWorkflow 0.82 0.78 0.90 0.76 0.92
  , FutureDirectionRecord "digital_twins" "Digital twins and living models" OperationalModeling 0.86 0.75 0.88 0.70 0.84
  , FutureDirectionRecord "uncertainty_workflows" "Uncertainty-aware modeling" UncertaintyAnalysis 0.90 0.72 0.82 0.92 0.86
  , FutureDirectionRecord "participatory_modeling" "Participatory and public-interest modeling" GovernanceAndLegitimacy 0.78 0.62 0.86 0.68 0.94
  ]

futurePriorityScore :: FutureDirectionRecord -> Double
futurePriorityScore item =
  0.25 * complexityRelevance item + 0.20 * technicalMaturity item + 0.20 * governanceNeed item + 0.20 * uncertaintyPressure item + 0.15 * humanJudgmentNeed item

reviewClass :: FutureDirectionRecord -> ReviewClass
reviewClass item
  | governanceNeed item >= 0.85 || humanJudgmentNeed item >= 0.90 = GovernancePriority
  | uncertaintyPressure item >= 0.85 = UncertaintyPriority
  | futurePriorityScore item >= 0.78 = StrategicPriority
  | otherwise = Monitor

main :: IO ()
main = do
  putStrLn "Typed future modeling direction records:"
  mapM_ print futureDirections
  putStrLn "\nFuture direction review classes:"
  mapM_ (\item -> putStrLn (key item ++ ": " ++ show (reviewClass item))) futureDirections
