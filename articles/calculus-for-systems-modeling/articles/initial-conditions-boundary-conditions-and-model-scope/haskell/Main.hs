module Main where

data BoundaryType
  = Dirichlet
  | Neumann
  | Robin
  | Periodic
  | Absorbing
  | NoFlux
  deriving (Show, Eq)

data InitialCondition = InitialCondition
  { variableName :: String
  , initialValue :: Double
  , unitLabel :: String
  , sourceNote :: String
  , uncertaintyNote :: String
  } deriving (Show, Eq)

data BoundaryCondition = BoundaryCondition
  { boundaryName :: String
  , boundaryType :: BoundaryType
  , valueNote :: String
  , systemsInterpretation :: String
  , boundaryWarning :: String
  } deriving (Show, Eq)

data ScopeRecord = ScopeRecord
  { scopeDimension :: String
  , allowedDomain :: String
  , intendedUse :: String
  , reviewWarning :: String
  } deriving (Show, Eq)

initialConditions :: [InitialCondition]
initialConditions =
  [ InitialCondition "population_stock" 10.0 "state units" "synthetic teaching baseline" "baseline chosen for demonstration"
  , InitialCondition "time_start" 0.0 "time units" "model convention" "no empirical timestamp attached"
  ]

boundaryConditions :: [BoundaryCondition]
boundaryConditions =
  [ BoundaryCondition "left_edge" NoFlux "zero normal flux" "material does not leave through the left boundary" "No-flux boundaries may overstate retention if the real system is open."
  , BoundaryCondition "right_edge" Absorbing "outflow allowed" "material can leave the modeled domain" "Absorbing boundaries may understate feedback from surroundings."
  ]

scopeRecords :: [ScopeRecord]
scopeRecords =
  [ ScopeRecord "temporal_scope" "0 to 20 time units" "short-horizon teaching simulation" "Do not interpret as long-term forecast."
  , ScopeRecord "parameter_scope" "growth_rate between 0.1 and 0.6" "local sensitivity and teaching examples" "Do not use outside tested parameter range without review."
  , ScopeRecord "decision_scope" "exploratory and educational use" "model interpretation and workflow demonstration" "Do not treat as direct decision prescription."
  ]

main :: IO ()
main = do
  putStrLn "Initial conditions:"
  mapM_ print initialConditions
  putStrLn ""
  putStrLn "Boundary conditions:"
  mapM_ print boundaryConditions
  putStrLn ""
  putStrLn "Scope records:"
  mapM_ print scopeRecords
