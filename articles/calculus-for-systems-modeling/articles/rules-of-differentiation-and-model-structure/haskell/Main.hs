module Main where

newtype Time = Time Double deriving (Show)
newtype Rate = Rate Double deriving (Show)
newtype Component = Component Double deriving (Show)

data DifferentiationRule = SumRule | ProductRule | QuotientRule | ChainRule deriving (Show)

data RuleAudit = RuleAudit
  { rule :: DifferentiationRule
  , modelStructure :: String
  , time :: Time
  , derivativeValue :: Rate
  , firstComponent :: Component
  , secondComponent :: Component
  } deriving (Show)

population :: Time -> Double
population (Time t) = 100.0 * exp (0.01 * t)

populationRate :: Time -> Double
populationRate t = 0.01 * population t

affluence :: Time -> Double
affluence (Time t) = 2.0 * exp (0.02 * t)

affluenceRate :: Time -> Double
affluenceRate t = 0.02 * affluence t

productRuleAudit :: Time -> RuleAudit
productRuleAudit t =
  let a = populationRate t * affluence t
      b = population t * affluenceRate t
  in RuleAudit ProductRule "impact = population * affluence" t (Rate (a + b)) (Component a) (Component b)

main :: IO ()
main = mapM_ (print . productRuleAudit . Time) [0.0, 5.0, 10.0, 20.0]
