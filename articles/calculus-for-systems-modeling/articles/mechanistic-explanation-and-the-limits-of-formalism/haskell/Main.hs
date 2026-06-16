module Main where

data ClaimType
  = Mechanistic
  | Predictive
  | Exploratory
  | Descriptive
  | DecisionSupport
  deriving (Show, Eq)

data GovernanceStatus
  = Active
  | Review
  | Revise
  | Archive
  deriving (Show, Eq)

data MechanismRecord = MechanismRecord
  { mechanismName :: String
  , representedProcess :: String
  , entities :: String
  , activities :: String
  , evidenceStatus :: String
  , mechanismWarning :: String
  } deriving (Show, Eq)

data FormalRecord = FormalRecord
  { formalElement :: String
  , symbolOrStructure :: String
  , modelRole :: String
  , interpretationRequirement :: String
  , formalWarning :: String
  } deriving (Show, Eq)

data ExplanationClaim = ExplanationClaim
  { claimType :: ClaimType
  , supportedUse :: String
  , evidenceNeed :: String
  , scopeLimit :: String
  , governanceStatus :: GovernanceStatus
  } deriving (Show, Eq)

mechanismRecords :: [MechanismRecord]
mechanismRecords =
  [ MechanismRecord "stock_flow_accumulation" "stock changes through inflow and outflow" "stock, inflow, outflow" "accumulation, depletion, replacement" "synthetic teaching example" "A stock-flow equation is mechanistic only when flows represent real processes."
  , MechanismRecord "balancing_feedback" "state-dependent adjustment limits growth or change" "state variable, feedback coefficient, constraint" "adjustment, saturation, stabilization" "formal teaching example" "Feedback parameters require process interpretation and evidence."
  ]

formalRecords :: [FormalRecord]
formalRecords =
  [ FormalRecord "differential_equation" "dx/dt = f(x,t,theta)" "describes state change over time" "identify what process f represents" "A rate equation without process interpretation may be descriptive only."
  , FormalRecord "parameter" "theta" "controls model behavior" "record unit, source, range, and mechanism meaning" "Calibrated parameters are not automatically causal quantities."
  ]

claims :: [ExplanationClaim]
claims =
  [ ExplanationClaim Mechanistic "explains how an organized process can produce behavior" "process evidence, structural plausibility, sensitivity review" "applies only where the mechanism and assumptions hold" Review
  , ExplanationClaim Exploratory "investigates possible system behavior" "clear scenario assumptions and limitation notes" "not a confirmed mechanism or forecast" Active
  ]

main :: IO ()
main = do
  putStrLn "Mechanism records:"
  mapM_ print mechanismRecords
  putStrLn ""
  putStrLn "Formal records:"
  mapM_ print formalRecords
  putStrLn ""
  putStrLn "Explanation claims:"
  mapM_ print claims
