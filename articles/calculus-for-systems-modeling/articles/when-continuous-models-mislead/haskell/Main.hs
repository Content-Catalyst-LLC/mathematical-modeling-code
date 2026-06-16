module Main where

data RiskStatus
  = Active
  | Review
  | Revise
  | Archive
  deriving (Show, Eq)

data ContinuityAssumption = ContinuityAssumption
  { assumptionName :: String
  , modelElement :: String
  , assumptionDescription :: String
  , reviewQuestion :: String
  , assumptionWarning :: String
  } deriving (Show, Eq)

data ContinuousModelRisk = ContinuousModelRisk
  { riskName :: String
  , riskPattern :: String
  , possibleConsequence :: String
  , governanceResponse :: String
  , riskStatus :: RiskStatus
  } deriving (Show, Eq)

assumptions :: [ContinuityAssumption]
assumptions =
  [ ContinuityAssumption "smooth_state_change" "state trajectory x(t)" "state changes gradually over modeled time" "Are shocks, events, or thresholds possible?" "Smooth output does not prove smooth system behavior."
  , ContinuityAssumption "continuous_rate_function" "dx/dt = f(x,t,theta)" "rate can be represented as a continuous function" "Does the process change through discrete decisions or regime switches?" "Rate continuity should be justified at the modeled scale."
  ]

risks :: [ContinuousModelRisk]
risks =
  [ ContinuousModelRisk "false_smoothness" "smooth curve hides structural breaks" "threshold, failure, or event dynamics are missed" "test for breaks and document discontinuities" Review
  , ContinuousModelRisk "equilibrium_bias" "steady-state result is overinterpreted" "transition cost, overshoot, delay, or distributional effect is hidden" "analyze trajectories and stability, not only equilibria" Review
  , ContinuousModelRisk "solver_confidence" "successful computation is mistaken for validation" "numerical artifacts appear as model insight" "record solver method, tolerance, convergence, and warnings" Review
  ]

main :: IO ()
main = do
  putStrLn "Continuity assumptions:"
  mapM_ print assumptions
  putStrLn ""
  putStrLn "Continuous model risks:"
  mapM_ print risks
