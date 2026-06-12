{-# OPTIONS_GHC -Wall #-}
module Main where
data ComponentType = StateVariable | InputVariable | OutputVariable | DecisionVariable | Parameter | Constraint | DerivedVariable deriving (Eq, Show)
data Domain = NonnegativeReal | ProbabilityUnitInterval | IntegerDomain | BoundedReal Double Double | UnrestrictedReal deriving (Eq, Show)
data ReviewStatus = Active | RequiresReview | RequiresSensitivityTest | RequiresValidation | Revise deriving (Eq, Show)
data ModelComponent = ModelComponent { symbol :: String, componentName :: String, componentType :: ComponentType, domain :: Domain, interpretation :: String, status :: ReviewStatus } deriving (Eq, Show)
components :: [ModelComponent]
components = [ ModelComponent "S_t" "storage" StateVariable (BoundedReal 0 100) "Stored resource at time t." Active, ModelComponent "I_t" "inflow" InputVariable NonnegativeReal "Resource entering the system." RequiresReview, ModelComponent "D_t" "demand" InputVariable NonnegativeReal "Resource requested or consumed." RequiresReview, ModelComponent "lambda" "loss rate" Parameter ProbabilityUnitInterval "Fraction lost per period." RequiresSensitivityTest, ModelComponent "K" "capacity" Constraint NonnegativeReal "Maximum allowed storage." RequiresValidation ]
needsReview :: ModelComponent -> Bool
needsReview item = case status item of Active -> False; _ -> True
main :: IO ()
main = do putStrLn "Typed variables, parameters, and constraints:"; mapM_ print components; putStrLn "\nComponents requiring review:"; mapM_ print (filter needsReview components)
